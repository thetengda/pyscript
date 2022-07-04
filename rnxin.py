from math import ceil
from utils import *
import numpy as np
import sys

def readobshead(fp): ## return [csys][code list]
    line = fp.readline()
    codes = {}
    tmp =""
    nline=0
    while line:
        if line.find('END OF HEADER') == 60:
            break
        if line.find('SYS / # / OBS TYPES')==60:
            if line[0] != ' ': 
                csys = line[0]
                nline = ceil(float(line[3:6])/13)
            if nline > 0: 
                tmp+=line[6:6+52];nline-=1
                if nline == 0: 
                    codes[csys] = ['C2I' if csys=='C' and c=='C1I' else c for c in tmp.split()] ## rnx3.02
                    codes[csys];tmp="";nline=0
        line = fp.readline()
    return codes

def readobs(file,unit = 'm',beg=0,end=99999e99): ## return code, obs[time][sat][data list]
    fp = open(file,'r')
    codes = readobshead(fp)
    line = fp.readline()
    obs={}
    while line:
        if line[0]=='>':
            str_time = line[2:1+28-8]
            epoch_time = str2stamp(str_time)
            if  epoch_time > end:
                break
            if epoch_time < beg:
                flag = 99
            else:
                flag = int(line[29:29+3])
            line = fp.readline()
            continue
        if flag > 1:line = fp.readline();continue ## special event
        csat = line[0:3]
        pos = 3
        if obs.get(epoch_time) == None:
            obs[epoch_time] = {}
        if obs[epoch_time].get(csat) == None:
            obs[epoch_time][csat] = []
        iobs=0
        while pos <len(line): 
            if line[pos:pos+14].isspace():
                val = None
            else:
                typ = codes[csat[0]][iobs]
                factor = 1.0
                lamb = lambof(csat[0],typ[1])
                if lamb ==None :
                    val=None
                else:
                    if typ[0] == 'L' and unit =='m':
                        factor = lamb
                    if typ[0] == 'C' and unit == 'cycle':
                        factor = 1.0/lamb
                    val = float(line[pos:pos+14]) * factor
            obs[epoch_time][csat].append(val)
            pos += 16
            iobs+=1
        line = fp.readline()
    fp.close()
    return codes,obs