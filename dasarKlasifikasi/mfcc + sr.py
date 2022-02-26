import librosa
import librosa.feature
import numpy as np
import matplotlib.pyplot as plt

def mfcc_extract(filename):
    try:
        y, sr  = librosa.load(filename, sr=44100)
        yt, index = librosa.effects.trim(y, top_db=60)
        # lebar window untuk overlapping = 50% overlapping
        a=int(0.02*sr)
        # panjang frame 1/100 detik
        b=int(0.01*sr)
        mfcc = librosa.feature.mfcc(y=yt, sr=sr, n_mfcc=13,n_fft=a,hop_length=b)
        mfcc0 = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13,n_fft=a,hop_length=b)
        
        sample_rate = 44100

        plt.figure(figsize=(15,4))
        plt.plot(np.linspace(0, len(y) / sample_rate, num=len(y)), y)
        plt.grid(True)
        
        plt.figure(figsize=(15,4))
        plt.plot(np.linspace(0, len(yt) / sample_rate, num=len(yt)), yt)
        plt.grid(True)
        
        print(librosa.get_duration(y), librosa.get_duration(yt))

        return mfcc,a,b,mfcc0
    except:
        return

filename = 'dataset/toneBasic/tak/tak66.wav'
mfcc1,y,z,mfcc0 = mfcc_extract(filename)
mfcc2 = np.mean(mfcc1, axis=1)