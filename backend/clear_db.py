import sys
import os
from sqlalchemy import MetaData

# Add the current directory to sys.path so we can import database
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from database import engine

def clear_db():
    print(f"🗑️ Clearing database...")
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
    print("✅ All tables dropped.")

if __name__ == "__main__":
    try:
        clear_db()
    except Exception as e:
        print(f"❌ Error: {e}")
