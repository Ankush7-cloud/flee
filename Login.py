import streamlit as st
from db_connection import get_connection

def app():
    st.title("🔐 Login")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.warning("🚫 Please enter both username and password.")
            return

        conn = get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR PRIMARY KEY,
                password VARCHAR
            )
        """)

        result = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchall()

        if result:
            st.success("✅ Login successful!")
            st.info("ℹ This login page is for testing only and does not link to Admin.")
        else:
            st.error("❌ Invalid username or password.")
