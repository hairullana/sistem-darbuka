from tkinter import *
import tkinter.font
from tkinter import ttk
import trainingDataFunc
import automaticClassificationFunc
import resetResultFunc
import selectFileFunc
from tkinter import messagebox as mb

# Set Window
root = Tk()
root.geometry("1200x800")
root.title("Sistem Identifikasi Nada Darbuka")

# Open File Style
s = ttk.Style()
s.configure('TButton', font="Normal 12")

# Default Value of Parameter Form
windowLength = 0.02
frameLength = 0.01
mfccCoefficients = 13
k = 1

# Heading Template
h1 = tkinter.font.Font(size=20)
h2 = tkinter.font.Font(size=16)

# Simpan koefisien
def simpanKoefisien():
  global windowLength, frameLength, mfccCoefficients, k
  windowLength = float(windowLengthEntry.get())
  frameLength = float(frameLengthEntry.get())
  mfccCoefficients = int(mfccCoefficientsEntry.get())
  k = int(kEntry.get())
  windowLengthLabel.config(text="Panjang Window (detik) = " + str(windowLength))
  frameLengthLabel.config(text="Panjang Frame (detik) = " + str(frameLength))
  mfccCoefficientsLabel.config(text="Jumlah Koefisien MFCC = " + str(mfccCoefficients))
  kLabel.config(text="Jumlah K = " + str(k))
  mb.showinfo('Success', 'Parameter berhasil disimpan')

# DISPLAY
# TITLE
Label(root, text="SISTEM IDENTIFIKASI NADA DARBUKA", font=h1).grid(row=0, column=2, columnspan=6)
# COLUMN A
# Sub Title
Label(root, text="Parameter", font=h2).grid(row=2, column=0, pady=10)
# Form
windowLengthLabel = Label(root, text="Panjang Window (detik) = " + str(windowLength))
windowLengthLabel.grid(row=3, column=0, pady=5)
windowLengthEntry = Entry(root, width=25, textvariable=StringVar(root, value=windowLength))
windowLengthEntry.grid(row=3, column=1)
frameLengthLabel = Label(root, text="Panjang Frame (detik) = " + str(frameLength))
frameLengthLabel.grid(row=4, column=0, pady=5)
frameLengthEntry = Entry(root, width=25, textvariable=StringVar(root, value=frameLength))
frameLengthEntry.grid(row=4, column=1)
mfccCoefficientsLabel = Label(root, text="Jumlah Koefisien MFCC = " + str(mfccCoefficients))
mfccCoefficientsLabel.grid(row=5, column=0, pady=5)
mfccCoefficientsEntry = Entry(root, width=25, textvariable=StringVar(root, value=mfccCoefficients))
mfccCoefficientsEntry.grid(row=5, column=1)
kLabel = Label(root, text="Jumlah K = " + str(k))
kLabel.grid(row=6, column=0, pady=5)
kEntry = Entry(root, width=25, textvariable=StringVar(root, value=k))
kEntry.grid(row=6, column=1)
Button(root, text="simpan", command=simpanKoefisien).grid(row=7, column=0, columnspan=2, pady=5)

# Sub Title
Label(root, text="Aksi", font=h2).grid(row=2, column=3, pady=10)
# COLUMN B-1
Button(root, text = "Training Data", command=lambda: trainingDataFunc.trainingData(windowLength, frameLength, mfccCoefficients, info), font="Normal 15").grid(row=3, column=3, rowspan=2, pady=5, padx=10)
Button(root, text="Klasifikasi", command=lambda: automaticClassificationFunc.klasifikasiNada(k, windowLength, frameLength, mfccCoefficients, info, klasifikasiDum, klasifikasiTak, klasifikasiSlap, presentaseKlasifikasi), font="Normal 15").grid(row=5, column=3, rowspan=2 ,pady=5, padx=10)
# COLUMN B-2
Button(root, text="Reset Hasil", command=lambda: resetResultFunc.resetHasil(klasifikasiDum, klasifikasiTak, klasifikasiSlap, presentaseKlasifikasi, info), font="Normal 15").grid(row=3, column=5, rowspan=2 ,pady=5, padx=10)
ttk.Button(root, text='Open a File', command=lambda: selectFileFunc.select_file(k, windowLength, frameLength, mfccCoefficients, klasifikasiDum, klasifikasiTak, klasifikasiSlap, presentaseKlasifikasi, info), style='TButton').grid(row=5, column=5, rowspan=2 ,pady=5, padx=10)

# Training Data
info = Label(root, text="")
info.grid(row=9, column=3)
# Hasil Klasifikasi
klasifikasiDum = Label(root, text=" ")
klasifikasiDum.grid(row=9, column=0, columnspan=2, padx=10)
klasifikasiTak = Label(root, text=" ")
klasifikasiTak.grid(row=9, column=2, columnspan=2, padx=10)
klasifikasiSlap = Label(root, text=" ")
klasifikasiSlap.grid(row=9, column=4, columnspan=2, padx=10)
# Hasil Klasifikasi (Tingkat Akurasi)
presentaseKlasifikasi = Label(root, text=" ")
presentaseKlasifikasi.grid(row=10, column=0, columnspan=6, pady=10)

root.mainloop()