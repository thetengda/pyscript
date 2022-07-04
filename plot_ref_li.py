import matplotlib.pyplot as plt
import numpy as np


def degree2rad(degree):
    return degree * np.pi / 180.0


def blh2xyz(lat, lon, hgt):
    sinp = np.sin(lat)
    cosp = np.cos(lat)
    sinl = np.sin(lon)
    cosl = np.cos(lon)
    RE_WGS84 = 6378137.0
    FE_WGS84 = (1.0 / 298.257223563)
    e2 = FE_WGS84 * (2.0 - FE_WGS84)
    v = RE_WGS84 / np.sqrt(1.0 - e2 * sinp * sinp)
    x = (v + hgt) * cosp * cosl
    y = (v + hgt) * cosp * sinl
    z = (v * (1.0 - e2) + hgt) * sinp
    return x, y, z


def xyz2enu(lat, lon, dx, dy, dz):
    sinp = np.sin(lat)
    cosp = np.cos(lat)
    sinl = np.sin(lon)
    cosl = np.cos(lon)
    E = []
    E[0] = -sinl
    E[3] = cosl
    E[6] = 0.0
    E[1] = -sinp * cosl
    E[4] = -sinp * sinl
    E[7] = cosp
    E[2] = cosp * cosl
    E[5] = cosp * sinl
    E[8] = sinp
    rot = np.array(E).reshape([3, 3])
    enu = rot @ np.array([dx, dy, dz])
    return enu


def readref(file: str):
    state = 0
    txyz = []
    with open(file, 'r') as fp:
        for line in fp.readlines():
            if line.startswith('   (weeks)'):
                state = 1
                continue
            if state == 1:
                words = line.split(',')
                sod = np.mod(float(words[1]), 86400.0)
                x, y, z = blh2xyz(degree2rad(float(words[2])), degree2rad(float(
                    words[3])), float(words[4]))
                txyz.append([sod, x, y, z])
    return txyz


def readcord(file: str):
    with open(file, 'r') as fp:
        head = fp.readline().split()
        txyz = []
        for line in fp.readlines():
            words = line.split()
            sod = float(words[head.index('sod')])
            x = float(words[head.index('X')])
            y = float(words[head.index('Y')])
            z = float(words[head.index('Z')])
            txyz.append([sod, x, y, z])
    return txyz


def adjust(ref, pos):
    sub = []
    i = 0
    for r in ref:
        while i < len(pos):
            if pos[i][0] == r[0]:
                sub.append([r[0], pos[i][1]-r[1], pos[i]
                           [2]-r[2], pos[i][3]-r[3], r[1], r[2], r[3]])
                i += 1
                break
            if pos[i][0] < r[0]:
                i += 1
            if pos[i][0] > r[0]:
                break
        if i == len(pos):
            break
    return np.array(sub)


if __name__ == '__main__':
    pref = readref('d165/backward.txt')
    ppos = readcord('d165/neiz2022165_ppp.coor')
    sub = adjust(pref, ppos)

    plt.plot(sub[:, 0], sub[:, 1], label='X')
    plt.plot(sub[:, 0], sub[:, 2], label='Y')
    plt.plot(sub[:, 0], sub[:, 3], label='Z')
    plt.legend()
    plt.ylim([-5000, 5000])
    plt.xlabel('sod')
    plt.ylabel('bias/m')
    plt.show()

    print(' ')
