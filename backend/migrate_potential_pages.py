#!/usr/bin/env python3
"""
Database migration to add PotentialPage table for page preview & selection functionality
"""

import sys
from sqlalchemy import create_engine, text
from database import engine
from models import Base

def migrate_potential_pages():
    """Create the potential_pages table if it doesn't exist"""
    
    print("🔄 Running PotentialPage database migration...")
    
    try:
        # Create all tables (this will create potential_pages if it doesn't exist)
        Base.metadata.create_all(bind=engine)
        
        # Test that the table was created by querying it
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='potential_pages'"))
            table_exists = result.fetchone() is not None
            
            if table_exists:
                print("✅ potential_pages table created successfully")
                
                # Check the table structure
                result = conn.execute(text("PRAGMA table_info(potential_pages)"))
                columns = result.fetchall()
                print(f"📋 Table structure: {len(columns)} columns")
                for col in columns:
                    print(f"   - {col[1]} ({col[2]})")
            else:
                print("❌ Failed to create potential_pages table")
                return False
                
        print("✅ Migration completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_potential_pages()
    sys.exit(0 if success else 1)