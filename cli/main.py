from automaticClassificationFunc import basicToneAutomaticIdentification, tonePatternAutomaticIdentification
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
cursor.execute("SELECT * FROM mfcc_parameters WHERE id=1")
data = cursor.fetchone()
frameLength = data[1]
overlap = data[2]
mfccCoefficient = data[3]

for k in [1, 3, 5, 7, 9] :
  dumResult, takResult, slapResult, accuracyResultOfBasicTone = basicToneAutomaticIdentification(frameLength, overlap, mfccCoefficient, k)
  baladiResult, maqsumResult, sayyidiResult, accuracyResultOfTonePattern, dumAccuracyResult, takAccuracyResult = tonePatternAutomaticIdentification(frameLength, overlap, mfccCoefficient, k)

  print(str(frameLength*1000) + ', ' + str(overlap*1000) + ', ' +  str(mfccCoefficient) + ', ' + str(k))
  print(accuracyResultOfBasicTone)
  print(accuracyResultOfTonePattern)
  # print(dumResult)
  # print(takResult)
  # print(slapResult)
  # print(dumAccuracyResult)
  # print(takAccuracyResult)