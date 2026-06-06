import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
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

def send_status_email(to_email: str, name: str, status: str, date: str, time: str):
    if not SMTP_SERVER or not SMTP_USER:
        print(f"📧 [MOCK EMAIL] To: {to_email} | Status: {status} | User: {name}")
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
    name: str
    description: str
    price: float
    category: str
    image_url: Optional[str] = None

class MenuItem(MenuItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ReservationBase(BaseModel):
    name: str
    email: str
    phone: str
    date: str
    time: str
    guests: int
    ordered_items: Optional[str] = None # JSON string of selected items

class Reservation(ReservationBase):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
