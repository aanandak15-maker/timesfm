#!/usr/bin/env python3
"""
Quick fix for Streamlit deprecation warnings
Replace use_container_width with width parameter
"""

import os
import re

def fix_streamlit_warnings():
    """Fix use_container_width deprecation warnings"""
    
    # Files to fix (excluding .venv directory)
    files_to_fix = [
        'agriforecast_mobile.py',
        'soil_health_system.py', 
        'agriforecast_multi_field.py',
        'market_intelligence_system.py',
        'agriforecast_simple.py',
        'iot_integration_system.py',
        'advanced_analytics_dashboard.py',
        'agriforecast_mvp.py',
        'report_generation_system.py',
        'crop_management_system.py',
        'agriforecast_user_simple.py'
    ]
    
    fixed_count = 0
    
    for filename in files_to_fix:
        if os.path.exists(filename):
            print(f"Fixing {filename}...")
            
            with open(filename, 'r') as f:
                content = f.read()
            
            # Replace use_container_width=True with width='stretch'
            content = re.sub(
                r'use_container_width=True',
                "width='stretch'",
                content
            )
            
            # Replace use_container_width=False with width='content'
            content = re.sub(
                r'use_container_width=False',
                "width='content'",
                content
            )
            
            # Write back the fixed content
            with open(filename, 'w') as f:
                f.write(content)
            
            fixed_count += 1
            print(f"✅ Fixed {filename}")
        else:
            print(f"⚠️ File not found: {filename}")
    
    print(f"\n🎉 Fixed {fixed_count} files!")
    print("Streamlit deprecation warnings should now be resolved.")

if __name__ == "__main__":
    fix_streamlit_warnings()




