"""Initialize the database with tables."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_db, engine
from models import Base

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {', '.join(tables)}")
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_tables()