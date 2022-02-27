import librosa

x, sr = librosa.load('d:/ngoding/sistem darbuka/dataset/tonePattern/baladi2_1.wav')
onsetDetection = librosa.onset.onset_detect(x, sr=sr, units='time')

BaladiTonePattern = ['dum', 'dum', 'tak', 'dum', 'tak']
i=0
for onset in onsetDetection:
    onsetDetection[i] = int(onset * 100)
    i += 1

print(onsetDetection)