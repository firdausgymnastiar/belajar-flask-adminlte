from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskadminlte_db'
mysql = MySQL(app)



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
        return "<h1>Maaf, fitur ini hanya tersedia di perangkat mobile.</h1>"
    # return render_template('register.html',menu='register')

@app.route("/registerwajah", methods=["POST"])
def registerwajah():
    email = request.form.get('emailAddress')
    nama = request.form.get('fullName')
    nim = request.form.get('nim')
    prodi = request.form.get('programStudi')
    angkatan = request.form.get('angkatan')

    if email and nama and nim and prodi and angkatan:  # Memastikan semua data diterima
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO mahasiswaterdaftar(email,nama,nim,prodi,angkatan) VALUES(%s,%s,%s,%s,%s)", (email,nama,nim,prodi,angkatan))
            mysql.connection.commit()
            cur.close()
            response = {'success': True, 'nim': nim}
            return jsonify(response)
        except Exception as e:
            response = {'success': False, 'error_message': str(e)}
            return jsonify(response), 500  # Mengembalikan kode status 500 (Internal Server Error) jika terjadi kesalahan
    else:
        response = {'success': False, 'error_message': 'Missing required data'}
        return jsonify(response), 400  # Mengembalikan kode status 400 (Bad Request) jika data yang diperlukan tidak ditemukan

@app.route("/login")
def login():
    # return render_template('login.html',menu='login')
# Mendeteksi apakah perangkat adalah perangkat mobile
    user_agent = request.headers.get('User-Agent').lower()
    is_mobile = any(mobile in user_agent for mobile in ['iphone', 'android', 'blackberry', 'opera mini', 'windows mobile'])
    
    if is_mobile:
        return render_template('login.html',menu='login')
    else:
        return "<h1>Maaf, fitur ini hanya tersedia di perangkat mobile.</h1>"

# @app.route("/tes", methods=["POST"])
# def ngetes():
#     # if request.method == 'POST':
#     #     # Mengambil data username dari permintaan POST
#     #     username = request.json.get('nim')
        
#     #     # Periksa apakah username sudah ada di database
#     #     cursor = mysql.connection.cursor()
#     #     cursor.execute("SELECT * FROM mahasiswaterdaftar WHERE nim = %s", (username,))
#     #     existing_user = cursor.fetchone()

#     #     if existing_user:
#     #         # Jika username sudah ada, kirim respons dengan pesan error
#     #         response = {'status': 'error', 'message': 'Username already exists in the database'}
#     #         cursor.close()
#     #         return jsonify(response), 400

#     #     # Jika username belum ada, simpan data ke database
#     #     cursor.execute("INSERT INTO mahasiswaterdaftar (nim) VALUES (%s)", (username,))
#     #     mysql.connection.commit()
#     #     cursor.close()

#     #     # Buat respons sukses
#     #     response = {'status': 'success', 'message': 'Username submitted successfully'}

#     #     # Mengirim respons JSON kembali ke klien
#     #     return jsonify(response), 200
#     # else:
#     #     # Jika metode tidak diizinkan, kirim respons JSON dengan status 405 (Method Not Allowed)
#     #     response = {'status': 'error', 'message': 'Method not allowed'}
#     #     return jsonify(response), 405

#     nim = request.form['nim']
#     prodi = request.form['prodi']

#     # Mengambil data pengguna dari database
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM mahasiswaterdaftar WHERE nim = %s", (nim,)) 
#     user = cur.fetchone()
#     cur.close()
#     # if user:
#     #     # Konversi tupel menjadi dictionary
#     #     user_dict = {
#     #     'nim': user[0],
#     #     'prodi': user[1]
#     #     }

#     #     if user and user_dict['prodi'] == prodi:
#     #         # Jika login berhasil, kirim respon JSON
#     #         return jsonify({"success": True})
#     #     else:
#     #         # Jika login gagal, kirim respon JSON dengan pesan kesalahan
#     #         return jsonify({"success": False, "message": "Invalid username or password"})
#     if user and user[1] == prodi:
#     # Jika login berhasil, kirim respon JSON
#         return jsonify({"success": True})
#     else:
#     # Jika login gagal, kirim respon JSON dengan pesan kesalahan yang lebih spesifik
#         return jsonify({"success": False, "message": "Invalid username or prodi"})

@app.route("/table")
def table():
    return render_template('table.html',menu='table')
@app.route("/generate")
def generate():
    return render_template('generate.html',menu='generate')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')