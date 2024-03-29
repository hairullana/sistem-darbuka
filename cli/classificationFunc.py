import os
import math
import numpy as np
from mfccFunc import mfcc_extract
import librosa
from pydub import AudioSegment
import mysql.connector

# COLLECTING TRAINING DATASET IN DB
connection = mysql.connector.connect(
  user='root',
  password='',
  host='127.0.0.1',
  database='darbuka_tone'
)
# TAKE TRAINING DATASET TO ARRAY
cursor = connection.cursor()
cursor.execute("SELECT * FROM dataset")
data = cursor.fetchall()

# print(data)

dum = []
tak = []
slap = []

for x in data:
  dataExtraction = x[2]
  if x[1] == 'dum' :
    dum.append(np.fromstring(dataExtraction.strip('[]'), dtype=float, sep=' '))
  elif x[1] == 'tak' :
    tak.append(np.fromstring(dataExtraction.strip('[]'), dtype=float, sep=' '))
  elif x[1] == 'slap' :
    slap.append(np.fromstring(dataExtraction.strip('[]'), dtype=float, sep=' '))

# CLASSIFICATION
def basicToneIdentification(filename, k, frameLength, overlap, mfccTotalFeature) :
  # print(filename)
  # MFCC
  testing = mfcc_extract(filename, frameLength, overlap, mfccTotalFeature)
  # MEAN OF EACH COEFFICIENT
  testing = np.mean(testing, axis=1)
  # CALCULATE DISTANCE
  data_jarak = []
  for nada_dum in dum :
    total = 0
    for i in range(mfccTotalFeature) :
      total += pow((nada_dum[i] - testing[i]),2)
    euclidean_distance = math.sqrt(total)
    data_jarak.append(euclidean_distance)
  for nada_tak in tak :
    total = 0
    for i in range(mfccTotalFeature) :
      total += pow((nada_tak[i] - testing[i]),2)
    euclidean_distance = math.sqrt(total)
    data_jarak.append(euclidean_distance)
  for nada_slap  in slap :
    total = 0
    for i in range(mfccTotalFeature) :
      total += pow((nada_slap[i] - testing[i]),2)
    euclidean_distance = math.sqrt(total)
    data_jarak.append(euclidean_distance)
  
  # print(len(data_jarak))
  
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
    result = 'DUM'
  elif k_tak > k_dum and k_tak > k_slap :
    result = 'TAK'
  elif k_slap > k_dum and k_slap > k_tak :
    result = 'SLAP'
  elif k_dum == k_tak :
    result = 'DUM / TAK'
  elif k_dum == k_slap :
    result = 'DUM / SLAP'
  elif k_tak == k_slap :
    result = 'TAK / SLAP'
  else :
    result = 'DUM / TAK / SLAP'
  
  # print(k_dum)
  # print(k_tak)
  # print(k_slap)
  return result

def tonePatternIdentification(filename, k, frameLength, overlap, mfccCoefficient):
  x, sr = librosa.load(filename, sr=44100)
  onsetDetection = librosa.onset.onset_detect(x, sr=sr, units='time')
  while len(onsetDetection) > 5 :
    onsetDetection = np.delete(onsetDetection, 0)
  toneDetect = []
  j=1

  for onset in onsetDetection:
    newAudio = AudioSegment.from_wav(filename)
    start = int(onset*1000)
    if j != len(onsetDetection) :
        end = int(onsetDetection[j]*1000)
    else :
        end = int(librosa.get_duration(filename=filename)*1000)
    newAudio = newAudio[start:end]
    newAudio.export('temp.wav', format="wav")
    result = basicToneIdentification('temp.wav', k, frameLength, overlap, mfccCoefficient)

    toneDetect.append(result)
    
    j += 1

  os.remove('temp.wav')
  return toneDetect