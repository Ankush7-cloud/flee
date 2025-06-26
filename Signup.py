import streamlit as st
from db_connection import get_connection

def app():
    st.title("📝 Signup")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not username or not password:
            st.warning("🚫 Please fill in all fields.")
            return

        if password != confirm_password:
            st.error("❌ Passwords do not match.")
            return

        conn = get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR PRIMARY KEY,
                password VARCHAR
            )
        """)

        # Check if user exists
        user_exists = conn.execute(
            "SELECT COUNT(*) FROM users WHERE username = ?",
            (username,)
        ).fetchone()[0]

        if user_exists:
            st.error("❌ Username already taken. Choose another.")
        else:
            conn.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            st.success("✅ Account created successfully. You can now log in.")
