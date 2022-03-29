import librosa
import librosa.display
from scipy import signal
# import random
from IPython.display import Audio, IFrame, display

audio,sr = librosa.load('download.wav', mono=True, sr=16000, offset=0, duration=10)

def f_high(y,sr):
  b,a = signal.butter(10, 2000/(sr/2), btype='highpass')
  yf = signal.lfilter(b,a,y)
  return yf

audioClean = f_high(audio, sr)

# librosa.display.waveplot(audio,sr=sr, x_axis='time')
# librosa.display.waveplot(audioClean,sr=sr, x_axis='time')

# display(Audio(audioClean,rate=sr))
print(audioClean)