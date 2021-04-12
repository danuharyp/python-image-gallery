from flask import jsonify, request
from app import app
from app.controllers import Kategori, Akun

# Class Instance
kategori = Kategori.Kategori()
akun = Akun.Akun()


@app.route("/", methods=['GET'])
def index():
    return jsonify({
        "result": "home rest api"
    })


# Kategori Route List
@app.route("/kategori", methods=['GET'])
def all_kategori():
    return kategori.get_all_kategori()


@app.route("/kategori/<int:id>", methods=['GET'])
def get_kategori(id):
    return kategori.get_kategori(id)


@app.route("/kategori/insert", methods=['POST'])
def insert_kategori():
    if request.method == 'POST':
        kategori.nama_kategori = request.form['nama_kategori']
        return kategori.insert_kategori()


@app.route("/kategori/update/<int:id>", methods=['PUT'])
def update_kategori(id):
    if request.method == 'PUT':
        kategori.id = id
        kategori.nama_kategori = request.form['nama_kategori']
        return kategori.update_kategori()


@app.route("/kategori/delete/<int:id>", methods=['DELETE'])
def delete_kategori(id):
    if request.method == 'DELETE':
        kategori.id = id
        return kategori.delete_kategori()


# Akun Route Lst
@app.route("/akun", methods=['GET'])
def all_akun():
    return akun.get_all_akun()


@app.route("/akun/<int:id>", methods=['GET'])
def get_akun(id):
    return akun.get_akun(id)


@app.route("/akun/insert", methods=['POST'])
def insert_akun():
    if request.method == 'POST':
        akun.username = request.form['username']
        akun.password = request.form['password']
        akun.nama_lengkap = request.form['nama_lengkap']
        akun.email = request.form['email']
        return akun.insert_akun()


@app.route("/akun/update/<int:id>", methods=['PUT'])
def update_akun(id):
    if request.method == 'PUT':
        akun.id = id
        akun.nama_lengkap = request.form['nama_lengkap']
        akun.email = request.form['email']
        return akun.update_akun()


@app.route("/akun/delete/<int:id>", methods=['DELETE'])
def delete_akun(id):
    if request.method == 'DELETE':
        akun.id = id
        return akun.delete_akun()
