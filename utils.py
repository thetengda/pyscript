import time


def str2stamp(strtime: str):  # time stamp of epoch
    time_array = time.strptime(strtime, "%Y %m %d %H %M %S")
    time_stamp = time.mktime(time_array)
    sec = float(strtime.split()[5])
    sec -= time_array[5]
    return time_stamp+sec


freqmap = {
    "G": {
        '1': 1575.42e6,
        '2': 1227.60e6,
        '5': 1176.45e6
    },
    "E": {
        '1': 1575.42e6,
        '5': 1176.45e6,
        '7': 1207.140e6,
        '8': 1191.795e6,
        '6': 1278.75e6
    },
    "C": {
        '2': 1561.098e6,
        '1': 1575.42e6,
        '5': 1176.45e6,
        '7': 1207.140e6,
        '8': 1191.795e6,
        '6': 1268.52e6
    }
}

clight = 299792458.0


def freqof(csys, cfreq):
    if freqmap.get(csys) != None and freqmap[csys].get(cfreq) != None:
        return freqmap[csys][cfreq]
    return None


def lambof(csys, cfreq):
    fr = freqof(csys, cfreq)
    if fr == None:
        return None
    else: return  clight/fr