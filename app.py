import json
from flask import Flask, render_template, request,session, redirect,jsonify, redirect
from flask_mysqldb import MySQL
from controller import koneksi, peramalan
import bcrypt

app = Flask(__name__)
app.secret_key="forcasting"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projek_peramalan_website'
mysql = MySQL(app)

# route login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password'].encode('utf-8')
        cur=mysql.connection.cursor()
        cur.execute("select * from user where email=%s",(email,))
        user =cur.fetchone()
        cur.close()
        if user is not None and len(user)>0:
           if bcrypt.hashpw(password,user[2].encode('utf-8'))==user[2].encode('utf-8'):
                session['name']=user[0]
                session['email']=user[1]
                return redirect('/')
           else :
                Flask("gagal, email dan password tidak cocok")
                return redirect('/login')
        else:
           return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form['email']
        nama=request.form['nama']
        password=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("select * from user where email=%s",(email,))
        user =cur.fetchone()
        cur.close()
        if  len(user) >0:
            Flask("email sudah di pakai")
            return redirect('/register')
        cur=mysql.connection.cursor()
        cur.execute("insert into user (nama,email,password) values (%s,%s,%s)",(name,email,bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())))
        mysql.connection.commit()
        session['name']=nama
        session['email']=email
        return redirect('/')
    else:
     return render_template('auth/register.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# routing view 
@app.route('/')
def main():
    if 'email' in session:
        return render_template('index.html')
    else :
        return render_template('auth/login.html')
@app.route('/honda')
def honda():
    if 'email' in session:
        hasil=koneksi.data('honda')[0]
        return render_template('honda/honda.html',data=hasil,page_awal=1,total_page=koneksi.data('honda')[1])
    else :
        return render_template('auth/login.html')

@app.route('/kawasaki')
def kawasaki():
    if 'email' in session:
        hasil=koneksi.data('kawasaki')[0]
        return render_template('kawasaki/kawasaki.html',data=hasil,page_awal=1,total_page=koneksi.data('kawasaki')[1])
    else :
        return render_template('auth/login.html')
@app.route('/suzuki')
def suzuki():
    if 'email' in session:
        hasil=koneksi.data('suzuki')[0]
        return render_template('suzuki/suzuki.html',data=hasil,page_awal=1,total_page=koneksi.data('suzuki')[1])
    else :
        return render_template('auth/login.html')
@app.route('/yamaha')
def yamaha():
    if 'email' in session:
        hasil=koneksi.data('yamaha')[0]
        return render_template('yamaha/yamaha.html',data=hasil,page_awal=1,total_page=koneksi.data('yamaha')[1])
    else :
        return render_template('auth/login.html')

# roating tambah
@app.route('/kawasaki_tambah', methods=['GET', 'POST'])
def kawasaki_tambah():
    if 'email' in session:
        if request.method=='GET':
            return render_template('kawasaki/tambah.html')
        else:
            tahun=request.form['tahun']
            minat=request.form['minat']
            penjualan=request.form['penjualan']
            trand=request.form['trand']
            data=[tahun,minat,penjualan,trand]
            koneksi.tambah('honda',data)
    else :
        return render_template('auth/login.html')
    
@app.route('/suzuki_tambah', methods=['GET', 'POST'])
def suzuki_tambah():
    if 'email' in session:
        if request.method=='GET':
            return render_template('suzuki/tambah.html')
        else:
            tahun=request.form['tahun']
            minat=request.form['minat']
            penjualan=request.form['penjualan']
            trand=request.form['trand']
            data=[tahun,minat,penjualan,trand]
            koneksi.tambah('honda',data)
    else :
        return render_template('auth/login.html')
@app.route('/honda_tambah', methods=['GET', 'POST'])
def honda_tambah():
    if 'email' in session:
        if request.method=='GET':
            return render_template('honda/tambah.html')
        else:
            tahun=request.form['tahun']
            minat=request.form['minat']
            penjualan=request.form['penjualan']
            trand=request.form['trand']
            data=[tahun,minat,penjualan,trand]
            koneksi.tambah('honda',data)
    else :
        return render_template('auth/login.html')

@app.route('/yamaha_tambah', methods=['GET', 'POST'])
def yamaha_tambah():
    if 'email' in session:
        if request.method=='GET':
            return render_template('yamaha/tambah.html')
        else:
            tahun=request.form['tahun']
            minat=request.form['minat']
            penjualan=request.form['penjualan']
            trand=request.form['trand']
            data=[tahun,minat,penjualan,trand]
            koneksi.tambah('honda',data)
    else :
        return render_template('auth/login.html')

# route view page 
@app.route('/page/<int:page>/honda')
def honda_page(page):
    if 'email' in session:
        hasil=koneksi.data_page('honda',page)[0]
        return render_template('honda/honda.html',data=hasil,page_awal=page,total_page=koneksi.data_page('honda',page)[1])
    else :
        return render_template('auth/login.html')
@app.route('/page/<int:page>/kawasaki')
def kawasaki_page(page):
    if 'email' in session:
        hasil=koneksi.data_page('kawasaki',page)[0]
        return render_template('kawasaki/kawasaki.html',data=hasil,page_awal=page,total_page=koneksi.data_page('kawasaki',page)[1])
    else :
        return render_template('auth/login.html')
@app.route('/page/<int:page>/suzuki')
def suzuki_page(page):
    if 'email' in session:
        hasil=koneksi.data_page('suzuki',page)[0]
        return render_template('suzuki/suzuki.html',data=hasil,page_awal=page,total_page=koneksi.data_page('suzuki',page)[1])
    else :
        return render_template('auth/login.html')
@app.route('/page/<int:page>/yamaha')
def yamaha_page(page):
    if 'email' in session:
        hasil=koneksi.data_page('yamaha',page)[0]
        return render_template('yamaha/yamaha.html',data=hasil,page_awal=page,total_page=koneksi.data_page('yamaha',page)[1])
    else :
        return render_template('auth/login.html')

# route peramalan sarima
@app.route('/rsarima_honda')
def sarima_honda():
    data=peramalan.sarima(db="honda")
    return jsonify(data.tolist(),data.index.tolist())
@app.route('/rsarima_kawasaki')
def sarima_kawasaki():
    data=peramalan.sarima(db="kawasaki")
    return jsonify(data.tolist(),data.index.tolist())
@app.route('/rsarima_suzuki')
def sarima_suzuki():
    data=peramalan.sarima(db="suzuki")
    return jsonify(data.tolist(),data.index.tolist())
@app.route('/rsarima_yamaha')
def sarima_yamaha():
    data=peramalan.sarima(db="yamaha")
    return jsonify(data.tolist(),data.index.tolist())

# route peramalan regresi linier
@app.route('/rrlinier_honda')
def linier_honda():
    data=peramalan.regresi_linier(db="honda")
    return jsonify(data.tolist(),data.index.tolist())
@app.route('/rrlinier_kawasaki')
def linier_kawasaki():
    data=peramalan.regresi_linier(db="kawasaki")
    return jsonify(data.tolist(),data.index.tolist())
@app.route('/rrlinier_suzuki')
def linier_suzuki():
    data=peramalan.regresi_linier(db="suzuki")
    return jsonify(data.tolist(),data.index.tolist())
@app.route('/rrlinier_yamaha')
def linier_yamaha():
    data=peramalan.regresi_linier(db="yamaha")
    return jsonify(data.tolist(),data.index.tolist())

# route prtamalan moving avarage
@app.route('/rmoving_honda')
def moving_honda():
    data=peramalan.moving_avarage(db="honda")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())
