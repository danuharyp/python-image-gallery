from flask import jsonify
from app import app
from app.controllers import Kategori

# Class Instance
kategori = Kategori.Kategori()


@app.route("/")
def index():
    return jsonify({
        "result": "home rest api"
    })


@app.route("/kategori")
def kategori_index():
    return kategori.kategori_index()
