#!/usr/bin/env python3
"""Migration script to add API cost tracking table."""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base
from models import ApiCost
from sqlalchemy import inspect

def table_exists(table_name):
    """Check if a table exists in the database."""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def main():
    """Run migration to add ApiCost table."""
    print("Running migration: Add API cost tracking...")
    
    # Check if table already exists
    if table_exists('api_costs'):
        print("✅ Table 'api_costs' already exists, skipping creation.")
        return
    
    # Create the new table
    print("Creating 'api_costs' table...")
    ApiCost.__table__.create(engine)
    print("✅ Table 'api_costs' created successfully!")
    
    print("\nMigration completed successfully!")

if __name__ == "__main__":
    main()