@app.route('/rmoving_kawasaki')
def moving_kawasaki():
    data=peramalan.moving_avarage(db="kawasaki")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())
@app.route('/rmoving_suzuki')
def moving_suzuki():
    data=peramalan.moving_avarage(db="suzuki")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())
@app.route('/rmoving_yamaha')
def moving_yamaha():
    data=peramalan.moving_avarage(db="yamaha")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())

# route auto regresi
@app.route('/rrauto_honda')
def autor_honda():
    data=peramalan.auto_regresi(db="honda")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())
@app.route('/rrauto_kawasaki')
def autor_kawasaki():
    data=peramalan.auto_regresi(db="kawasaki")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())
@app.route('/rrauto_suzuki')
def autor_suzuki():
    data=peramalan.auto_regresi(db="suzuki")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())
@app.route('/rrauto_yamaha')
def autor_yamaha():
    data=peramalan.auto_regresi(db="yamaha")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())

# route metode lstm
@app.route('/rlstm_honda')
def lstm_honda():
    data=peramalan.lstm(db="honda")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())
@app.route('/rlstm_kawasaki')
def lstm_kawasaki():
    data=peramalan.lstm(db="kawasaki")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())
@app.route('/rlstm_suzuki')
def lstm_suzuki():
    data=peramalan.lstm(db="suzuki")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())
@app.route('/rlstm_yamaha')
def lstm_yamaha():
    data=peramalan.lstm(db="yamaha")
    return jsonify(data.index.tolist(),data.moving_avg.tolist())


if __name__=="__main__":
    app.run(debug=True)
