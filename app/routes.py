from flask import jsonify, request, render_template, redirect, url_for
from app import app
from app.controllers import Kategori, Akun, ImageGallery
from flask_cors import CORS
import os

CORS(app)

# Class Instance
kategori = Kategori.Kategori()
akun = Akun.Akun()
image_gallery = ImageGallery.ImageGallery()

# View routes
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/kategori/<int:id>/galeri')
def get_image_gallery_category(id):
    images = image_gallery.get_image_gallery_category(id)
    return render_template('gallery.html', images=images)


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
      return insert_image_gallery()

    return render_template('upload.html')


@app.route("/image_gallery/<int:id>/image", methods=['GET'])
def image():
    return render_template('image.html')


@app.route('/gallery')
def gallery():
    img_names = os.listdir(os.path.join(app.static_folder, "img"))
    print(img_names)
    return render_template('gallery.html', img_names=img_names)


@app.route("/login", methods=['GET'])
def view_login():
    return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def view_register():
    if request.method == 'POST':
        return insert_akun()
    return render_template('register.html')


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
        # return akun.insert_akun()
        return redirect(url_for("index"))


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


@app.route("/login", methods=['POST'])
def login_akun():
    if request.method == 'POST':
        akun.username = request.form['username']
        akun.password = request.form['password']
        return akun.login_akun()

# Image Gallery Route List


@app.route("/image_gallery", methods=['GET'])
def all_image_gallery():
    return image_gallery.get_all_images()


@app.route("/image_gallery/<int:id>", methods=['GET'])
def get_image_gallery(id):
    return image_gallery.get_image_gallery(id)

# @app.route("/upload-image", methods=["GET", "POST"])
# def upload_image():
#     if request.method == "POST":
#         if request.files:
#             image = request.files["image"]
#             print(image)
#             return redirect(request.url)
#     return render_template("upload_image.html")

@app.route("/image_gallery/insert", methods=['POST'])
def insert_image_gallery():
    if request.method == 'POST':
        upload_file = image_gallery.upload_images(request.files)

        if upload_file:
            image_gallery.id_kategori = request.form['id_kategori']
            # image_gallery.id_akun = request.form['id_akun']
            image_gallery.judul = request.form['judul']
            image_gallery.caption = request.form['caption']
            # return image_gallery.insert_images()
            return redirect(url_for("index"))
        else:
            return jsonify({
                "status": False
            })


# @app.route("/image_gallery/update/<int:id>", methods=['PUT'])
# def update_image_gallery(id):
#     if request.method == 'PUT':
#         image_gallery.id = id
#         image_gallery.nama_lengkap = request.form['nama_lengkap']
#         image_gallery.email = request.form['email']
#         return image_gallery.update_image_gallery()


# @app.route("/image_gallery/delete/<int:id>", methods=['DELETE'])
# def delete_image_gallery(id):
#     if request.method == 'DELETE':
#         akun.id = id
#         return akun.delete_akun()
