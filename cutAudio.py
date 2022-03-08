from pydub import AudioSegment
newAudio = AudioSegment.from_wav("d:/ngoding/sistem darbuka/dataset/tonePattern/baladi2_5.wav")
newAudio = newAudio[1000:2000]
# newAudio.export('newSong.wav', format="wav")