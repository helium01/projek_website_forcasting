from flask import Flask, session, redirect,render_template, request
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projek_peramalan_website'
mysql = MySQL(app)

def data(data):
     per_page = 10
     cur=mysql.connection.cursor()
     cur.execute("select * from "+data)
     honda=cur.fetchall()
     # Hitung jumlah halaman
     total_pages = len(honda) // per_page + 1
      # Tampilkan data pada halaman pertama
     offset = 0
     limit = per_page
     cur.close()
     return honda[offset:limit],total_pages

def data_page(data,page):
     per_page = 10
     cur=mysql.connection.cursor()
     cur.execute("select * from "+data)
     honda=cur.fetchall()
     # Hitung jumlah halaman
     total_pages = len(honda) // per_page + 1
      # Tampilkan data pada halaman pertama
       # Tampilkan data pada halaman yang diminta
     offset = (page - 1) * per_page
     limit = page * per_page
     cur.close()
     return honda[offset:limit],total_pages


def page(data):
    per_page = 10
    page = request.args.get('page', 1, type=int)
    start_index = (page - 1) * per_page
    cur = mysql.cursor()
    cur.execute("SELECT * FROM"+data+" LIMIT %s, %s", (start_index, per_page))
    rows = cur.fetchall()
    cur.close()
    return rows

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
def update(database,dataid,data):
      cur=mysql.connection.cursor()
      cur.execute("UPDATE"+database+" SET tahun = %s,minat = %s,penjualan = %s,trand=%s WHERE id = %s;",(data[0],data[1],data[2],data[3],dataid))
      mysql.connection.commit()
      cur.close()
      return redirect('/'+database)

def loginsession(email,password):
      cur=mysql.connection.cursor()
      cur.execute("select * from user where email=%s",(email,))
      user =cur.fetchone()
      cur.close()
      if user is not None and len(user)>0:
           if bcrypt.hashpw(password,user['password'].encode('utf-8'))==user['password'].encode('utf-8'):
                session['name']=user['nama']
                session['email']=user['email']
                return redirect('/')
           else :
                flask("gagal, email dan password tidak cocok")
                return redirect('/login')
      else:
           return render_template('auth/login.html')
def registersession(name,email,password):
     
      cur=mysql.connection.cursor()
      cur.execute("insert into user (nama,email,password) values (%s,%s,%s)",(name,email,bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())))
      mysql.connection.commit()
      session['name']=name
      session['email']=email
      return reditect('/')
      