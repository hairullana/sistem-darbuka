import librosa
from classificationFunc import klasifikasi
from pydub import AudioSegment

filename = 'd:/ngoding/sistem darbuka/dataset/tonePattern/baladi2_1.wav'
windowLength = 0.02
frameLength = 0.01
mfccTotalFeature = 13
x, sr = librosa.load(filename)
# x, index = librosa.effects.trim(x, top_db=30)
onsetDetection = librosa.onset.onset_detect(x, sr=sr, units='time')

print(onsetDetection)

BaladiTonePattern = ['dum', 'dum', 'tak', 'dum', 'tak']
i=0
for onset in onsetDetection:
    newAudio = AudioSegment.from_wav(filename)
    start = int(onsetDetection[i]*1000)
    if i != len(onsetDetection)-1 :
        end = int(onsetDetection[i+1]*1000)
    else :
        end = int(librosa.get_duration(filename=filename)*1000)
    newAudio = newAudio[start:end]
    newAudio.export('temp.wav', format="wav")
    hasil, k_dum, k_tak, k_slap, indeks = klasifikasi('temp.wav', 1, 0.02, 0.01, 13)
    i += 1
    print(hasil)