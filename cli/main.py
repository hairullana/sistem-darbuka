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
hopLength = data[2]
mfccCoefficient = data[3]

k = 9

dumResult, takResult, slapResult, accuracyResultOfBasicTone = basicToneAutomaticIdentification(frameLength, hopLength, mfccCoefficient, k)
baladiResult, maqsumResult, sayyidiResult, accuracyResultofTonePattern = tonePatternAutomaticIdentification(frameLength, hopLength, mfccCoefficient, k)

print(accuracyResultOfBasicTone)
print(accuracyResultofTonePattern)