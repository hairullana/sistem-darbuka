import mysql.connector
import mfccFunc
import numpy as np

def trainingData(windowLength, frameLength, mfccCoefficients, info):
  infoText = ""

  # DB CONNECTOR
  connection = mysql.connector.connect(
    user='root',
    password='',
    host='127.0.0.1',
    database='darbuka_tone'
  )
  cursor = connection.cursor()

  # QUERY AND PUSH
  cursor.execute("DELETE FROM dataset")
  connection.commit()

  def save_to_db(jenisNada,mfcc):
    # QUERY AND PUSH
    cursor.execute("INSERT INTO dataset VALUES('','" + jenisNada + "','" + mfcc + "')")
    connection.commit()
  
  # testing dataset
  jenisNada = ['dum','tak','slap']
  jumlahDataLatih = 50
  
  # TRAINING
  for i in jenisNada :
    for j in range(jumlahDataLatih) :
      filename = 'D:/Ngoding/darbukaToneClassification/static/dataset/toneBasic/' + i + '/' + i + str(j+1) + '.wav'
      # EXTRACTION
      mfccResult = mfccFunc.mfcc_extract(filename, windowLength, frameLength, mfccCoefficients)
      # MEAN OF EACH COEFFICIENT
      mfccResult2 = np.mean(mfccResult, axis=1)
      # CONVERT TO STRING
      mfccResult2 = np.array2string(mfccResult2)
      # SAVE TO DB
      save_to_db(i, mfccResult2)
    infoText += 'Sedang melakukan ekstraksi pada nada' + ' i sebanyak ' + str(jumlahDataLatih) + ' nada ...\n'
    info.config(text=infoText)