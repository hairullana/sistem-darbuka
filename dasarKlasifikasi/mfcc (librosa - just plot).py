import os
import numpy as np
import scipy
from scipy.io import wavfile
import scipy.fftpack as fft
from scipy.signal import get_window
import IPython.display as ipd
import matplotlib.pyplot as plt

# %matplotlib inline
# TRAIN_PATH = '../input/audio_train/'
ipd.Audio("dum1.wav")

sample_rate, audio = wavfile.read("dum1.wav")
print("Sample rate: {0}Hz".format(sample_rate))
print("Audio duration: {0}s".format(len(audio) / sample_rate))

def normalize_audio(audio):
    audio = audio / np.max(np.abs(audio))
    return audio

audio = normalize_audio(audio)
plt.figure(figsize=(15,4))
plt.plot(np.linspace(0, len(audio) / sample_rate, num=len(audio)), audio)
plt.grid(True)