from flask import jsonify


class Kategori:

    def __init__(self):
        pass

    def kategori_index(self):
        return jsonify({
            "result": "index category"
        })
