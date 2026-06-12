import os
import json
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import SessionLocal, init_db, DBMenuItem, DBReservation

load_dotenv()
init_db()

# Startup integrity check
db = SessionLocal()
item_count = db.query(DBMenuItem).count()
print(f"📖 Registry loaded: {item_count} menu items active.")
db.close()

# --- Email Configuration ---
SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@bargemini.it")

# Treat the shipped placeholder values as "not configured" so we don't try
# (and fail) to send real mail until proper credentials are set.
_SMTP_PLACEHOLDERS = {"", "your-email@gmail.com", "your-app-password"}

def smtp_configured() -> bool:
    return bool(SMTP_SERVER) and SMTP_USER not in _SMTP_PLACEHOLDERS and SMTP_PASS not in _SMTP_PLACEHOLDERS

def send_status_email(to_email: str, name: str, status: str, date: str, time: str):
    if not smtp_configured():
        print(f"📧 [MOCK EMAIL — SMTP non configurato] A: {to_email} | Stato: {status} | Cliente: {name}")
        return

    subject = f"Bar Gemini: Prenotazione {status.replace('confirmed', 'Confermata').replace('cancelled', 'Annullata')}"
    
    if status == "confirmed":
        body = f"Ciao {name}!\n\nLa tua prenotazione per il {date} alle {time} è stata CONFERMATA.\nTi aspettiamo al Bar Gemini per un'esperienza indimenticabile.\n\nSaluti,\nLo Staff di Bar Gemini"
    elif status == "cancelled":
        body = f"Ciao {name},\n\nSiamo spiacenti di informarti che la tua prenotazione per il {date} alle {time} è stata ANNULLATA.\nPer qualsiasi domanda, non esitare a contattarci direttamente.\n\nSaluti,\nLo Staff di Bar Gemini"
    else:
        return

    msg = MIMEMultipart()
    msg['From'] = MAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Configuration from .env
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(",")

# Warn loudly if the app is running with insecure defaults.
if SECRET_KEY in ("fallback-secret-key", "y0ur_sup3r_s3cr3t_k3y_h3r3_f0r_b4rg3m1n1"):
    print("⚠️  SECRET_KEY debole/di default: i token JWT sono falsificabili. Imposta una chiave robusta e casuale in backend/.env.")
if os.getenv("ADMIN_PASSWORD", "bargemini2026") == "bargemini2026":
    print("⚠️  Password admin di default in uso: cambiala in backend/.env prima di andare in produzione.")
if "*" in ALLOW_ORIGINS:
    print("⚠️  ALLOW_ORIGINS=* (consentite tutte le origini): in produzione impostalo sul tuo dominio in backend/.env.")

app = FastAPI(title="Bar Gemini API")

# Auth uses Bearer tokens (Authorization header), not cookies, so credentials
# are not required — this keeps the wildcard origin valid for browsers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Models ---
class User(BaseModel):
    username: str
    email: Optional[str] = None

class MenuItemBase(BaseModel):
    # Only the name is required; everything else is optional so a dish can be
    # added quickly and filled in later.
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=500)
    price: float = Field(default=0, ge=0, le=10000)
    category: str = Field(default="Altro", max_length=100)
    image_url: Optional[str] = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Il nome è obbligatorio")
        return v

    @field_validator("description")
    @classmethod
    def trim_description(cls, v):
        return (v or "").strip()

    @field_validator("category")
    @classmethod
    def category_default(cls, v):
        return (v or "").strip() or "Altro"

    @field_validator("image_url")
    @classmethod
    def clean_image_url(cls, v):
        return (v.strip() or None) if v else None

# Response model — plain fields only. It must NOT re-run the input validators,
# otherwise pre-existing rows that predate a stricter rule would break the
# endpoint that returns them.
class MenuItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str = ""
    price: float = 0
    category: str = "Altro"
    image_url: Optional[str] = None

class ReservationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: str = Field(..., min_length=5, max_length=50)
    date: str
    time: str
    guests: int = Field(..., ge=1, le=50)
    ordered_items: Optional[str] = None  # JSON string of selected items

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Nome non valido")
        return v

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: str) -> str:
        v = v.strip()
        digits = sum(c.isdigit() for c in v)
        if digits < 6 or any(c not in "0123456789 +-()./" for c in v):
            raise ValueError("Numero di telefono non valido")
        return v

    @field_validator("date")
    @classmethod
    def date_valid(cls, v: str) -> str:
        try:
            d = datetime.strptime(v.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Data non valida (formato richiesto AAAA-MM-GG)")
        if d < datetime.now().date():
            raise ValueError("La data non può essere nel passato")
        return v

    @field_validator("time")
    @classmethod
    def time_valid(cls, v: str) -> str:
        try:
            datetime.strptime(v.strip(), "%H:%M")
        except ValueError:
            raise ValueError("Orario non valido (formato richiesto HH:MM)")
        return v

    @field_validator("ordered_items")
    @classmethod
    def items_valid_json(cls, v):
        if v is None:
            return v
        try:
            json.loads(v)
        except (ValueError, TypeError):
            raise ValueError("Pre-ordine non valido")
        return v

# Response model — plain fields only (see MenuItem note above): older rows may
# not satisfy the current input rules, but must still be readable.
class Reservation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str
    email: str
    phone: str
    date: str
    time: str
    guests: int
    ordered_items: Optional[str] = None
    status: str = "pending"
    created_at: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Mock User Store ---
fake_users_db = {
    os.getenv("ADMIN_USERNAME", "admin"): {
        "username": os.getenv("ADMIN_USERNAME", "admin"),
        "hashed_password": pwd_context.hash(os.getenv("ADMIN_PASSWORD", "bargemini2026")),
        "email": "admin@bargemini.it",
    }
}

# --- Auth Helpers ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

# --- Routes ---

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if user and pwd_context.verify(form_data.password, user["hashed_password"]):
        access_token = create_access_token(data={"sub": user["username"]})
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")

# -- Menu Endpoints --
@app.get("/api/menu", response_model=List[MenuItem])
async def get_menu(db: Session = Depends(get_db)):
    return db.query(DBMenuItem).all()

@app.post("/api/admin/menu", response_model=MenuItem)
async def add_menu_item(item: MenuItemBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = DBMenuItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.post("/api/admin/menu/bulk")
async def add_menu_items_bulk(items: List[MenuItemBase], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not items:
        raise HTTPException(status_code=400, detail="Nessun piatto da importare")
    if len(items) > 200:
        raise HTTPException(status_code=400, detail="Massimo 200 piatti per importazione")
    db.add_all(DBMenuItem(**item.model_dump()) for item in items)
    db.commit()
    return {"created": len(items)}

@app.put("/api/admin/menu/{item_id}", response_model=MenuItem)
async def update_menu_item(item_id: int, item: MenuItemBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(DBMenuItem).filter(DBMenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/admin/menu/{item_id}")
async def delete_menu_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(DBMenuItem).filter(DBMenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"status": "deleted"}

# -- Reservation Endpoints --
@app.post("/api/reservations")
async def create_reservation(res: ReservationBase, db: Session = Depends(get_db)):
    db_res = DBReservation(**res.model_dump())
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return {"status": "success", "id": db_res.id}

@app.get("/api/admin/reservations", response_model=List[Reservation])
async def get_reservations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(DBReservation).order_by(DBReservation.created_at.desc()).all()

@app.patch("/api/admin/reservations/{res_id}")
async def update_reservation_status(
    res_id: int, 
    status: str, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_res = db.query(DBReservation).filter(DBReservation.id == res_id).first()
    if not db_res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    db_res.status = status
    db.commit()
    
    # Send email in background
    background_tasks.add_task(send_status_email, db_res.email, db_res.name, status, db_res.date, db_res.time)
    
    return db_res

# --- Serve the built frontend (single origin) ---
# If the production build exists, the API and the website are served together,
# so the whole app can be shared behind one URL (e.g. a Cloudflare tunnel).
# In normal dev there's no dist/ folder, so this block is skipped.
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

FRONTEND_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "dist")

if os.path.isdir(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Real file (favicon, etc.) if present, otherwise the SPA entry point.
        candidate = os.path.join(FRONTEND_DIST, full_path)
        if full_path and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
