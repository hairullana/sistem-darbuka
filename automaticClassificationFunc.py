import classificationFunc

def klasifikasiNada(k, windowLength, frameLength, mfccCoefficients, info, klasifikasiDum, klasifikasiTak, klasifikasiSlap, presentaseKlasifikasi):

  hasilKlasifikasiDum = ""
  hasilKlasifikasiTak = ""
  hasilKlasifikasiSlap = ""
  jumlahKlasifikasiDumBenar = 0
  jumlahKlasifikasiTakBenar = 0
  jumlahKlasifikasiSlapBenar = 0
  jumlahDataTesting = 0
  textPresentaseKlasifikasi = ""

  # TESTING DUM
  hasilKlasifikasiDum += '\nSedang melakukan klasifikasi nada DUM (K=' + str(k) + ')\n'
  for i in range(20) :
    indeks = i + 51
    filename = 'DataTA/NadaDasar/dum/dum' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'DUM':
      jumlahKlasifikasiDumBenar += 1
    hasilKlasifikasiDum += '\nHasil dari klasifikasi ' + file2 + ' adalah nada ' + hasil
    jumlahDataTesting += 1

  # TESTING TAK
  hasilKlasifikasiTak += '\nSedang melakukan klasifikasi nada TAK (K=' + str(k) + ')\n'
  for i in range(20) :
    indeks = i + 51
    filename = 'DataTA/NadaDasar/tak/tak' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'TAK':
      jumlahKlasifikasiTakBenar += 1
    hasilKlasifikasiTak += '\nHasil dari klasifikasi ' + file2 + ' adalah nada ' + hasil
    jumlahDataTesting += 1

  # TESTING SLAP
  hasilKlasifikasiSlap += '\nSedang melakukan klasifikasi nada SLAP (K=' + str(k) + ')\n'
  for i in range(20) :
    indeks = i + 51
    filename = 'DataTA/NadaDasar/slap/slap' + str(indeks) + '.wav'
    hasil, k_dum, k_tak, k_slap, indeks = classificationFunc.klasifikasi(filename, k, windowLength, frameLength, mfccCoefficients)
    file = filename.split(sep="/")
    file2 = file[len(file)-1]
    if hasil == 'SLAP':
      jumlahKlasifikasiSlapBenar += 1
    hasilKlasifikasiSlap += '\nHasil dari klasifikasi ' + file2 + ' adalah nada' + hasil
    jumlahDataTesting += 1
  
  jumlahKlasifikasiBenar = jumlahKlasifikasiDumBenar + jumlahKlasifikasiTakBenar + jumlahKlasifikasiSlapBenar

  textPresentaseKlasifikasi += "Akurasi Nada DUM = " + str(jumlahKlasifikasiDumBenar) + "/20 (" + str(jumlahKlasifikasiDumBenar/20*100) + "%)\n"
  textPresentaseKlasifikasi += "Akurasi Nada TAK = " + str(jumlahKlasifikasiTakBenar) + "/20 (" + str(jumlahKlasifikasiTakBenar/20*100) + "%)\n"
  textPresentaseKlasifikasi += "Akurasi Nada SLAP = " + str(jumlahKlasifikasiSlapBenar) + "/20 (" + str(jumlahKlasifikasiSlapBenar/20*100) + "%)\n"
  textPresentaseKlasifikasi += "Akurasi Sistem = " + str(jumlahKlasifikasiBenar) + "/60 (" + str(jumlahKlasifikasiBenar/60*100) + "%)"

  info.config(text="")
  klasifikasiDum.config(text=hasilKlasifikasiDum)
  klasifikasiTak.config(text=hasilKlasifikasiTak)
  klasifikasiSlap.config(text=hasilKlasifikasiSlap)
  presentaseKlasifikasi.config(text=textPresentaseKlasifikasi)