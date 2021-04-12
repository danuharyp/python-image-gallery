from app.core import Database
from flask import jsonify
from math import ceil


class Kategori(Database.Database):

    def __init__(self):
        super().__init__()
        self.__table = "kategori"
        self.id = 0
        self.nama_kategori = ""
        self.limit = 15
        self.page = 1
        self.offset = 0
        self.orderby = "id"
        self.orderdir = "desc"

    def __get_total_record(self):
        query = "SELECT * FROM kategori".format(
            table=self.__table
        )
        self.cursor.execute(query)
        return len(self.cursor.fetchall())

    def get_all_kategori(self):
        query = "SELECT * FROM {table} ORDER BY {orderby} {orderdir} LIMIT {limit} OFFSET {offset}".format(
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

    def get_kategori(self, id):
        query = "SELECT * FROM {table} WHERE id={id}".format(
            table=self.__table,
            id=id
        )
        self.cursor.execute(query)
        get_query = self.cursor.fetchone()

        return jsonify({
            "result": get_query
        })

    def insert_kategori(self):
        query = "INSERT INTO {table} (nama_kategori) VALUES(%s)".format(
            table=self.__table
        )
        value = (self.nama_kategori,)
        self.cursor.execute(query, value)
        self.db.commit()

        return jsonify({
            "status": self.cursor.rowcount
        })

    def update_kategori(self):
        query = "UPDATE {table} SET nama_kategori=%s WHERE id=%s".format(
            table=self.__table
        )
        value = (self.nama_kategori, self.id)
        self.cursor.execute(query, value)
        self.db.commit()

        return jsonify({
            "status": self.cursor.rowcount
        })

    def delete_kategori(self):
        query = "DELETE FROM {table} WHERE id=%s".format(
            table=self.__table
        )
        value = (self.id,)
        self.cursor.execute(query, value)
        self.db.commit()

        return jsonify({
            "status": self.cursor.rowcount
        })
