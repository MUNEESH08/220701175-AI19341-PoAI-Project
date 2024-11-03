import sqlite3

db_conn = sqlite3.connect('admin.db')
cursor = db_conn.cursor()

# List all tables to verify if the 'students' table exists
cursor.execute("SELECT * FROM students")
tables = cursor.fetchall()
print(tables)

cursor.close()
db_conn.close()
