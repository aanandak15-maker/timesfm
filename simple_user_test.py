#!/usr/bin/env python3
"""
Simple test of user authentication system
"""

import streamlit as st
import sqlite3
import hashlib

# Configure page
st.set_page_config(
    page_title="User Auth Test",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 User Authentication Test")

# Test database connection
try:
    conn = sqlite3.connect('agriforecast_user_auth.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute("SELECT id, username, email, full_name FROM users")
    users = cursor.fetchall()
    
    st.success(f"✅ Database connected! Found {len(users)} users")
    
    if users:
        st.subheader("Existing Users:")
        for user in users:
            st.write(f"- {user[1]} ({user[2]}) - {user[3]}")
    
    # Get all farms
    cursor.execute("SELECT id, user_id, name, location FROM farms")
    farms = cursor.fetchall()
    
    st.subheader(f"Existing Farms: {len(farms)}")
    for farm in farms:
        st.write(f"- {farm[2]} (User ID: {farm[1]}) - {farm[3]}")
    
    # Get all fields
    cursor.execute("SELECT id, user_id, farm_id, name, crop_type, area_acres FROM fields")
    fields = cursor.fetchall()
    
    st.subheader(f"Existing Fields: {len(fields)}")
    for field in fields:
        st.write(f"- {field[3]} ({field[4]}) - {field[5]:.2f} acres (User ID: {field[1]}, Farm ID: {field[2]})")
    
    conn.close()
    
except Exception as e:
    st.error(f"❌ Database error: {e}")

# Test user creation form
st.subheader("Test User Creation")

with st.form("test_user_form"):
    username = st.text_input("Username", value="test_user_2")
    email = st.text_input("Email", value="test2@example.com")
    full_name = st.text_input("Full Name", value="Test User 2")
    password = st.text_input("Password", type="password", value="test123")
    
    submitted = st.form_submit_button("Create Test User")
    
    if submitted:
        try:
            conn = sqlite3.connect('agriforecast_user_auth.db', check_same_thread=False)
            cursor = conn.cursor()
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)",
                (username, email, password_hash, full_name)
            )
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            st.success(f"✅ User created successfully! ID: {user_id}")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error creating user: {e}")

st.info("🌐 Main User Auth System: http://localhost:8504")




