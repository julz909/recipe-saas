import sqlite3

def get_connection():
    return sqlite3.connect("app.db")

# =========================
# INIT DATABASE
# =========================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        title TEXT,
        ingredients TEXT
    )
    """)

    conn.commit()
    conn.close()

# =========================
# ADD RECIPE
# =========================
def add_recipe(username, title, ingredients):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    INSERT INTO recipes (username, title, ingredients)
    VALUES (?, ?, ?)
    """, (username, title, ingredients))

    conn.commit()
    conn.close()

# =========================
# GET RECIPES
# =========================
def get_recipes(username):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    SELECT title, ingredients FROM recipes
    WHERE username=?
    """, (username,))

    rows = c.fetchall()
    conn.close()

    return rows