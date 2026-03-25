import sqlite3

# Database file name
DB_NAME = "expenses.db"


# Create connection to SQLite database
def connect():
    return sqlite3.connect(DB_NAME)


# Create database tables if they don't exist
def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
    """)

    # Expenses table (linked to user)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# =========================
# USER FUNCTIONS
# =========================

# Create a new user
def create_user(username, email, password_hash):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (username, email, password_hash)
    VALUES (?, ?, ?)
    """, (username, email, password_hash))

    conn.commit()
    conn.close()


# Get user by email (used for login)
def get_user_by_email(email):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    return user


# Get user by username (used for registration validation)
def get_user_by_username(username):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    conn.close()

    return user


# =========================
# EXPENSE FUNCTIONS
# =========================

# Add a new expense (linked to a specific user)
def add_expense(amount, category, description, date, user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses (amount, category, description, date, user_id)
    VALUES (?, ?, ?, ?, ?)
    """, (amount, category, description, date, user_id))

    conn.commit()
    conn.close()


# Get all expenses for a specific user
def get_expenses(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM expenses WHERE user_id = ?
    """, (user_id,))

    data = cursor.fetchall()
    conn.close()

    return data


# Get expenses by category for a specific user
def get_by_category(category, user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM expenses
    WHERE category = ? AND user_id = ?
    """, (category, user_id))

    data = cursor.fetchall()
    conn.close()

    return data


# Delete expense by ID (only for specific user)
def delete_expense(expense_id, user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM expenses
    WHERE id = ? AND user_id = ?
    """, (expense_id, user_id))

    conn.commit()
    conn.close()


# Get total expenses per category for a user
def total_by_category(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    WHERE user_id = ?
    GROUP BY category
    """, (user_id,))

    data = cursor.fetchall()
    conn.close()

    return data


# Update expense amount (only for specific user)
def update_expense(expense_id, new_amount, user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE expenses
    SET amount = ?
    WHERE id = ? AND user_id = ?
    """, (new_amount, expense_id, user_id))

    conn.commit()
    conn.close()