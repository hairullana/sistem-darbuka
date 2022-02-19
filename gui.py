from tkinter import *
import tkinter.font
import mysql.connector
import numpy as np
import librosa
import librosa.feature
import math

root = Tk()

# set window size
root.geometry("1200x800")
# title
root.title("Sistem Identifikasi Nada Darbuka")

# default value of form
windowLength = 0.02
frameLength = 0.01
mfccTotalFeature = 13
k = 1

# testing dataset
jenisNada = ['dum','tak','slap']
jumlahDataLatih = 50

# MFCC
def mfcc_extract(filename):
  global windowLength, frameLength, mfccTotalFeature
  # LOAD SONG WITH 44,1K
  y, sr  = librosa.load(filename, sr=44100)
  # SILENCE REMOVAL
  yt, index = librosa.effects.trim(y, top_db=30)
  # WINDOW WIDTH (OVERLAPPING) = 20ms
  a=int(windowLength*sr)
  # FRAME LENGTH = 10ms
  b=int(frameLength*sr)
  # EXTRACTION
  mfcc = librosa.feature.mfcc(y=yt, sr=sr, n_mfcc=mfccTotalFeature,n_fft=a,hop_length=b)
  return mfcc

# COLLECTING TRAINING DATASET IN DB
connection = mysql.connector.connect(
  user='root',
  password='',
  host='127.0.0.1',
  database='darbuka'
)
# TAKE TRAINING DATASET TO ARRAY
cursor = connection.cursor()
cursor.execute("SELECT * FROM data_latih")
data = cursor.fetchall()

dum = []
tak = []
slap = []

for x in data:
  if x[1] == 'dum' :
    dum.append(np.fromstring(x[2].strip('[]'),count=13, dtype=float, sep=' '))
  elif x[1] == 'tak' :
    tak.append(np.fromstring(x[2].strip('[]'),count=13, dtype=float, sep=' '))
  elif x[1] == 'slap' :
    slap.append(np.fromstring(x[2].strip('[]'),count=13, dtype=float, sep=' '))

# CLASSIFICATION
def klasifikasi(filename,k) :
  # MFCC
  testing = mfcc_extract(filename)
  # MEAN OF EACH COEFFICIENT
  testing = np.mean(testing, axis=1)
  # CALCULATE DISTANCE
  data_jarak = []
  for nada_dum in dum :
    total = 0
    for i in range(13) :
      total += pow((nada_dum[i] - testing[i]),2)
    euclidean_distance = math.sqrt(total)
    data_jarak.append(euclidean_distance)
  for nada_tak in tak :
    total = 0
    for i in range(13) :
      total += pow((nada_tak[i] - testing[i]),2)
    euclidean_distance = math.sqrt(total)
    data_jarak.append(euclidean_distance)
  for nada_slap  in slap :
    total = 0
    for i in range(13) :
      total += pow((nada_slap[i] - testing[i]),2)
    euclidean_distance = math.sqrt(total)
    data_jarak.append(euclidean_distance)
  
  # KNN
  data_jarak2 = data_jarak
  indeks = []
  for knn in range(k) :
    smallest = 0
    indeks.append(0)
    for i in range(len(data_jarak2)) :
      if i not in indeks and data_jarak2[i] <= data_jarak2[smallest] :
        smallest = i
        indeks[knn] = smallest

  # CHOOSE MOST K
  k_dum = 0
  k_tak = 0
  k_slap = 0
  for i in range(len(indeks)) :
    if indeks[i] < 50 :
      k_dum += 1
    elif indeks[i] < 100 :
      k_tak += 1
    elif indeks[i] < 150 :
      k_slap += 1

  if k_dum > k_tak and k_dum > k_slap :
    hasil = 'DUM'
  elif k_tak > k_dum and k_tak > k_slap :
    hasil = 'TAK'
  elif k_slap > k_dum and k_slap > k_tak :
    hasil = 'SLAP'
  elif k_dum == k_tak :
    hasil = 'DUM / TAK'
  elif k_dum == k_slap :
    hasil = 'DUM / SLAP'
  elif k_tak == k_slap :
    hasil = 'TAK / SLAP'
  else :
    hasil = 'DUM / TAK / SLAP'
      
  return hasil, k_dum, k_tak, k_slap, indeks

