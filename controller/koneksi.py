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
 
def tambah(database,data):
     cur=mysql.connection.cursor()
     cur.execute("INSERT INTO"+database+"(tahun,minat,penjualan,trand) VALUES(%s,%s,%s)",(data[0],data[1],data[2],data[3]))
     mysql.connection.commit()
     cur.close()
     return redirect('/'+database)
def edit(database,dataid):
     cur=mysql.connection.cursor()
     cur.execute("select * from "+database+"where id=%s",(dataid))
     honda=cur.fetchall()
     cur.close()
     return honda
def update(dataset,dataid,data):
      cur=mysql.connection.cursor()
      cur.execute("UPDATE"+database+" SET tahun = %s,minat = %s,penjualan = %s,trand=%s WHERE id = %s;",(data[0],data[1],data[2],data[3],dataid))
      mysql.connection.commit()
      cur.close()
      return redirect('/'+database)