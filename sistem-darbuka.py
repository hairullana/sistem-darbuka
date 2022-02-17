# LIBRARY
import mysql.connector
import numpy as np
import librosa
import librosa.feature
import math

# TESTING DATASET
jenisNada = ['dum','tak','slap']
jumlahDataLatih = 50

# MFCC
def mfcc_extract(filename):
    # LOAD SONG WITH 44,1K
    y, sr  = librosa.load(filename, sr=44100)
    # SILENCCE REMOVAL
    yt, index = librosa.effects.trim(y, top_db=30)
    # WINDOW WIDTH (OVERLAPPING) = 20ms
    a=int(0.02*sr)
    # FRAME LENGTH = 10ms
    b=int(0.01*sr)
    # EXTRACTION
    mfcc = librosa.feature.mfcc(y=yt, sr=sr, n_mfcc=13,n_fft=a,hop_length=b)
    return mfcc

# SAVE TO DB
def save_to_db(jenisNada,mfcc):
    # DB CONNECTOR
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        database='darbuka'
        )
    
    # QUERY AND PUSH
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data_latih VALUES('','" + jenisNada + "','" + mfcc + "')")
    connection.commit()

# TRAINING
for i in jenisNada :
    for j in range(jumlahDataLatih) :
        filename = 'DataTA/NadaDasar/' + i + '/' + i + str(j+1) + '.wav'
        # EXTRACTION
        mfcc = mfcc_extract(filename)
        # MEAN OF EACH COEFFICIENT
        mfcc2 = np.mean(mfcc, axis=1)
        # CONVERT TO STRING
        mfcc2 = np.array2string(mfcc2)
        # SAVE TO DB
        save_to_db(i, mfcc2)
    print('Training to ' + str(jumlahDataLatih) + ' ' + i + ' tone ...')

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
    # file = filename.split(sep="/")
    # file2 = file[len(file)-1]
    # print('Classifying on ' + file2)
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

#%%
# TESTING DUM
k = 5
print('TESTING ON DUM TONE (K=' + str(k) + ')')
for i in range(20) :
    indeks = i + 51
    filename = 'DataTA/NadaDasar/dum/dum' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = klasifikasi(filename,k)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    print('Result of ' + file2 + ' classification is ' + hasil + ' tone')


# TESTING TAK
print('TESTING ON TAK TONE (K=' + str(k) + ')')
for i in range(20) :
    indeks = i + 51
    filename = 'DataTA/NadaDasar/tak/tak' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = klasifikasi(filename,k)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    print('Result of ' + file2 + ' classification is ' + hasil + ' tone')

# TESTING SLAP
print('TESTING ON SLAP TONE (K=' + str(k) + ')')
for i in range(20) :
    indeks = i + 51
    filename = 'DataTA/NadaDasar/slap/slap' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = klasifikasi(filename,k)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    print('Result of ' + file2 + ' classification is ' + hasil + ' tone')