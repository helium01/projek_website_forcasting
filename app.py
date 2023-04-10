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
@app.route('/kawasaki_tambah', methods=['GET', 'POST'])
def kawasaki_tambah():
    if request.method=='GET':
        return render_template('kawasaki/tambah.html')
    else:
        tahun=request.form['tahun']
        minat=request.form['minat']
        penjualan=request.form['penjualan']
        trand=request.form['trand']
        data=[tahun,minat,penjualan,trand]
        koneksi.tambah('honda',data)
    
@app.route('/suzuki_tambah', methods=['GET', 'POST'])
def suzuki_tambah():
    if request.method=='GET':
        return render_template('suzuki/tambah.html')
    else:
        tahun=request.form['tahun']
        minat=request.form['minat']
        penjualan=request.form['penjualan']
        trand=request.form['trand']
        data=[tahun,minat,penjualan,trand]
        koneksi.tambah('honda',data)
@app.route('/honda_tambah', methods=['GET', 'POST'])
def honda_tambah():
    if request.method=='GET':
        return render_template('honda/tambah.html')
    else:
        tahun=request.form['tahun']
        minat=request.form['minat']
        penjualan=request.form['penjualan']
        trand=request.form['trand']
        data=[tahun,minat,penjualan,trand]
        koneksi.tambah('honda',data)
@app.route('/yamaha_tambah', methods=['GET', 'POST'])
def yamaha_tambah():
    if request.method=='GET':
        return render_template('yamaha/tambah.html')
    else:
        tahun=request.form['tahun']
        minat=request.form['minat']
        penjualan=request.form['penjualan']
        trand=request.form['trand']
        data=[tahun,minat,penjualan,trand]
        koneksi.tambah('honda',data)
if __name__=="__main__":
    app.run(debug=True)
