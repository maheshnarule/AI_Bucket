# # user.py
# import sqlite3

# def create_db():
#     # Connect to SQLite (creates user.db if it doesn't exist)
#     conn = sqlite3.connect("user.db")
#     cursor = conn.cursor()

#     # Create users table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         )
#     """)

#     conn.commit()
#     conn.close()
#     print("✅ user.db created successfully with 'users' table.")

# if __name__ == "__main__":
#     create_db()
import sqlite3

conn = sqlite3.connect("user.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
               ("John Doe", "john@example.com", "1234"))
cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
               ("Alice Smith", "alice@example.com", "abcd"))

conn.commit()
conn.close()

print("✅ Sample users added!")
