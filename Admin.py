import streamlit as st
import pandas as pd
from db_connection import get_connection

def app():
    st.title("🛠 Admin Panel")

    # Admin sub-sections
    section = st.sidebar.radio("Admin Sections", ["Dashboard", "User Management", "Resource Management"])

    conn = get_connection()

    # Ensure tables exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            service_tag VARCHAR,
            employee_id INT,
            device_type VARCHAR,
            memory INT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR,
            password VARCHAR
        )
    """)

    # Insert sample devices once
    if conn.execute("SELECT COUNT(*) FROM devices").fetchone()[0] == 0:
        conn.execute("""
            INSERT INTO devices VALUES
            ('ABC123', 1001, 'GPU', 16),
            ('DEF456', 1002, 'Desktop', 32),
            ('GHI789', 1003, 'GPU', 8),
            ('JKL012', 1004, 'Desktop', 64)
        """)

    # ========== Dashboard ==========
    if section == "Dashboard":
        st.subheader("📊 Device Table")
        df = conn.execute("SELECT * FROM devices").df()
        st.dataframe(df)

        st.subheader("✏ Run SQL Query (UPDATE / DELETE / INSERT)")
        query = st.text_area("Enter SQL query")

        if st.button("Execute SQL"):
            try:
                conn.execute(query)
                st.success("✅ Query executed successfully.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

        # Updated table
        df2 = conn.execute("SELECT * FROM devices").df()
        st.subheader("🔄 Updated Device Table")
        st.dataframe(df2)

    # ========== User Management ==========
    elif section == "User Management":
        st.subheader("👤 User Table")
        users = conn.execute("SELECT * FROM users").df()
        st.dataframe(users)

    # ========== Resource Management ==========
    elif section == "Resource Management":
        st.subheader("💾 Resource Management")
        st.info("You can add device forms or edit tools here later.")
