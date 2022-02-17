from cgitb import text
from tkinter import *

root = Tk()

# set window size
root.geometry("800x600")
# title
root.title("Sistem Identifikasi Nada Darbuka")

# default value of form
windowLength = StringVar(root, value=0.02)
frameLength = StringVar(root, value=0.01)
mfccTotalFeature = StringVar(root, value=13)

Label(root, text="Panjang Window (detik)").place(x=10, y=20)
Entry(root, width=25, textvariable=windowLength).place(x=10, y=40)
Label(root, text="Panjang Frame (detik)").place(x=10, y=60)
Entry(root, width=25, textvariable=frameLength).place(x=10, y=80)
Label(root, text="Jumlah Fitur MFCC").place(x=10, y=100)
Entry(root, width=25, textvariable=mfccTotalFeature).place(x=10, y=120)

root.mainloop()