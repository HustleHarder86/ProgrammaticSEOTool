#!/usr/bin/env python3
"""
Fix the integration between variable generation and potential pages generation
"""

import sys
from sqlalchemy import create_engine, text
from database import engine
from models import Base

def add_variables_data_storage():
    """Add a column to store generated variables data in templates table"""
    
    print("🔧 Fixing Variable Integration...")
    
    try:
        with engine.connect() as conn:
            # Check if generated_variables_data column exists
            result = conn.execute(text("PRAGMA table_info(templates)"))
            columns = [col[1] for col in result.fetchall()]
            
            if 'generated_variables_data' not in columns:
                print("📋 Adding generated_variables_data column to templates table...")
                conn.execute(text(
                    "ALTER TABLE templates ADD COLUMN generated_variables_data JSON"
                ))
                conn.commit()
                print("✅ Column added successfully")
            else:
                print("✅ generated_variables_data column already exists")
                
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = add_variables_data_storage()
    sys.exit(0 if success else 1)