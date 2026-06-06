import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Robust absolute path for SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'bargemini_v2.db')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DBMenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(500))
    price = Column(Float)
    category = Column(String(100))
    image_url = Column(String(500), nullable=True)

class DBReservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    date = Column(String(50))
    time = Column(String(50))
    guests = Column(Integer)
    status = Column(String(50), default="pending")
    ordered_items = Column(String(1000), nullable=True) # JSON string of items: [{"name": "...", "qty": 1}, ...]
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Seed with initial data if empty
    db = SessionLocal()
    if db.query(DBMenuItem).count() == 0:
        initial_menu = [
            # Consigliati dallo Chef
            DBMenuItem(name="Tortelli Verdi al Burro o Soffritto", description="Tortelli fatti a mano con spinaci e ricotta, burro e salvia", price=8.00, category="Consigliati dallo Chef"),
            DBMenuItem(name="Risotto ai Funghi Porcini", description="Riso Carnaroli con funghi porcini freschi e olio al tartufo", price=12.00, category="Consigliati dallo Chef"),
            DBMenuItem(name="Tagliata di Manzo al Rosmarino", description="Tagliata di manzo con rosmarino e sale grosso", price=18.00, category="Consigliati dallo Chef"),
            
            # Piatto Unico
            DBMenuItem(name="Insalatona Gemini", description="Insalata verde, radicchio, carote, rucola, pomodoro, tonno, mozzarella, uovo, mais", price=9.00, category="Piatto Unico"),
            DBMenuItem(name="Insalata Nizzarda", description="Insalata verde, carote, carciofi, mozzarella, scaglie di grana, glassa di balsamico", price=9.50, category="Piatto Unico"),
            DBMenuItem(name="Insalata di Pollo", description="Insalata verde, mais, pomodori, pollo grigliato, rucola, crostini. Senape o Olio al Limone", price=9.50, category="Piatto Unico"),
            DBMenuItem(name="Gemini Power Bowl", description="Quinoa, ceci, avocado, patata dolce e condimento alla tahina", price=11.00, category="Piatto Unico"),

            # Primi
            DBMenuItem(name="Tortelli di Zucca al Burro o al Soffritto", description="Tortelli di zucca fatti a mano, ricetta tradizionale", price=8.00, category="Primi"),
            DBMenuItem(name="Penne all' Arrabbiata", description="Sugo di pomodoro piccante con aglio e peperoncino", price=7.00, category="Primi"),
            DBMenuItem(name="Penne al Pomodoro", description="Classico sugo di pomodoro e basilico", price=7.00, category="Primi"),
            DBMenuItem(name="Mezze Maniche alla Carbonara", description="Uovo cremoso, pecorino e guanciale croccante", price=9.00, category="Primi"),
            DBMenuItem(name="Penne Speck e Funghi", description="Speck e funghi di montagna in salsa leggera", price=8.50, category="Primi"),
            DBMenuItem(name="Lasagnetta di Verdure", description="Pasta stratificata con verdure di stagione e besciamella", price=8.00, category="Primi"),
            DBMenuItem(name="Spaghetti alla Chitarra Cacio e Pepe", description="Spaghetti freschi con pecorino e pepe nero", price=10.00, category="Primi"),

            # Secondi
            DBMenuItem(name="Bresaola Rucola e Grana", description="Bresaola con rucola e scaglie di parmigiano", price=10.00, category="Secondi"),
            DBMenuItem(name="Caprese di Bufala", description="Mozzarella di bufala e pomodori con basilico", price=9.00, category="Secondi"),
            DBMenuItem(name="Crudo e Mozzarella", description="Prosciutto di Parma 24 mesi e mozzarella fresca", price=11.00, category="Secondi"),
            DBMenuItem(name="Scamorza alla Piastra", description="Scamorza affumicata fusa servita con patate al forno", price=9.50, category="Secondi"),
            DBMenuItem(name="Puntine in Salsa BBQ", description="Costine di maiale a lenta cottura con salsa BBQ e patate", price=10.00, category="Secondi"),
            DBMenuItem(name="Arrosto di Coniglio", description="Coniglio arrosto tradizionale con erbe e patate al forno", price=12.00, category="Secondi"),
            DBMenuItem(name="Flan di Parmigiano", description="Flan di parmigiano saporito con burro o spinaci piccanti", price=9.50, category="Secondi"),
            DBMenuItem(name="Polpette al Sugo", description="Polpette al sugo secondo la ricetta della nonna", price=11.00, category="Secondi"),

            # Contorni
            DBMenuItem(name="Insalata Mista", description="Insalata mista di stagione", price=3.50, category="Contorni"),
            DBMenuItem(name="Pomodori", description="Pomodori freschi con origano", price=3.50, category="Contorni"),
            DBMenuItem(name="Carote Julienne", description="Carote grattugiate marinate al limone", price=3.00, category="Contorni"),
            DBMenuItem(name="Patate al Forno", description="Patate al forno con rosmarino e aglio", price=4.00, category="Contorni"),
            DBMenuItem(name="Finocchi Marinati", description="Finocchi marinati agli agrumi", price=3.50, category="Contorni"),

            # Dolci
            DBMenuItem(name="Tartufo Nero/Bianco", description="Classico tartufo gelato italiano", price=4.50, category="Dolci"),
            DBMenuItem(name="Ananas al Naturale", description="Ananas fresco a fette", price=4.00, category="Dolci"),
            DBMenuItem(name="Soufflè al Cioccolato", description="Cuore caldo al cioccolato con panna montata", price=5.00, category="Dolci"),
            DBMenuItem(name="Crepes alla Nutella", description="Crepes fatte in casa con Nutella", price=4.00, category="Dolci"),
            DBMenuItem(name="Torta Cioccolatino", description="Ricca torta al cioccolato senza farina", price=4.00, category="Dolci"),
            DBMenuItem(name="Tiramisù Originale", description="Savoiardi bagnati al caffè con crema al mascarpone", price=6.00, category="Dolci"),
            
            # Bevande (Drinks)
            DBMenuItem(name="Negroni Sbagliato", description="Il classico cocktail milanese", price=9.00, category="Bevande"),
            DBMenuItem(name="Aperol Spritz", description="Aperitivo bilanciato perfettamente", price=8.00, category="Bevande"),
            DBMenuItem(name="Gemini Craft Beer", description="La nostra birra bionda artigianale locale", price=6.00, category="Bevande"),
            DBMenuItem(name="Vino della Casa (Rosso/Bianco)", description="Selezione curata dai vigneti locali", price=5.00, category="Bevande"),
        ]
        db.add_all(initial_menu)
        db.commit()
    db.close()
