import librosa
import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

# Load some audio
y, sr = librosa.load('dataset/toneBasic/dum/dum5.wav')
# Trim the beginning and ending silence
yt, index = librosa.effects.trim(y, top_db=40)
# Print the durations
print(librosa.get_duration(y), librosa.get_duration(yt))

scaled = np.int16(yt/np.max(np.abs(yt)) * 32767)
write('test.wav', 44100, scaled)

sample_rate = 44100

plt.figure(figsize=(15,4))
plt.plot(np.linspace(0, len(y) / sample_rate, num=len(y)), y)
plt.grid(True)

plt.figure(figsize=(15,4))
plt.plot(np.linspace(0, len(yt) / sample_rate, num=len(yt)), yt)
plt.grid(True)