from sqlalchemy import create_all_engines, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./bargemini.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DBMenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String)
    image_url = Column(String, nullable=True)

class DBReservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    date = Column(String)
    time = Column(String)
    guests = Column(Integer)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Seed with initial data if empty
    db = SessionLocal()
    if db.query(DBMenuItem).count() == 0:
        initial_menu = [
            DBMenuItem(name="Espresso", description="Classic Italian espresso", price=1.20, category="Bar"),
            DBMenuItem(name="Cappuccino", description="Creamy cappuccino with fresh milk", price=1.50, category="Bar"),
            DBMenuItem(name="Aperol Spritz", description="The classic Italian aperitivo", price=5.00, category="Aperitifs"),
            DBMenuItem(name="Tagliatelle al Ragu", description="Homemade pasta with traditional meat sauce", price=10.00, category="Kitchen"),
        ]
        db.add_all(initial_menu)
        db.commit()
    db.close()
