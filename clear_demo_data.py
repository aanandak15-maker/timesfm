#!/usr/bin/env python3
"""
Clear demo data and prepare for real farm data
"""

import sqlite3

def clear_demo_data():
    """Clear all demo data from the database"""
    
    # Connect to database
    conn = sqlite3.connect('agriforecast_multi_field.db')
    cursor = conn.cursor()
    
    # Clear all data
    cursor.execute("DELETE FROM field_data")
    cursor.execute("DELETE FROM yield_predictions")
    cursor.execute("DELETE FROM field_zones")
    cursor.execute("DELETE FROM fields")
    cursor.execute("DELETE FROM farms")
    
    # Reset auto-increment counters
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='farms'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='fields'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='field_zones'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='field_data'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='yield_predictions'")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("✅ Demo data cleared successfully!")
    print("🌾 Ready for your real farm data!")

if __name__ == "__main__":
    clear_demo_data()
