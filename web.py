from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskadminlte_db'
mysql = MySQL(app)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

# Fungsi bantuan untuk memeriksa ekstensi file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/register")
def register():
     # Mendeteksi apakah perangkat adalah perangkat mobile
    user_agent = request.headers.get('User-Agent').lower()
    is_mobile = any(mobile in user_agent for mobile in ['iphone', 'android', 'blackberry', 'opera mini', 'windows mobile'])
    
    if is_mobile:
        return render_template('register.html',menu='register')
    else:
        return render_template('mobile-only.html')

@app.route("/registerwajah", methods=["POST"])
def registerwajah():
    if 'gambarWajah' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})
    
    email = request.form.get('email')
    nama = request.form.get('nama')
    nim = request.form.get('nim')
    prodi = request.form.get('prodi')
    angkatan = request.form.get('angkatan')
    file = request.files['gambarWajah']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})
    
    if email and nama and nim and prodi and angkatan and file and allowed_file(file.filename):  # Memastikan semua data diterima
        filename = secure_filename("register_" + nim) + ".jpg"  # Ganti ekstensi sesuai kebutuhan
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO mahasiswaterdaftar(email,nama,nim,prodi,angkatan,files) VALUES(%s,%s,%s,%s,%s,%s)", (email,nama,nim,prodi,angkatan,filename))
            mysql.connection.commit()
            cur.close()
            response = {'success': True, 'message': 'Data berhasil disimpan'}
            return jsonify(response)
        except Exception as e:
            response = {'success': False, 'message': str(e)}
            return jsonify(response), 500  # Mengembalikan kode status 500 (Internal Server Error) jika terjadi kesalahan
    else:
        response = {'success': False, 'message': 'Missing required data'}
        return jsonify(response), 400  # Mengembalikan kode status 400 (Bad Request) jika data yang diperlukan tidak ditemukan

@app.route("/login")
def login():
     # Mendeteksi apakah perangkat adalah perangkat mobile
    user_agent = request.headers.get('User-Agent').lower()
    is_mobile = any(mobile in user_agent for mobile in ['iphone', 'android', 'blackberry', 'opera mini', 'windows mobile'])
    
    if is_mobile:
        return render_template('login.html',menu='login')
    else:
        return render_template('mobile-only.html')
@app.route("/loginkelas", methods=["POST"])
def loginkelas():
    if 'gambarWajah' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})
    
    nim = request.form.get('nim')
    file = request.files['gambarWajah']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})
    
    if nim and file and allowed_file(file.filename):  # Memastikan semua data diterima
        filename = secure_filename("login_" + nim) + ".jpg"  # Ganti ekstensi sesuai kebutuhan
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        response = {'success': True, 'message': 'Selamat Datang!'}
        return jsonify(response)


        # try:
        #     cur = mysql.connection.cursor()
        #     cur.execute("INSERT INTO mahasiswaterdaftar(email,nama,nim,prodi,angkatan,files) VALUES(%s,%s,%s,%s,%s,%s)", (email,nama,nim,prodi,angkatan,filename))
        #     mysql.connection.commit()
        #     cur.close()
        #     response = {'success': True, 'message': 'Data berhasil disimpan'}
        #     return jsonify(response)
        # except Exception as e:
        #     response = {'success': False, 'message': str(e)}
        #     return jsonify(response), 500  # Mengembalikan kode status 500 (Internal Server Error) jika terjadi kesalahan
    else:
        response = {'success': False, 'message': 'Missing required data'}
        return jsonify(response), 400  # Mengembalikan kode status 400 (Bad Request) jika data yang diperlukan tidak ditemukan
    
@app.route("/table")
def table():
    return render_template('table.html',menu='table')
@app.route("/generate")
def generate():
    return render_template('generate.html',menu='generate')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')