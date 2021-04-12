from app.core import Database
from flask import jsonify
from math import ceil
from cryptography.fernet import Fernet


class Akun(Database.Database):

    def __init__(self):
        super().__init__()
        self.__table = "akun"
        self.__select_field = "id, username, nama_lengkap, email"
        self.id = 0
        self.username = ""
        self.password = ""
        self.nama_lengkap = ""
        self.email = ""
        self.limit = 15
        self.page = 1
        self.offset = 0
        self.orderby = "id"
        self.orderdir = "desc"
        self.pass_key = b'uDqEnuVZq5cKxLtzdySYM9l0HlXEmjTA7-RYGsZayuY='

    def __get_total_record(self):
        query = "SELECT * FROM {table}".format(
            table=self.__table
        )
        self.cursor.execute(query)
        return len(self.cursor.fetchall())

    def get_all_akun(self):
        query = "SELECT {select_field} FROM {table} ORDER BY {orderby} {orderdir} LIMIT {limit} OFFSET {offset}".format(
            select_field=self.__select_field,
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

    def get_akun(self, id):
        query = "SELECT {select_field} FROM {table} WHERE id={id}".format(
            select_field=self.__select_field,
            table=self.__table,
            id=id
        )
        self.cursor.execute(query)
        get_query = self.cursor.fetchone()

        return jsonify({
            "result": get_query
        })

    def __encrypt_password(self):
        chiper_suite = Fernet(self.pass_key)
        encode_password = str.encode(self.password)
        chipered_text = chiper_suite.encrypt(b"%s" % encode_password)
        return chipered_text

    def __decrypt_password(self, chipered_password):
        chiper_suite = Fernet(self.pass_key)
        chipered_text = b"%s" % chipered_password.encode()
        unchipered_text = (chiper_suite.decrypt(chipered_text))
        return unchipered_text.decode()

    def insert_akun(self):

        cek_akun = "SELECT * FROM {table} WHERE username=%s".format(
            table=self.__table,
        )
        cek_value = (self.username,)
        self.cursor.execute(cek_akun, cek_value)
        get_akun = len(self.cursor.fetchall())

        # Cek jika akun sudah ada maka return username exists
        if get_akun > 0:
            return jsonify({
                "status": "username_exists"
            })
        # JIka Tidak ada makan akan di insert ke table
        else:
            query = "INSERT INTO {table} (username, password, nama_lengkap, email) VALUES(%s,%s,%s,%s)".format(
                table=self.__table
            )
            value = (self.username, self.__encrypt_password(),
                     self.nama_lengkap, self.email)
            self.cursor.execute(query, value)
            self.db.commit()

            return jsonify({
                "status": self.cursor.rowcount


            })

    def update_akun(self):
        query = "UPDATE {table} SET nama_lengkap=%s, email=%s WHERE id=%s".format(
            table=self.__table
        )
        value = (self.nama_lengkap, self.email, self.id)
        self.cursor.execute(query, value)
        self.db.commit()

        return jsonify({
            "status": self.cursor.rowcount
        })

    def delete_akun(self):
        query = "DELETE FROM {table} WHERE id=%s".format(
            table=self.__table
        )
        value = (self.id,)
        self.cursor.execute(query, value)
        self.db.commit()

        return jsonify({
            "status": self.cursor.rowcount
        })

    def login_akun(self):
        res = {}
        query = "SELECT * FROM {table} WHERE username=%s".format(
            table=self.__table
        )
        value = (self.username,)
        self.cursor.execute(query,value)
        akun_exists = self.cursor.fetchone()

        if akun_exists != None:
            if self.__decrypt_password(akun_exists['password']) == self.password:
                akun_exists.pop("password")
                res['status'] = True
                res['data'] = akun_exists
            else:
                res['status'] = False
                res['error'] = "Wrong password for username %s " % self.username
        else:
            res['status'] = False
            res['error'] = "Username %s not exists" % self.username

        return jsonify(res)


