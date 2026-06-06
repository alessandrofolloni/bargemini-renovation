import sys
import os

# Add the current directory to sys.path so we can import database
sys.path.append(os.getcwd())

from database import init_db

if __name__ == "__main__":
    print("🌱 Initializing and seeding the database...")
    try:
        init_db()
        print("✅ Database 'bargemini.db' created and populated successfully!")
        print("You can now open it in TablePlus.")
    except Exception as e:
        print(f"❌ Error: {e}")
