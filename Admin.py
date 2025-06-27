import streamlit as st
import pandas as pd
from db_connection import get_connection

def app():
    st.title("🛠 Admin Panel")

    # Sidebar for admin sections
    section = st.sidebar.radio("Admin Sections", ["Dashboard", "User Management", "Resource Management"])

    conn = get_connection()

    # Create both tables if not exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR,
            password VARCHAR
        )
    """)

    # ========== Dashboard ==========
    if section == "Dashboard":
        st.subheader("📊 Device Table Management")

        col1, col2, col3 = st.columns(3)

        # ➕ Create Table
        with col1:
            if st.button("➕ Create Table"):
                try:
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS devices (
                            service_tag VARCHAR PRIMARY KEY,
                            employee_id INT,
                            device_type VARCHAR,
                            memory INT
                        )
                    """)
                    st.success("✅ Table created with service_tag as PRIMARY KEY.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        # 🗑 Delete all
        with col2:
            if st.button("🗑 Delete All Records"):
                try:
                    conn.execute("DELETE FROM devices")
                    st.success("✅ All device records deleted.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        # ➕ Insert sample
        with col3:
            if st.button("➕ Insert Sample Data"):
                try:
                    conn.execute("""
                        INSERT OR IGNORE INTO devices VALUES
                        ('ABC123', 1001, 'GPU', 16),
                        ('DEF456', 1002, 'Desktop', 32),
                        ('GHI789', 1003, 'GPU', 8),
                        ('JKL012', 1004, 'Desktop', 64)
                    """)
                    st.success("✅ Sample data inserted (skipped duplicates).")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        # 📋 Show table
        try:
            df = conn.execute("SELECT * FROM devices").df()
            st.dataframe(df)
        except:
            st.warning("⚠ Table not found. Try 'Create Table' first.")

        # ✏ Custom SQL
        st.subheader("✏ Custom SQL Query")
        query = st.text_area("Enter your SQL (e.g., UPDATE devices SET memory=64 WHERE employee_id=1001)")

        if st.button("Execute SQL Query"):
            try:
                conn.execute(query)
                st.success("✅ SQL executed.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

        # 🔄 Show updated table
        try:
            updated_df = conn.execute("SELECT * FROM devices").df()
            st.subheader("🔄 Updated Device Table")
            st.dataframe(updated_df)
        except:
            st.warning("⚠ Table not found.")

    # ========== User Management ==========
    elif section == "User Management":
        st.subheader("👤 User Table")
        try:
            users_df = conn.execute("SELECT * FROM users").df()
            st.dataframe(users_df)
        except:
            st.warning("⚠ User table not found.")

    # ========== Resource Management ==========
    elif section == "Resource Management":
        st.subheader("💾 Resource Management")
        st.info("You can add forms or reports here later (e.g., available memory, GPU tracking, etc.)")
