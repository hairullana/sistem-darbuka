import librosa
import speaker_verification_toolkit.tools as svt

data,sr = librosa.load('Data TA/Nada Dasar/dum/dum1.wav')
data = svt.rms_silence_filter(data)
data = svt.extract_mfcc(data)
print('The MFCC Values Are As Follows : \n', data)