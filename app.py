from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'mydatabase'
mysql = MySQL(app)

from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from controller import koneksi

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projek_peramalan_website'
mysql = MySQL(app)
# routing view 
@app.route('/')
def main():
    return render_template('index.html')
@app.route('/honda')
def honda():
    hasil=koneksi.data('honda')
    return render_template('honda/honda.html',data=hasil)
@app.route('/kawasaki')
def kawasaki():
    hasil=koneksi.data('kawasaki')
    return render_template('kawasaki/kawasaki.html',data=hasil)
@app.route('/suzuki')
def suzuki():
    hasil=koneksi.data('suzuki')
    return render_template('suzuki/suzuki.html',data=hasil)
@app.route('/yamaha')
def yamaha():
    hasil=koneksi.data('yamaha')
    return render_template('yamaha/yamaha.html',data=hasil)

# roating tambah
@app.route('/kawasaki_tambah')
def kawasaki_tambah():
    return render_template('kawasaki/tambah.html')
@app.route('/suzuki_tambah')
def suzuki_tambah():
    return render_template('suzuki/tambah.html')
@app.route('/honda_tambah')
def honda_tambah():
    return render_template('honda/tambah.html')
@app.route('/yamaha_tambah')
def yamaha_tambah():
    return render_template('yamaha/tambah.html')
if __name__=="__main__":
    app.run(debug=True)
