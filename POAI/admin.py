import sqlite3
import bcrypt

conn = sqlite3.connect('admin.db')
cursor = conn.cursor()

user = input("Enter Admin Name: ")
pwd = input("Enter Password: ").encode('utf-8')
hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())

cursor.execute('''
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert a sample admin user
cursor.execute('''
INSERT INTO admin (username, password) VALUES (?, ?)
''', (user, hashed_pwd))

conn.commit()
conn.close()
print("Successfully Inserted!")
