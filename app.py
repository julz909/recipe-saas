from database import init_db, add_recipe, get_recipes
import streamlit as st

init_db()

import sqlite3

import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Recipe SaaS",
    page_icon="🍳",
    layout="centered"
)

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# LOGIN PAGE
# =========================
def login_page():

    st.title("🔐 Recipe SaaS Login")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ---------------- LOGIN ----------------
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            conn = sqlite3.connect("app.db")
            c = conn.cursor()

            c.execute(
                "SELECT password FROM users WHERE username=?",
                (username,)
            )

            result = c.fetchone()
            conn.close()

            if result is None:
                st.error("User not found")
            else:
                stored_hash = result[0]

                if verify_password(password, stored_hash):
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    # ---------------- SIGN UP ----------------
    with tab2:
        new_user = st.text_input("Create username", key="signup_user")
        new_pass = st.text_input("Create password", type="password", key="signup_pass")

        if st.button("Sign Up"):
            conn = sqlite3.connect("app.db")
            c = conn.cursor()

            try:
                hashed_pw = hash_password(new_pass)

                c.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (new_user, hashed_pw)
                )

                conn.commit()
                st.success("Account created! Now login.")

            except:
                st.error("User already exists")

            conn.close()

# =========================
# LOGOUT
# =========================
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.history = []
    st.rerun()

# =========================
# APP PAGE
# =========================
def app_page():

    st.sidebar.title(f"🍳 {st.session_state.current_user}")

    if st.sidebar.button("Logout"):
        logout()

    page = st.sidebar.radio("Navigation", ["Dashboard", "History"])

    # ================= DASHBOARD =================
    
    if page == "Dashboard":

        st.title("📊 Dashboard")

        ingredients = st.text_input("Enter ingredients")
        generate = st.button("Generate Recipe")

        if generate and ingredients:

            title = "🍲 Custom Recipe"

            add_recipe(
                st.session_state.current_user,
                title,
                ingredients
            )

            st.success("Recipe saved!")

        st.subheader("Latest Recipe")

        rows = get_recipes(st.session_state.current_user)

        if rows:
            latest = rows[-1]
            st.write(latest[0])
            st.write(latest[1])

    # ================= HISTORY =================
    if page == "History":

        st.title("📜 History")

        rows = get_recipes(st.session_state.current_user)

        if rows:
            for r in reversed(rows):
                st.write(f"🍽 {r[0]} — {r[1]}")
        else:
            st.info("No recipes yet")

# =========================
# ROUTER
# =========================
if not st.session_state.logged_in:
    login_page()
else:
    app_page()