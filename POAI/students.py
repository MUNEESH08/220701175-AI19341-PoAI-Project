from cryptography.fernet import Fernet
import pandas as pd
import sqlite3

# Load the key from the secret.key file
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

# Create a Fernet instance with the provided key
cipher_suite = Fernet(key)

# CSV file to read from
csv_file = 'Datas.csv'

# Create database connection
db_conn = sqlite3.connect('admin.db')
cursor = db_conn.cursor()

# Create table in SQLite database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        roll_no TEXT,
        name_of_the_student TEXT,
        company_employed TEXT,
        campus_status TEXT,
        lpa TEXT,
        cgpa TEXT,
        batch TEXT
    )
''')

# Read CSV file using pandas
df = pd.read_csv(csv_file)

# Strip any extra spaces from the column headers
df.columns = df.columns.str.strip()

# Insert data into the database
for index, row in df.iterrows():
    # Convert roll_no to string without encryption
    roll_no = str(row['ROLL NO.'])

    # Encrypt other fields
    encrypted_name = cipher_suite.encrypt(str(row['NAME OF THE STUDENT']).encode('utf-8'))
    encrypted_company = cipher_suite.encrypt(str(row['COMPANY EMPLOYED']).encode('utf-8'))
    encrypted_campus_status = cipher_suite.encrypt(str(row['ON/OFF CAMPUS/HIGHER EDUCATION/ENTREPRENEUR']).encode('utf-8'))
    encrypted_lpa = cipher_suite.encrypt(str(row['LPA']).encode('utf-8'))
    encrypted_cgpa = cipher_suite.encrypt(str(row['CGPA']).encode('utf-8'))
    encrypted_batch = cipher_suite.encrypt(str(row['BATCH']).encode('utf-8'))

    # Prepare data to insert into the database
    data = (
        roll_no,
        encrypted_name.decode('utf-8'),  # Store as text in SQLite
        encrypted_company.decode('utf-8'),
        encrypted_campus_status.decode('utf-8'),
        encrypted_lpa.decode('utf-8'),
        encrypted_cgpa.decode('utf-8'),
        encrypted_batch.decode('utf-8')
    )
    
    # Insert data into the students table
    cursor.execute('''
        INSERT INTO students(
            roll_no,
            name_of_the_student,
            company_employed,
            campus_status,
            lpa,
            cgpa,
            batch
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)

# Commit and close connection
db_conn.commit()
db_conn.close()

print("Data has been successfully inserted into the database.")
