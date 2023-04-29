from ast import dump
import mysql.connector
import pandas as pd
import numpy as np
import datetime
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.ar_model import AutoReg
from keras.models import Sequential
from keras.layers import Dense, LSTM
import json
# %matplotlib inline

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="projek_peramalan_website"
)
mycursor = mydb.cursor()
def moving_avarage(db):
    mycursor.execute("SELECT * FROM `"+db+"` ORDER BY `"+db+"`.`tahun` ASC")

    # Fetch semua data
    data = mycursor.fetchall()

    # Konversi data ke dalam DataFrame pandas
    motor_sales_data = pd.DataFrame(data, columns=['tahun', 'minat', 'trand', 'penjualan','id'])

    # Ubah kolom 'tanggal' menjadi index
    motor_sales_data = motor_sales_data.set_index('tahun')

    # Lihat 5 data teratas
    # print(motor_sales_data.head())
    #
    # plt.figure(figsize=(10, 5))
    # plt.plot(motor_sales_data.index, motor_sales_data['penjualan'])
    # plt.xlabel('Date')
    # plt.ylabel('Sales')
    # plt.title('Motor Sales Data')
    # plt.show()

    motor_sales_data['moving_avg'] = motor_sales_data['penjualan'].rolling(window=3).mean()

    # Melihat 5 data teratas
    # print(motor_sales_data.head())

    motor_sales_data['ma_with_interest_trend'] = motor_sales_data['moving_avg'] * motor_sales_data['minat'] * motor_sales_data['trand']

    # Melihat 5 data teratas
    print(motor_sales_data)
    # def hasil():
    # return motor_sales_data

    # plt.figure(figsize=(10, 5))
    # plt.plot(motor_sales_data.index, motor_sales_data['penjualan'], label='Actual Sales')
    # plt.plot(motor_sales_data.index, motor_sales_data['ma_with_interest_trend'], label='Moving Average with Interest and Trend')
    # plt.xlabel('Date')
    # plt.ylabel('Sales')
    # plt.title('Motor Sales Data with Moving Average, Interest, and Trend')
    # plt.legend()
    # plt.show()

    # Menghitung nilai MSE (Mean Squared Error)
    mse = ((motor_sales_data['penjualan'] - motor_sales_data['ma_with_interest_trend']) ** 2).mean()
    print(f"Mean Squared Error (MSE) : {mse:.2f}")
    return(motor_sales_data)

def auto_regresi(db):
    mycursor.execute("SELECT * FROM `"+db+"` ORDER BY `"+db+"`.`tahun` ASC")

    # Fetch semua data
    data = mycursor.fetchall()

    # Konversi data ke dalam DataFrame pandas
    motor_sales_data = pd.DataFrame(data, columns=['tahun', 'minat', 'trand', 'penjualan','id'])

    # Ubah kolom 'tanggal' menjadi index
    motor_sales_data = motor_sales_data.set_index('tahun')
    print(motor_sales_data.head())

    # plt.figure(figsize=(10, 5))
    # plt.plot(motor_sales_data.index, motor_sales_data['penjualan'])
    # plt.xlabel('Date')
    # plt.ylabel('Sales')
    # plt.title('Motor Sales Data')
    # plt.show()

    train_data = motor_sales_data.iloc[:-12] # menggunakan data sebelum 12 bulan terakhir sebagai data latih
    test_data = motor_sales_data.iloc[-12:] # menggunakan 12 bulan terakhir sebagai data uji

    # Melihat jumlah data latih dan data uji
    print(f"Jumlah data latih : {len(train_data)}")
    print(f"Jumlah data uji : {len(test_data)}")

    model = AutoReg(train_data['penjualan'], lags=3)

    # Latih model
    model_fit = model.fit()
    # print(model_fit.summary())
    # print(model)
    # Gunakan model untuk melakukan prediksi pada data uji
    predictions = model_fit.predict(start=len(train_data), end=len(train_data)+len(test_data)-1)
    #
    # # Tampilkan hasil prediksi
    print(predictions)
    # #
    # # Visualisasikan hasil prediksi dan data uji
    # plt.figure(figsize=(10, 5))
    # plt.plot(test_data.index, test_data['penjualan'], label='data aktual')
    # plt.plot(test_data.index, predictions, label='data prediksi')
    # plt.xlabel('tahun')
    # plt.ylabel('penjualan')
    # plt.title('penjualan motor dengan auto regresi')
    # plt.legend()
    # plt.show()

    # Menghitung nilai MSE (Mean Squared Error)
    # mse = ((motor_sales_data['penjualan'] - motor_sales_data['ma_with_interest_trend']) ** 2).mean()
    # print(f"Mean Squared Error (MSE) : {mse:.2f}")
    return(motor_sales_data)
    
