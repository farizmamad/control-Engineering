# Membuat a spring-mass system coordinate
# definisi class
"""
nama class adalah springMass.
class berisi:
    1. MembuatBox               -> koordinat kotak massa
    2. MembuatDumper            -> koordinat dumper
    3. MembuatSpring            -> koordinat pegas
    4. MembuatInitialPosition   -> koordinat posisi inisial (garis putus-putus berwarna merah)
    5. titik pusat massa
    6. plot                     -> menampilkan plot dari sistem pegas massa

format class:
springMass(x)
    x adalah koordinat titik pusat masa di sumbu-x. Nilai default x = 0

output yang didapat:
    .boxCoor()          -> koordinat kotak massa
    .dumperCoor()       -> koordinat dumper
    .springCoor()       -> koordinat spring
    .initialPosCoor()   -> koordinat posisi inisial


pemanggilan kelas dari program luar
from plotSpring import springMass

a = springMass(0)
a.plot()

dibuat oleh
Cahya Amalinadhi Putra

Silahkan untuk diubah/didistribusikan

@EngCode.id
"""

import math
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np


class animSpringMass():
    def __init__(self, state):
        self.state = state

        # Definisi nilai geometri
        self.box_length = 1
        self.box_center = [0, 0]
        self.line_length = 0
        self.spring_coor_x = []
        self.spring_coor_y = []
        self.dumper_coor_x = []
        self.dumper_coor_y = []

        # Membuat figure
        self.fig = plt.figure(figsize=(5, 5))
        # Membuat axes
        self.ax = plt.axes(xlim=(0, 8), ylim=(-self.box_length / 2.0 - 3.5, self.box_length / 2.0 + 3.5), aspect='equal')

        # Membuat box massa
        self.center = [self.line_length, self.box_center[1]]
        self.bottomleft = (self.center[0] - (self.box_length / 2.0), self.center[1] - (self.box_length / 2.0))
        self.box = plt.Rectangle(self.bottomleft, self.box_length, self.box_length)
        self.ax.add_patch(self.box)

        # Membuat pegas
        self.spring, = self.ax.plot([], [], lw=2)

        # Membuat peredam
        self.dumper, = self.ax.plot([], [], lw=2)

        self.callAnimation()

    def callAnimation(self):
        self.anim = animation.FuncAnimation(self.fig, self.animate, frames = np.arange(1, len(self.state)),
            init_func=self.init, interval=25, blit=True, repeat=False)

    def animate(self, i):
        # dinamika posisi box
        self.box.set_xy((self.line_length + self.state[i][1], self.bottomleft[1]))
        #print(self.box)
        # dinamika posisi peredam
        dumper_seq_array = np.array([0, 0, 0, 0, 0, 1])
        self.dumper.set_data((self.dumper_coor_x + dumper_seq_array * self.state[i][1]), self.dumper_coor_y)
        # Membuat array untuk menentukan faktor susut pegas
        spring_seq_array = np.arange(0, 1, (1 / len(self.spring_coor_x)))
        # dinamika posisi pegas
        self.spring.set_data((self.spring_coor_x + spring_seq_array * self.state[i][1]), self.spring_coor_y)
        return self.box, self.dumper, self.spring,

    def init(self):
        self.line_length = 4 * self.box_length + self.box_center[0]
        # kondisi awal box
        self.box.set_xy(self.bottomleft)
        # kondisi awal peredam
        self.MembuatDumper()
        self.dumper.set_data(self.dumper_coor_y, self.dumper_coor_x)
        # kondisi awal pegas
        self.MembuatSpring()
        self.spring.set_data(self.spring_coor_y, self.spring_coor_x)
        return self.box, self.dumper, self.spring,

    def MembuatSpring(self):
        total_length = self.line_length
        part1 = 0.25
        part2 = total_length - 0.5
        part3 = total_length - (part1 + part2)

        # part 1
        for i in range(2):
            temp_x = i * part1
            temp_y = -self.box_length / 4.0

            self.spring_coor_x.append(temp_x)
            self.spring_coor_y.append(temp_y)

        # part 2
        size = 20
        delta = part2 / size

        for i in range(size - 1):
            temp_x = (i + 1) * delta + part1
            temp_y = -self.box_length / 4.0 + \
                math.pow(-1, (i + 1)) * self.box_length / 8.0

            self.spring_coor_x.append(temp_x)
            self.spring_coor_y.append(temp_y)

        # part 3
        for i in range(2):
            temp_x = total_length - part3 * (1 - i)
            temp_y = -self.box_length / 4.0

            self.spring_coor_x.append(temp_x)
            self.spring_coor_y.append(temp_y)

    def MembuatDumper(self):
        half_length = self.line_length / 2.

        temp_x = [0, half_length, half_length,
                  half_length, half_length, self.line_length]
        temp_y = [self.box_length / 4.0, self.box_length / 4.0, self.box_length /
                  3.0, self.box_length / 5, self.box_length / 4.0, self.box_length / 4.0]

        self.dumper_coor_x = temp_x
        self.dumper_coor_y = temp_y
