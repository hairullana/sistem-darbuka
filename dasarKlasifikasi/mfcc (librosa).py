# untuk mfcc nya
import librosa
import librosa.feature
import numpy as np

audio = 'dataset/toneBasic/tak/tak5.wav'
y,_ = librosa.load(audio, sr=44100)
mfcc = librosa.feature.mfcc(y=y, n_mfcc=13)
mfcc_flat = np.mean(mfcc, axis=1)
mfcc_string = np.array2string(mfcc_flat)
print(mfcc)
print("Audio duration: {0}s".format(len(y) / 44100))