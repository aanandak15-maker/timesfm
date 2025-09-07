#!/usr/bin/env python3
"""
Comprehensive system status check
"""

import requests
import sqlite3
import subprocess
import sys

def check_system_status():
    """Check all systems and report status"""
    
    print("🔍 AgriForecast.ai System Status Check")
    print("=" * 50)
    
    # Check all running systems
    systems = [
        ("Simple Forecasting", "http://localhost:8501"),
        ("MVP System", "http://localhost:8502"), 
        ("Multi-Field System", "http://localhost:8503"),
        ("User Auth System", "http://localhost:8504"),
        ("Test System", "http://localhost:8505")
    ]
    
    print("\n🌐 Web Systems Status:")
    for name, url in systems:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: {url} - RUNNING")
            else:
                print(f"⚠️  {name}: {url} - Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: {url} - NOT RUNNING ({e})")
    
    # Check databases
    print("\n🗄️  Database Status:")
    databases = [
        "agriforecast_simple.db",
        "agriforecast_multi_field.db", 
        "agriforecast_user_auth.db"
    ]
    
    for db in databases:
        try:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            
            # Get table counts
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"✅ {db}: {len(tables)} tables")
            
            # Check users table if exists
            if any('users' in table[0] for table in tables):
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                print(f"   👥 Users: {user_count}")
            
            # Check farms table if exists
            if any('farms' in table[0] for table in tables):
                cursor.execute("SELECT COUNT(*) FROM farms")
                farm_count = cursor.fetchone()[0]
                print(f"   🏡 Farms: {farm_count}")
            
            # Check fields table if exists
            if any('fields' in table[0] for table in tables):
                cursor.execute("SELECT COUNT(*) FROM fields")
                field_count = cursor.fetchone()[0]
                print(f"   🌾 Fields: {field_count}")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ {db}: ERROR - {e}")
    
    # Check Python environment
    print("\n🐍 Python Environment:")
    print(f"Python version: {sys.version}")
    
    # Check if virtual environment is active
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment: ACTIVE")
    else:
        print("⚠️  Virtual environment: NOT DETECTED")
    
    # Check key dependencies
    print("\n📦 Key Dependencies:")
    dependencies = ['streamlit', 'pandas', 'numpy', 'plotly', 'sqlite3']
    
    for dep in dependencies:
        try:
            if dep == 'sqlite3':
                import sqlite3
                print(f"✅ {dep}: Available")
            else:
                __import__(dep)
                print(f"✅ {dep}: Available")
        except ImportError:
            print(f"❌ {dep}: MISSING")
    
    print("\n🎯 Recommendations:")
    print("1. If systems are not running, start them with:")
    print("   source .venv/bin/activate && streamlit run [filename] --server.port [port]")
    print("2. If databases are empty, run demo data scripts")
    print("3. If you see errors, check the terminal output")
    print("4. User Auth System: http://localhost:8504")
    
    print("\n" + "=" * 50)
    print("✅ System check complete!")

if __name__ == "__main__":
    check_system_status()
