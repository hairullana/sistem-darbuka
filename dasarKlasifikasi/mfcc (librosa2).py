import librosa
import librosa.feature

def mfcc_extract(filename):
    try:
        y, sr  = librosa.load(filename, sr=44100)
        # lebar window untuk overlapping
        a=int(0.02*sr)
        # panjang frame 1/100 detik
        b=int(0.01*sr)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13,n_fft=a,hop_length=b)
        return mfcc,a,b
    except:
        return

filename = 'dataset/toneBasic/tak/tak1.wav'
audio, sr  = librosa.load(filename, sr=44100)
x,y,z = mfcc_extract(filename)
print("Audio duration: {0}s".format(len(audio) / 44100))