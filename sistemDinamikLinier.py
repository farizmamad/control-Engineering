# Dibuat oleh: Ahmad Fariz
# 14 April 2019, 10:13
# Code ini dapat disebarluaskan untuk tujuan pendidikan

# ============================================ #
#       KESTABILAN SISTEM DINAMIK LINIER
# ============================================ #

# Salah satu pendekatan dalam memodelkan sistem dinamik adalah menggunakan model linier.
# Berdasarkan ref [1], sistem dinamik linier dimodelkan dengan state-space:
#                               (d/dt)x = A*x + B*u
#   di mana A adalah matriks persegi [A bagian dari R^(n x n)], x adalah vektor state,
#   B adalah matriks kendali, dan u adalah input kendali.

# Matriks A memiliki eigenvalue(s), yaitu suatu besaran yang menggambarkan karakteristik
# dinamik sistem tersebut. Eigenvalue ditulis dalam bentuk:
#           riil:                   eigenvalue = (riil)
#           imajiner:               eigenvalue = +- (imajiner) j
#           kompleks:               eigenvalue = (riil) +- (imajiner) j

# Teorinya, sebuah sistem dinamik linier dikatakan stabil asimptotik jika dan hanya jika
# seluruh eigenvalue dari A memiliki bagian riil yang bernilai negatif.

# Berarti, sistem tidak stabil jika ada salah satu eigenvalue dari A yang memiliki
# bagian riil yang bernilai positif.

# ====== REFERENSI ========
# [1] K. J. Alstrom dan R. M. Murray, Feedback System: An Introduction for Scientists and Engineers 2nd Edition

# =============================================== #
#  MENGANALISIS KESTABILAN SISTEM DINAMIK LINIER
# =============================================== #

# Kasus yang diangkat adalah sebuah sistem pegas-massa sesuai contoh 3.1 dari referensi.
# Diketahui sistem pegas-massa sederhana bisa dimodelkan dengan persamaan diferensial:
#       m * (d^2/dt^2)q + c * (d/dt)q + k * q = 0 (Pers. 3.1)
# di mana m adalah massa, c adalah konstanta redaman/friksi, dan k adalah
# konstanta pegas

# Pada (Pers. 3.1), state dari sistem adalah q, di mana q adalah posisi.

# Maka, vektor state x adalah:
#           x = [x_1, x_2]
#           x_1 = (d/dt)q
#           x_2 = q

# Turunan dari tiap state adalah:
#           (d/dt)x_1 = (d^2/dt^2)q
#           (d/dt)x_1 = (-c/m) * (d/dt)x_1 + (-k/m) * x_2
#           (d/dt)x_2 = (d/dt)q = x_1

# Dengan hasil turunan tersebut, kita bisa membuat matriks dinamika sistem pegas-massa:
#           A = [[(-c / m), (-k / m)],
#                [ 1, 0]]

# =================================================== #
#                  START THE SCRIPT
# =================================================== #

import matplotlib.pyplot as plt
import numpy as np
from control import StateSpace, pzmap
from matplotlib import animation
from scipy import integrate
from animasiSpring import animSpringMass

# Buat sebuah kelas yang menggambarkan sistem pegas massa
class sistemPegasMassa:

    def __init__(self, m, c, k):
        self.A = np.array([[(-c / m), (-k / m)], [1, 0]])

    # Fungsi dinamika sistem pegas-massa adalah x dot = A*x
    def dinSis(self, state, t):
        dxdt = np.dot(self.A, state)
        return dxdt


if __name__ == '__main__':

    # Beri nilai m, c, k untuk masing-masing sistem
    m, c, k = (3, 1, 2)

    # Buat objek dari kelas sistem pegas massa
    pegasMassa = sistemPegasMassa(m, c, k)

    # Keluarkan matriks dinamik dari sistem tersebut
    A = pegasMassa.A
    print('Matriks dinamika sistem adalah: \n', A, '\n')

    # Kemudian buat representasi State Space dari sistem pegas-massa tersebut.
    # Buat matriks B dan D berisi 0, dan C = matriks identitas.
    B = np.zeros(np.shape(A))
    C = np.identity(np.ndim(A))
    D = np.zeros(np.shape(B))

    # Representasi state space nya adalah sebagai berikut
    mySys = StateSpace(A, B, C, D)
    #print('Model linier sistem adalah: \n', mySys)

    # Hitung eigenvalue dari sistem pegas massa tersebut
    poles = mySys.pole()
    print('Poles sistem adalah: \n', poles, '\n')

    # Nyatakan apakah sistem stabil atau tidak. Apabila nilai poles nya bukan bilangan complex
    # sistem tidak stabil
    if str(type(poles[1])) == "<class 'numpy.float64'>":
        print('===> sistem tidak stabil \n')
    else:
        print('===> sistem stabil \n')

    # Visualisasikan pula lokasi poles dengan memetakannya di ruang kompleks C.
    # Seluruh poles dari sistem yang stabil berada di sebelah kanan sumbu
    # imajiner
    pzmap(mySys)
    #fig = plt.figure()

    # Berikutnya dilakukan perhitungan dinamika sistem pegas-massa
    # Membuat array selang waktu dari 0 sampai 20 dengan time frame 0.05
    dt = 0.05
    t = np.arange(0.0, 20, dt)
    yt = []
    for i in range(len(t)):
    	yt.append(-0.5)

    # Mendefinisikan kondisis awal masing-masing state
    vInit = 1.0		# kecepatan awal
    sInit = 0.0		# posisi/simpangan awal

    # Kondisi awal state
    initState = [vInit, sInit]

    # Buat dinamika sistemnya
    dinSis = pegasMassa.dinSis

    # Hitung posisi dan kecepatan masing-masing sistem sepanjang 20 detik
    state = integrate.odeint(dinSis, initState, t)

    # Visualisasikan
    visualisasiSistem = animSpringMass(state)
    plt.plot(t, yt)
    plt.show()
