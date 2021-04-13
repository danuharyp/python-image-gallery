from app.core import Database
from flask import jsonify
from math import ceil
from werkzeug.utils import secure_filename
import os


class ImageGallery(Database.Database):

    def __init__(self):
        super().__init__()
        self.__table = "image_gallery"
        self.id = 0
        self.id_kategori = 0
        self.id_akun = 0
        self.judul = ""
        self.caption = ""
        self.image = ""
        self.limit = 15
        self.page = 1
        self.offset = 0
        self.orderby = "id"
        self.orderdir = "desc"
        self.upload_path = "/images/"

    def __get_total_record(self):
        query = "SELECT * FROM {table}".format(
            table=self.__table
        )
        self.cursor.execute(query)
        return len(self.cursor.fetchall())

    def get_all_images(self):
        query = """
            SELECT 
                {table}.*, kategori.nama_kategori, akun.nama_lengkap
            FROM
                {table} 
            INNER JOIN 
                kategori ON {table}.id_kategori = kategori.id
            INNER JOIN
                akun ON {table.id_akun}.id_akun = akun.id
            ORDER BY 
                {orderby} {orderdir}
            LIMIT {limit} OFFSET {offset}
        """.format(
            table=self.__table,
            orderby=self.orderby,
            orderdir=self.orderdir,
            limit=self.limit,
            offset=self.offset
        )
        self.cursor.execute(query)
        get_query = self.cursor.fetchall()

        return jsonify({
            "result": get_query,
            "total": self.__get_total_record(),
            "lastpage": ceil(self.__get_total_record() / self.limit)
        })

    def get_images(self, id):
        query = """
            SELECT 
                {table}.*, kategori.nama_kategori, akun.nama_lengkap
            FROM
                {table} 
            INNER JOIN 
                kategori ON {table}.id_kategori = kategori.id
            INNER JOIN
                akun ON {table.id_akun}.id_akun = akun.id
            WHERE
                {table}.id = {id}
        """.format(
            table=self.__table,
            orderby=self.orderby,
            orderdir=self.orderdir,
            limit=self.limit,
            offset=self.offset,
            id=id
        )
        self.cursor.execute(query)
        get_query = self.cursor.fetchone()

        return jsonify({
            "result": get_query
        })

    def upload_images(self, files):
        image_file = files['image']
        image_name = secure_filename(image_file.filename)

        image_file.save(os.path.join("images", image_name))
        self.image = image_name
        return True

    def insert_images(self):
        if self.image != None or self.image != "":
            query = """
                INSERT INTO 
                    {table} (id_kategori, id_akun, judul, caption, image) 
                VALUES 
                    (%s, %s, %s, %s, %s)
            """.format(
                table=self.__table
            )
            value = (self.id_kategori, self.id_akun,
                     self.judul, self.caption, self.image)
            self.cursor.execute(query, value)
            self.db.commit()

            return jsonify({
                "status": self.cursor.rowcount
            })

    def update_image(self):
        query = """
            UPDATE 
                {table}
            SET
                id_kategori=%s, judul=%s, caption=%s
            WHERE
                id=%s
        """.format(
            table=self.__table
        )
        value = (self.id_kategori, self.judul, self.caption, self.id)
        self.cursor.execute(query, value)
        self.db.commit()

        return jsonify({
            "status": self.cursor.rowcount
        })

    def delete_image(self):
        query = """
            DELETE FROM {table} WHERE id = %s
        """.format(
            table=self.__table
        )
        value = (self.id,)
        self.cursor.execute(query, value)
        self.db.commit()

        return jsonify({
            "status": self.cursor.rowcount
        })