def regresi_linier(db):
    mycursor.execute("SELECT * FROM `"+db+"` ORDER BY `"+db+"`.`tahun` ASC")

    # Fetch semua data
    data = mycursor.fetchall()

    # Konversi data ke dalam DataFrame pandas
    motor_sales_data = pd.DataFrame(data, columns=['tahun', 'penjualan', 'minat', 'trand','id'])

    motor_sales_data['tahun'] = pd.to_datetime(motor_sales_data['tahun'], format='%Y-%m-%d')
    motor_sales_data.set_index('tahun', inplace=True)

    # Hitung jumlah baris data training
    train_size = int(len(motor_sales_data) * 0.8)

    # Pisahkan data training dan testing
    train_data = motor_sales_data[:train_size]
    test_data = motor_sales_data[train_size:]

    # Inisialisasi model regresi linier
    model = LinearRegression()

    # Latih model dengan data training
    model.fit(train_data[['penjualan', 'trand', 'minat']], train_data[['penjualan']])

    # Lakukan prediksi dengan data testing
    test_data['prediksi'] = model.predict(test_data[['penjualan', 'trand', 'minat']])
    # Buat model regresi linier

    # Hitung nilai MSE
    mse = ((test_data['penjualan'] - test_data['prediksi']) ** 2).mean()

    # Hitung nilai RMSE
    rmse = mse ** 0.5

    print('MSE:', mse)
    print('RMSE:', rmse)

    return(test_data['prediksi'])
def sarima(db):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `"+db+"` ORDER BY `"+db+"`.`tahun` ASC")

    # Fetch semua data
    data = mycursor.fetchall()
    # Konversi data ke dalam DataFrame pandas
    motor_sales_data = pd.DataFrame(data, columns=['tahun', 'minat', 'trand', 'penjualan','id'])
    # Ubah kolom 'tanggal' menjadi index
    motor_sales_data = motor_sales_data.set_index('tahun')
    # print(motor_sales_data.head())
    # plt.figure(figsize=(10, 5))
    # plt.plot(motor_sales_data.index, motor_sales_data['penjualan'])
    # plt.xlabel('Date')
    # plt.ylabel('Sales')
    # plt.title('Motor Sales Data')
    # plt.show()

    train_data = motor_sales_data.iloc[:-12] # menggunakan data sebelum 12 bulan terakhir sebagai data latih
    test_data = motor_sales_data.iloc[-12:]

    # Tentukan model SARIMA
    model = SARIMAX(train_data['penjualan'],
                    order=(1,1,1),
                    seasonal_order=(1,1,1,12),
                    trend='c')

    results = model.fit()
    print(results.summary())

    # Lakukan prediksi pada data uji
    predictions = results.predict(start='2024-01-01', end='2024-12-01')
    print(predictions)
    # Visualisasikan hasil prediksi dan data uji
    # plt.figure(figsize=(10, 5))
    # plt.plot(test_data.index, test_data['penjualan'].values, label='Actual')
    # plt.plot(predictions.index, predictions.values, label='Predicted')
    # plt.xlabel('Date')
    # plt.ylabel('Sales')
    # plt.title('SARIMA Prediction')
    # plt.legend()
    # plt.show()

    # Evaluasi model dengan menggunakan mean squared error (MSE)
    # mse = ((predictions - test_data['penjualan'])**2).mean()
    # print(f"Mean Squared Error : {mse}")
    return(predictions)
    
def lstm(db):
    mycursor.execute("SELECT * FROM `"+db+"` ORDER BY `"+db+"`.`tahun` ASC")
    data = mycursor.fetchall()

    # Membuat DataFrame dari data MySQL
    df = pd.DataFrame(data, columns=['tahun', 'minat', 'trand', 'penjualan','id'])

    # Mengubah tipe data kolom 'sales' menjadi float
    df['penjualan'] = df['penjualan'].astype(float)

    # Menormalkan data menggunakan MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['penjualan']])

    # Membuat fungsi untuk membuat dataset dengan time steps
    def create_dataset(data, time_steps=1):
        X_data, Y_data = [], []
        for i in range(len(data)-time_steps):
            X_data.append(data[i:(i+time_steps), 0])
            Y_data.append(data[i+time_steps, 0])
        return np.array(X_data), np.array(Y_data)

    # Membuat dataset untuk training dan testing
    time_steps = 12 # Contoh: menggunakan 12 bulan sebelumnya untuk memprediksi penjualan bulan berikutnya
    data, _ = create_dataset(scaled_data, time_steps)

    # Reshape data agar sesuai dengan format input LSTM
    data = np.reshape(data, (data.shape[0], data.shape[1], 1))

    # Membuat model LSTM
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(time_steps, 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(data, scaled_data[time_steps:], epochs=100, batch_size=16, verbose=2)

    # Menggunakan model untuk memprediksi penjualan kendaraan bermotor selama 3 tahun ke depan
    last_data = scaled_data[-time_steps:]
    future_predictions = []
    for i in range(36): # Memprediksi selama 3 tahun ke depan
        input_data = np.reshape(last_data, (1, time_steps, 1))
        prediction = model.predict(input_data)
        future_predictions.append(prediction[0][0])
        last_data = np.append(last_data[1:], prediction[0][0])

    # Invers scaling untuk mendapatkan hasil yang sebenarnya
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    # Menambahkan nilai tahun ke data prediksi
    last_year = df['tahun'].max()
    future_years = [str(last_year+datetime.timedelta(i+1)) for i in range(len(future_predictions))]
    future_predictions_df = pd.DataFrame(columns=['tahun', 'penjualan'])
    future_predictions_df['tahun'] = future_years
    future_predictions_df['penjualan'] = float('nan')

    for i, prediction in enumerate(future_predictions):
        future_predictions_df.loc[future_predictions_df['tahun']==future_years[i], 'penjualan'] = prediction

    # Gabungkan DataFrame df dengan future_predictions_df
    df = pd.concat([df, future_predictions_df])

    # Cetak DataFrame hasil gabungan
    print(df)
    return(df)



