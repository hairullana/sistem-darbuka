# untuk mfcc nya
import librosa
import librosa.feature
import librosa.display
# ambil data musik
import glob
# memplot
import matplotlib.pyplot as plt
# untuk array
import numpy as np
# pengembangan dari tensorflow, lebih ringan
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils.np_utils import to_categorical
#%%
def display_mfcc(song):
    # melakukan pembacaan lagu
    y, _ = librosa.load(song)
    # melakukan mfcc, vektorisasi lagu
    mfcc = librosa.feature.mfcc(y)
    
    # menampilkan figure
    plt.figure(figsize=(10,4))
    librosa.display.specshow(mfcc, x_axis='time', y_axis='mel')
    plt.colorbar()
    plt.title(song)
    plt.tight_layout()
    plt.show()
#%%
display_mfcc('DataTA/NadaDasar/tak/tak1.wav')
#%%
# fitur ekstraksi
def extract_features_song(f):
    y, _ = librosa.load(f)
    
# silence removal
#    y, index = librosa.effects.trim(y, top_db=40)
#     get mfcc
    mfcc = librosa.feature.mfcc(y=y, n_mfcc=13)
#     normalize values between -1,1 (divide by max)
#    mfcc /= np.amax(np.absolute(mfcc))

#     1000 row data pertama dari vektorisasi vektor pertama
    return np.ndarray.flatten(mfcc)[:1000]
#    return mfcc
#%%
def generate_features_and_labels():
    all_features = []
    all_labels = []
    nada_dasar = ['dum','tak']
#     looping per folder
    for nada in nada_dasar :
#         masukkan semua nada ke sound_files
        sound_files = glob.glob('DataTA/NadaDasar/' + nada + '/*.wav')
        print('Processing %d songs in %s nada...' % (len(sound_files), nada))
#         tiap sound_files akan di ekstraksi
        for f in sound_files:
              features = extract_features_song(f)
#             semua fitur masukkan ke all_features
#             append = stack
              all_features.append(features)
#             semua label masukkan ke all_labels
              all_labels.append(nada)
    label_uniq_ids, label_row_ids = np.unique(all_labels, return_inverse=True)
    label_row_ids = label_row_ids.astype(np.int32, copy=False)
    onehot_labels = to_categorical(label_row_ids, len(label_uniq_ids))
    return np.stack(all_features), onehot_labels
#%%
# passing parameter dari fitur ekstraksi menggunakan mfcc
features, labels = generate_features_and_labels()
#%%
print(features)

#%%
# fitur ekstraksi
print(np.shape(features))
print(np.shape(labels))
#%%
# menentukan jumlah training 80%
training_split = 0.8
#%%
# menumpuk / menggabung features dan labels
alldata = np.column_stack((features, labels))
#%%
# memisahkan data training dan testing
np.random.shuffle(alldata)
splitidx = int(len(alldata) * training_split)
train, test = alldata[:splitidx,:], alldata[splitidx:,:]
#%%
print(np.shape(train))
print(np.shape(test))
#%%
print(np.shape(train))
print(np.shape(test))
#%%
train_input = train[:,:-10]
train_labels = train[:,-10:]
#%%
test_input = test[:,:-10]
test_labels = test[:,-10:]
#%%
print(np.shape(train_input))
print(np.shape(train_labels))
#%%
# membuat seq NN, layer pertama dense dari 100 neurons
model = Sequential([
#     neuron awal 100 bulatan
    Dense(100, input_dim=np.shape(train_input)[1]),
#     aktivasi menggunakan fungsi relu (relu cari di google)
    Activation('relu'),
#     output dari neural network membagi 2 jenis nada
    Dense(2),
#     aktivasi fungsi softmax
    Activation('softmax'),
    ])
#%%
# fitur ekstraksi
model.compile(optimizer='adam',
             loss='categorical_crossentropy',
             metrics=['accuracy'])
print(model.summary())
#%%
# melakukan pelatihan
# epochs = iterasi
# batch size = 1x epochs dilakukan 32 file
# split = 20% untuk dicek cross validation
model.fit(train_input, train_labels, epochs=10, batch_size=2, validation_split=0.2)
#%%
loss, acc = model.evaluate(test_input, test_labels, batch_size=32)
#%%
print('Done!')
# loss = prediksi salah, acc = ketepatan
print('Loss: %.4f, accuracy: %.4f' % (loss, acc))
#%%
p = extract_features_song('DataTA/NadaDasar/tak/tak1.wav')
#print(p)