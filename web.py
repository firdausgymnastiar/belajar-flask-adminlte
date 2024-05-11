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

UPLOAD_FOLDER = 'static/img_register'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

def process_image(file):
    # Membaca file menggunakan OpenCV
    img_np = np.fromstring(file.read(), np.uint8)
    img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    return img_cv


# Face Recognition with DeepFace
def face_processing(img_cv):
    # Path to the pre-trained SSD model
    model_path = "res10_300x300_ssd_iter_140000.caffemodel"
    # Path to the prototxt file of the model
    prototxt_path = "deploy.prototxt.txt"

    # Load pre-trained SSD model
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    # Load image
    # image = cv2.imread(img_cv)  
    image = img_cv  
    

    # Preprocess the image for SSD
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Pass the blob through the network and obtain detections
    net.setInput(blob)
    detections = net.forward()

    # Counter for number of faces detected
    face_count = 0
    confidence_above_099 = 0

    # Loop over the detections
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out detections with confidence below 0.8
        if confidence > 0.8:
            # print(confidence)
            face_count += 1
            if confidence > 0.99:
                confidence_above_099 += 1

    # Display appropriate text based on the number of faces detected and confidence level
    if face_count > 1:
        # response = {'success': False, 'message': 'Lebih dari 1 wajah terdeteksi'}
        # return jsonify(response), 400  #Lebih dari 1 wajah terdeteksi
        return "Lebih dari 1 wajah terdeteksi"
    elif face_count == 1:
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
            if confidence_above_099 == 1:
                # return print("wajah anda belum terdaftar, jika anda merasa sudah terdaftar mohon ulangi dengan gambar yang lebih jelas") #anda belum terdaftar
                return "anda belum terdaftar"
            else:
                return "gambar kurang jelas" #anda belum terdaftar tetapi gambar kurang jelas mohon ulangi
    elif face_count == 0:
        # response = {'success': False, 'message': 'Tidak ada wajah yang terdeteksi'}
        # return jsonify(response), 400  #Tidak ada wajah yang terdeteksi
        return "Tidak ada wajah yang terdeteksi"



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

