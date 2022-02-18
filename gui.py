from cgitb import text
from tkinter import *
import tkinter.font

root = Tk()

# set window size
root.geometry("800x600")
# title
root.title("Sistem Identifikasi Nada Darbuka")

# default value of form
windowLength = StringVar(root, value=0.02)
frameLength = StringVar(root, value=0.01)
mfccTotalFeature = StringVar(root, value=13)

# heading template
h1 = tkinter.font.Font(size=20)
h2 = tkinter.font.Font(size=16)

# simpan koefisien
def simpanKoefisien():
  class koefisien:
    def __init__(self, windowLength, frameLength, mfccTotalFeature):
      self.windowLength = windowLength
      self.frameLength = frameLength
      self.mfccTotalFeature = mfccTotalFeature

# title
Label(root, text="SISTEM IDENTIFIKASI NADA DARBUKA", font=h1).place(x=100, y=10)
# sub title
Label(root, text="Koefisien", font=h2).place(x=10, y=50)
# form
Label(root, text="Panjang Window (detik)").place(x=10, y=80)
Entry(root, width=25, textvariable=windowLength).place(x=10, y=100)
Label(root, text="Panjang Frame (detik)").place(x=10, y=120)
Entry(root, width=25, textvariable=frameLength).place(x=10, y=140)
Label(root, text="Jumlah Fitur MFCC").place(x=10, y=160)
Entry(root, width=25, textvariable=mfccTotalFeature).place(x=10, y=180)
# button
Button(root, text="simpan", command=simpanKoefisien).place(x=50, y=210)


root.mainloop()