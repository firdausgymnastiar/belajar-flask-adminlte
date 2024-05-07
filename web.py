from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
from deepface import DeepFace
import cv2
import numpy as np
import mysql.connector



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskadminlte_db'
mysql = MySQL(app)

app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

def process_image(file):
    # Membaca file menggunakan OpenCV
    img_np = np.fromstring(file.read(), np.uint8)
    img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    return img_cv


# Face Recognition with DeepFace
def faceRecogniton(img_cv):
    try:
        # folder_img = os.path.join(os.getcwd(), 'static', 'img_register')
        folder_img = "static/img_register"

        dfs = DeepFace.find(img_path=img_cv, db_path=folder_img)
        
        # Mengakses DataFrame pada indeks 0 dari list_of_dfs
        df_at_index_0 = dfs[0]
        # Temukan nilai minimum dari kolom 'distance' dalam DataFrame pada indeks 0
        min_distance = df_at_index_0['distance'].min()
        # Temukan baris dengan nilai minimum dalam kolom 'distance'
        row_with_min_distance = df_at_index_0.loc[df_at_index_0['distance'] == min_distance]
        # Ambil nilai dari kolom 'identity' pada baris tersebut
        identity_of_min_distance = row_with_min_distance['identity'].values[0]
        return identity_of_min_distance
    except:
        response = 404
        return response



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
        filename = secure_filename(nim) + ".jpg"  # Ganti ekstensi sesuai kebutuhan
        uploads_folder = os.path.join(os.getcwd(), 'static', 'img_register')
        file.save(os.path.join(uploads_folder, filename))

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
    # return render_template('login.html',menu='login')
    
@app.route("/loginkelas", methods=["POST", "GET"])
def loginkelas():
    if 'gambarWajah' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})
    
    token = request.form.get('tokenKelas')
    file = request.files['gambarWajah']

    img_np = np.fromstring(file.read(), np.uint8)
    img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    face_verify = faceRecogniton(img_cv)
    

    if isinstance(face_verify, int):
        response = {'success': False, 'message': 'gada wajahnya'}
        return jsonify(response), 400


    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})
    
    if token and file and allowed_file(file.filename) and face_verify:  # Memastikan semua data diterima
        
        # img_login = face_verify.replace('static/img_register\\', '').replace('.jpg', '')
        img_login = face_verify.split('\\')[1]

        try:
            cur = mysql.connection.cursor()
            query = "SELECT nama From mahasiswaterdaftar WHERE files LIKE %s"
            cur.execute(query, (img_login,))
            # cur.execute("SELECT nama From mahasiswaterdaftar WHERE files LIKE %s", (img_login,))
            # Mengambil hasil query
            data = cur.fetchall() #type data tuple
            cur.close()
            if data is not None:
                namalengkap = str(data[0])
                panggilan = namalengkap.split("'")[1]
                filename = secure_filename(namalengkap + "_login_" + token) + ".jpg"  # Ganti ekstensi sesuai kebutuhan
                uploads_folder = os.path.join(os.getcwd(), 'static', 'img_login')
                file.save(os.path.join(uploads_folder, filename))
                response = {'success': True, 'message': 'Selamat Datang!', 'nim': panggilan}
                return jsonify(response)
            else:
                response = {'success': False, 'message': 'gada didaftar db!'}
                return jsonify(response)
        except Exception as e:
            response = {'success': False, 'message': str(e)}
            return jsonify(response), 500
        # except:
        #     response = {'success': False, 'message': 'salah di mysql'}
        #     return jsonify(response), 500



        # if img_login == nim:
        #     filename = secure_filename(nim + "_login_" + token) + ".jpg"  # Ganti ekstensi sesuai kebutuhan
        #     uploads_folder = os.path.join(os.getcwd(), 'static', 'img_login')
        #     file.save(os.path.join(uploads_folder, filename))
        #     response = {'success': True, 'message': 'Selamat Datang!', 'nim': nim}
        #     return jsonify(response)
        # if img_login != nim:
        #     response = {'success': False, 'message': 'Nim anda salah!'}
        #     return jsonify(response)


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