import math
import numpy as np
import mfccFunc
import mysql.connector

# COLLECTING TRAINING DATASET IN DB
connection = mysql.connector.connect(
  user='root',
  password='root',
  host='localhost',
  database='darbuka_tone',
  auth_plugin='mysql_native_password'
)
# TAKE TRAINING DATASET TO ARRAY
cursor = connection.cursor()
cursor.execute("SELECT * FROM dataset")
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
def klasifikasi(filename, k, windowLength, frameLength, mfccTotalFeature) :
  # MFCC
  testing = mfccFunc.mfcc_extract(filename, windowLength, frameLength, mfccTotalFeature)
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