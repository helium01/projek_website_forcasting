from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projek_peramalan_website'
mysql = MySQL(app)

def data(data):
     cur=mysql.connection.cursor()
     cur.execute("select * from "+data)
     honda=cur.fetchall()
     cur.close()
     return honda
 
def tambah(data):
    return 0