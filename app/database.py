import mysql.connector

con = mysql.connector.connect(
    host="server.nixmedia.web.id",
    user="python_test",
    password="@pythonTest123",
    database="python_image_gallery"
)

cur = con.cursor(dictionary=True)
