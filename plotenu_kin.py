import sys
import matplotlib.pyplot as plt
import numpy as np
import re

def readcord_enu(file):
    data=[]
    with open(file,'r') as fp : 
        head = [x for x in re.split(' |\t|\r|\n',fp.readline()) if x]
        pind = [head.index('sod'),head.index('E'),head.index('N'),head.index('U')]
        for line in fp.readlines():
            ep =[]
            words = line.split()
            for i in pind: ep.append(float(words[i])) 
            data.append(ep)
    return np.array(data)

def adjust(ref,pos):
    sub=[]
    i=0
    for r in ref :
        while i < len(pos):
            if pos[i][0] == r[0]: sub.append([r[0],pos[i][1]-r[1],pos[i][2]-r[2],pos[i][3]-r[3]]);i+=1;break
            if pos[i][0] < r[0]:i+=1
            if pos[i][0] > r[0]:break
        if i == len(pos) : break
    return np.array(sub)
def plotenu_kin(fref,*files):
    pref = readcord_enu(fref)
    for f in files :
        ppos = readcord_enu(f)
        sub = adjust(pref,ppos)
        plt.plot(sub[:,0],sub[:,1],label='E')
        plt.plot(sub[:,0],sub[:,2],label='N')
        plt.plot(sub[:,0],sub[:,3],label='U')
        plt.legend();plt.xlabel('sod');plt.ylabel('bias/m')
        plt.ylim([-10,10]);plt.title(f)
        plt.savefig(f+'.png')
        plt.close()
        print(' ')
    return

if __name__ =='__main__':
    plotenu_kin('d160/rcvz2022160_ppp.coor','d160/waiz2022160_ppp.coor','d160/neiz2022160_ppp.coor')