@app.route("/registerwajah", methods=["POST", "GET"])
def registerwajah():
    try:
        if 'gambarWajah' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'})
        
        email = request.form.get('email')
        nama = request.form.get('nama')
        nim = request.form.get('nim')
        prodi = request.form.get('prodi')
        angkatan = request.form.get('angkatan')
        file = request.files['gambarWajah']
        
        img_np = np.fromstring(file.read(), np.uint8)
        img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        face_verify = face_processing(img_cv)

        if face_verify == "Lebih dari 1 wajah terdeteksi":
            response = {'success': False, 'message': 'Lebih dari 1 wajah terdeteksi'}
            return jsonify(response), 400
        if face_verify == "Tidak ada wajah yang terdeteksi":
            response = {'success': False, 'message': 'Tidak ada wajah yang terdeteksi'}
            return jsonify(response), 400
        if face_verify == "gambar kurang jelas":
            response = {'success': False, 'message': 'gambar kurang jelas'}
            return jsonify(response), 400
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'})
        
        # if face_verify == "anda belum terdaftar":
        #     if email and nama and nim and prodi and angkatan and file and allowed_file(file.filename): 
        #         didaftar
        #     else:
        #         response = {'success': False, 'message': 'Missing required data'}
        #         return jsonify(response), 400  # Mengembalikan kode status 400 (Bad Request) jika data yang diperlukan tidak ditemukan


        if email and nama and nim and prodi and angkatan and file and allowed_file(file.filename) and face_verify:  # Memastikan semua data diterima

            if face_verify == "anda belum terdaftar":
                try:
                    filename = secure_filename(str(nim)) + ".jpg"  # Ganti ekstensi sesuai kebutuhan
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO mahasiswaterdaftar(email,nama,nim,prodi,angkatan,files) VALUES(%s,%s,%s,%s,%s,%s)", (email,nama,nim,prodi,angkatan,filename))
                    mysql.connection.commit()
                    cur.close()

                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Path penyimpanan file
                    with open(file_path, 'wb') as f:  # Mode 'wb' untuk menyimpan dalam mode biner
                        f.write(img_np)  # Menulis konten byte ke file

                    response = {'success': True, 'message': 'Data berhasil disimpan', 'nim': nama}
                    return jsonify(response)
                except:
                    response = {'success': False, 'message': 'gagal pas di mysql'}
                    return jsonify(response), 500  # Mengembalikan kode status 500 (Internal Server Error) jika terjadi kesalahan
            else:
                img_login = face_verify.split('\\')[1]
                try:
                    cur = mysql.connection.cursor()
                    query = "SELECT nim From mahasiswaterdaftar WHERE files LIKE %s"
                    cur.execute(query, (img_login,))
                    # cur.execute("SELECT nama From mahasiswaterdaftar WHERE files LIKE %s", (img_login,))
                    # Mengambil hasil query
                    data = cur.fetchall() #type data tuple
                    cur.close()
                    if data is not None:
                        # namalengkap = str(data[0])
                        # panggilan = namalengkap.split("'")[1]
                        panggilan = data
                        # filename = secure_filename(panggilan + "_login_" + token) + ".jpg"  # Ganti ekstensi sesuai kebutuhan
                        # uploads_folder = os.path.join(os.getcwd(), 'static', 'img_login')
                        # file.save(os.path.join(uploads_folder, filename))
                        response = {'success': False, 'message': 'Sudah terdaftar!', 'nim': panggilan}
                        return jsonify(response)
                    else:
                        response = {'success': False, 'message': 'gada didaftar db!'}
                        return jsonify(response)
                except:
                    response = {'success': False, 'message': 'error setelah face processing'}
                    return jsonify(response), 500

        else:
            response = {'success': False, 'message': 'Missing required data'}
            return jsonify(response), 400  # Mengembalikan kode status 400 (Bad Request) jika data yang diperlukan tidak ditemukan
    except:
        response = {'success': False, 'message': 'form kosong'}
        return jsonify(response), 400
    
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
    try:
        if 'gambarWajah' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'})
        
        token = request.form.get('tokenKelas')
        file = request.files['gambarWajah']

        img_np = np.fromstring(file.read(), np.uint8)
        img_cv = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        face_verify = face_processing(img_cv)
        

        if face_verify == "Lebih dari 1 wajah terdeteksi":
            response = {'success': False, 'message': 'Lebih dari 1 wajah terdeteksi'}
            return jsonify(response), 400
        if face_verify == "Tidak ada wajah yang terdeteksi":
            response = {'success': False, 'message': 'Tidak ada wajah yang terdeteksi'}
            return jsonify(response), 400
        if face_verify == "gambar kurang jelas":
            response = {'success': False, 'message': 'gambar kurang jelas'}
            return jsonify(response), 400
        if face_verify == "anda belum terdaftar":
            response = {'success': False, 'message': 'anda belum terdaftar'}
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
                    filename = secure_filename(str(panggilan) + "_login_" + str(token)) + ".jpg"  # Ganti ekstensi sesuai kebutuhan

                    uploads_folder = os.path.join(os.getcwd(), 'static', 'img_login')
                    # file.save(os.path.join(uploads_folder, filename))

                    file_path = os.path.join(uploads_folder, filename)  # Path penyimpanan file
                    with open(file_path, 'wb') as f:  # Mode 'wb' untuk menyimpan dalam mode biner
                        f.write(img_np)  # Menulis konten byte ke file

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
    except:
        response = {'success': False, 'message': 'form kosong'}
        return jsonify(response), 400   
       
@app.route("/table")
def table():
    return render_template('table.html',menu='table')
@app.route("/generate")
def generate():
    return render_template('generate.html',menu='generate')

@app.route("/generatetoken", methods=["POST", "GET"])
def generatetoken():
    try:
        email = request.form.get('email')
        nama = request.form.get('nama')
        inisial = request.form.get('inisial')
        nip = request.form.get('nip')
        matkul = request.form.get('matkul')
        pertemuan = request.form.get('pertemuan')
        deskripsi = request.form.get('deskripsi')
        token = request.form.get('token')
        
        if email and nama and inisial and nip and matkul and pertemuan and deskripsi and token:
            try:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO data_token(email,nama,inisial,nip,matkul,pertemuan,deskripsi,token) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (email,nama,inisial,nip,matkul,pertemuan,deskripsi,token))
                mysql.connection.commit()
                cur.close()
                response = {'success': True, 'message': 'Data berhasil disimpan', 'nim': token}
                return jsonify(response)
            except:
                response = {'success': False, 'message': 'gagal pas di mysql'}
                return jsonify(response), 500  # Mengembalikan kode status 500 (Internal Server Error) jika terjadi kesalahan
        else:
            response = {'success': False, 'message': 'Missing required data'}
            return jsonify(response), 400
    except:
        response = {'success': False, 'message': 'form kosong'}
        return jsonify(response), 400 
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')