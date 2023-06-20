from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

# Inisialisasi koneksi ke proyek Firebase
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    # Membaca semua data dari koleksi 'users'
    users = db.collection('users').get()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    # Mengambil data dari form
    name = request.form['name']
    email = request.form['email']

    # Membuat data baru
    data = {
        'name': name,
        'email': email
    }

    # Menambahkan data ke koleksi 'users'
    doc_ref = db.collection('users').add(data)
    return 'Data berhasil ditambahkan dengan ID: ' + doc_ref[1].id

@app.route('/update', methods=['POST'])
def update_user():
    # Mengambil data dari form
    doc_id = request.form['doc_id']
    name = request.form['name']
    email = request.form['email']

    # Memperbarui data dalam dokumen dengan ID tertentu
    doc_ref = db.collection('users').document(doc_id)
    doc_ref.update({'name': name, 'email': email})
    return 'Data berhasil diperbarui'

@app.route('/delete', methods=['POST'])
def delete_user():
    # Mengambil data dari form
    doc_id = request.form['doc_id']

    # Menghapus dokumen dengan ID tertentu
    db.collection('users').document(doc_id).delete()
    return 'Data berhasil dihapus'

if __name__ == '__main__':
    app.run()