def klasifikasiNada():
  global k

  # variabel penampung nilai klasifikasi
  hasilKlasifikasiDum = ""
  hasilKlasifikasiTak = ""
  hasilKlasifikasiSlap = ""
  jumlahKlasifikasiDumBenar = 0
  jumlahKlasifikasiTakBenar = 0
  jumlahKlasifikasiSlapBenar = 0
  jumlahKlasifikasiBenar = 0
  textPresentaseKlasifikasi = ""
  jumlahDataTesting = 0

  # TESTING DUM
  hasilKlasifikasiDum += '\nTESTING ON DUM TONE (K=' + str(k) + ')\n'
  for i in range(20) :
    indeks = i + 51
    filename = 'DataTA/NadaDasar/dum/dum' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = klasifikasi(filename,k)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'DUM':
      jumlahKlasifikasiDumBenar += 1
    hasilKlasifikasiDum += '\nResult of ' + file2 + ' classification is ' + hasil + ' tone'
    jumlahDataTesting += 1

  # TESTING TAK
  hasilKlasifikasiTak += '\nTESTING ON TAK TONE (K=' + str(k) + ')\n'
  for i in range(20) :
    indeks = i + 51
    filename = 'DataTA/NadaDasar/tak/tak' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = klasifikasi(filename,k)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'TAK':
      jumlahKlasifikasiTakBenar += 1
    hasilKlasifikasiTak += '\nResult of ' + file2 + ' classification is ' + hasil + ' tone'
    jumlahDataTesting += 1

  # TESTING SLAP
  hasilKlasifikasiSlap += '\nTESTING ON SLAP TONE (K=' + str(k) + ')\n'
  for i in range(20) :
    indeks = i + 51
    filename = 'DataTA/NadaDasar/slap/slap' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = klasifikasi(filename,k)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'SLAP':
      jumlahKlasifikasiSlapBenar += 1
    hasilKlasifikasiSlap += '\nResult of ' + file2 + ' classification is ' + hasil + ' tone'
    jumlahDataTesting += 1
  
  jumlahKlasifikasiBenar = jumlahKlasifikasiDumBenar + jumlahKlasifikasiTakBenar + jumlahKlasifikasiSlapBenar

  textPresentaseKlasifikasi += "Nada DUM = " + str(jumlahKlasifikasiDumBenar) + "/20 (" + str(jumlahKlasifikasiDumBenar/20*100) + "%)\n"
  textPresentaseKlasifikasi += "Nada TAK = " + str(jumlahKlasifikasiTakBenar) + "/20 (" + str(jumlahKlasifikasiTakBenar/20*100) + "%)\n"
  textPresentaseKlasifikasi += "Nada SLAP = " + str(jumlahKlasifikasiSlapBenar) + "/20 (" + str(jumlahKlasifikasiSlapBenar/20*100) + "%)\n"
  textPresentaseKlasifikasi += "Presentase = " + str(jumlahKlasifikasiBenar) + "/60 (" + str(jumlahKlasifikasiBenar/60*100) + "%)"

  KlasifikasiDum.config(text=hasilKlasifikasiDum)
  KlasifikasiTak.config(text=hasilKlasifikasiTak)
  KlasifikasiSlap.config(text=hasilKlasifikasiSlap)
  presentaseKlasifikasi.config(text=textPresentaseKlasifikasi)

# heading template
h1 = tkinter.font.Font(size=20)
h2 = tkinter.font.Font(size=16)

# title
Label(root, text="SISTEM IDENTIFIKASI NADA DARBUKA", font=h1).grid(row=0, column=0, columnspan=6)

# COLUMN A
# sub title
Label(root, text="Koefisien", font=h2).grid(row=2, column=0, pady=10)
# form
Label(root, text="Panjang Window (detik)").grid(row=3, column=0, pady=5)
windowLengthEntry = Entry(root, width=25, textvariable=StringVar(root, value=windowLength))
windowLengthEntry.grid(row=3, column=1)
Label(root, text="Panjang Frame (detik)").grid(row=4, column=0, pady=5)
frameLengthEntry = Entry(root, width=25, textvariable=StringVar(root, value=frameLength))
frameLengthEntry.grid(row=4, column=1)
Label(root, text="Jumlah Fitur MFCC").grid(row=5, column=0, pady=5)
mfccTotalFeatureEntry = Entry(root, width=25, textvariable=StringVar(root, value=mfccTotalFeature))
mfccTotalFeatureEntry.grid(row=5, column=1)
Label(root, text="Jumlah K").grid(row=6, column=0, pady=5)
kEntry = Entry(root, width=25, textvariable=StringVar(root, value=k))
kEntry.grid(row=6, column=1)
# simpan koefisien
def simpanKoefisien():
  global windowLength, frameLength, mfccTotalFeature, k
  windowLength = float(windowLengthEntry.get())
  frameLength = float(frameLengthEntry.get())
  mfccTotalFeature = int(mfccTotalFeatureEntry.get())
  k = int(kEntry.get())

# button
Button(root, text="simpan", command=simpanKoefisien).grid(row=7, column=0, columnspan=2, pady=5)

# COLUMN B
Button(root, text="klasifikasi", command=klasifikasiNada).grid(row=7, column=3, pady=5)

# Hasil Klasifikasi
KlasifikasiDum = Label(root, text=" ")
KlasifikasiDum.grid(row=9, column=0, columnspan=2, padx=10)
KlasifikasiTak = Label(root, text=" ")
KlasifikasiTak.grid(row=9, column=2, columnspan=2, padx=10)
KlasifikasiSlap = Label(root, text=" ")
KlasifikasiSlap.grid(row=9, column=4, columnspan=2, padx=10)
# Hasil Klasifikasi (Tingkat Akurasi)
presentaseKlasifikasi = Label(root, text=" ")
presentaseKlasifikasi.grid(row=10, column=0, columnspan=6, pady=10)

root.mainloop()