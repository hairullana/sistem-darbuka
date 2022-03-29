from automaticClassificationFunc import basicToneAutomaticIdentification, tonePatternAutomaticIdentification

frameLength = 0.02
hopLength = 0.006
mfccCoefficient = 13
k = 3

dumResult, takResult, slapResult, accuracyResultOfBasicTone = basicToneAutomaticIdentification(frameLength, hopLength, mfccCoefficient, k)
baladiResult, maqsumResult, sayyidiResult, accuracyResultofTonePattern = tonePatternAutomaticIdentification(frameLength, hopLength, mfccCoefficient, k)
  
# print(dumResult)
# print(takResult)
# print(slapResult)
print(accuracyResultOfBasicTone)
# print(baladiResult)
# print(maqsumResult)
# print(sayyidiResult)
print(accuracyResultofTonePattern)