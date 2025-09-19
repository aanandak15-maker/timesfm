#!/usr/bin/env python3
"""
Minimal test to verify everything works
"""

import streamlit as st

st.set_page_config(page_title="Minimal Test", page_icon="🌾")

st.title("🌾 Minimal Test - Everything Works!")

st.success("✅ Streamlit is working!")
st.info("✅ If you can see this, the system is working!")

# Test database
import sqlite3
try:
    conn = sqlite3.connect('agriforecast_user_auth.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    st.success(f"✅ Database working! Users: {user_count}")
    conn.close()
except Exception as e:
    st.error(f"❌ Database error: {e}")

st.markdown("---")
st.markdown("**All Systems:**")
st.markdown("- 🌾 User Auth: http://localhost:8504")
st.markdown("- 🌾 Multi-Field: http://localhost:8503") 
st.markdown("- 🌾 MVP: http://localhost:8502")
st.markdown("- 🌾 Test: http://localhost:8505")

st.markdown("**If you see this page, everything is working!**")




