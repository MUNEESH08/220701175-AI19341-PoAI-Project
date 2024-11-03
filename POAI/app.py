from flask import Flask, render_template, request, send_from_directory, jsonify
from cryptography.fernet import Fernet
import sqlite3
import os
import pandas as pd
import bcrypt
from models.resume_analyzer import analyze_resume
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Limit file size to 16MB
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
port = 5000
company_data = pd.read_csv('company_list.csv')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/company')
def company():
    return render_template('company.html')

@app.route('/zoho')
def zoho():
    return render_template('zoho.html')

@app.route('/log')
def login_page():
    return send_from_directory('templates', 'login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')

    try:
        conn = sqlite3.connect('admin.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM admin WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password, result[0]):
            return send_from_directory('templates', 'details.html')
        else:
            return jsonify({'message': 'Only Admins are allowed...'}), 401
    except Exception as e:
        print(f'Error connecting to SQLite or querying the database: {e}')
        return jsonify({'message': 'Internal server error.'}), 500

@app.route('/details', methods=['POST'])
def get_student_details():
    regno = request.form['regno']

    # Load the encryption key
    with open("secret.key", "rb") as key_file:
        key = key_file.read()

    cipher_suite = Fernet(key)

    try:
        conn = sqlite3.connect('admin.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name_of_the_student, company_employed, campus_status, lpa, cgpa, batch FROM students WHERE roll_no=?", (regno,))
        result = cursor.fetchone()
        conn.close()

        if result:
            student_details = {
                'roll_no': result[0],
                'name': cipher_suite.decrypt(result[1].encode()).decode(),
                'company': cipher_suite.decrypt(result[2].encode()).decode(),
                'campus_status': cipher_suite.decrypt(result[3].encode()).decode(),
                'lpa': cipher_suite.decrypt(result[4].encode()).decode(),
                'cgpa': cipher_suite.decrypt(result[5].encode()).decode(),
                'batch': cipher_suite.decrypt(result[6].encode()).decode()
            }
            return jsonify({'student': student_details})
        else:
            return jsonify({'error': 'No student found with that registration number.'})
    except Exception as e:
        print(f'Error querying the database: {e}')
        return jsonify({'message': 'Internal server error.'}), 500

@app.route('/skillc')
def skillc():
    return render_template('skill.html')

# Route to handle company search and return JSON response
@app.route('/skill', methods=['POST'])
def search():
    company_name = request.form['company']
    result = company_data[company_data['Company'].str.contains(company_name, case=False, na=False)]

    if result.empty:
        return jsonify({'error': 'Company not found!'})

    return jsonify(result.to_dict(orient='records'))

@app.route('/resume')
def resume():
    return render_template('resume.html')

# Route to handle file upload and analysis
@app.route('/resume-upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Real-time analysis with AJAX update
            analysis_results = analyze_resume(file_path)
            
            return jsonify({'results': analysis_results}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'File format not supported. Please upload a PDF or DOCX.'}), 400

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(host="0.0.0.0",port=port)
