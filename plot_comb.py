import os
import matplotlib.pyplot as plt
import sys
import json
import time

from utils import str2stamp

def readcomb(file): ## return [time][sat] val
    data={}
    with open(file,'r') as fp:
        line = fp.readline()
        while line:
            if line[0] == '#':
                line = fp.readline()
                continue
            if line[0] == '>':
                stamp = str2stamp(line[2:2+19])
                if data.get(stamp) == None:
                    data[stamp] = {}
                line = fp.readline()
                continue
            csat = line[1:4]
            val = float(line[4:])
            data[stamp][csat] = val
            line = fp.readline()
    return data

def plot():

    return

if __name__ == '__main__':
    # ind = sys.argv.index('-c')
    # if ind > len(sys.argv)-1 : exit('no comb file')
    # else : cfiles = sys.argv[ind+1]
    ind = sys.argv.index('-f')
    if ind > len(sys.argv)-1 : exit('no conf file')
    else : kfile = sys.argv[ind+1]   
    
    with open(kfile,'r') as fp : conf = json.load(fp)
    cfiles = conf['cfiles'] 
    ## find files
    p = cfiles.rfind('/')
    files = []
    if p==-1: dir = '.'
    else : dir = cfiles[:p]
    q = cfiles.rfind('.')
    if q==-1: exit("input no ext")
    else: ext = cfiles[q+1:]
    outdir = os.path.join(dir,ext)
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    if cfiles[p+1:].startswith('*.'):  
        for f in os.listdir(dir):
            fullp = os.path.join(dir,f)
            if os.path.isfile(fullp) and f.endswith(ext): 
                files.append(fullp)
    else:
        files = cfiles.split()
    ## plot
    for cfile in files:
        name= os.path.basename(cfile)[0:4]
        data = readcomb(cfile)
        data_sort={}
        for stamp in data:
            for sat in data[stamp]:
                if data_sort.get(sat[0])==None:
                    data_sort[sat[0]]={}
                if data_sort[sat[0]].get(sat) == None :
                    data_sort[sat[0]][sat]={'time':[],'val':[]}
                dt =time.gmtime(stamp)
                doy = dt.tm_yday + (dt.tm_hour*3600+dt.tm_min*60 +dt.tm_sec)/86400.0
                data_sort[sat[0]][sat]['time'].append(doy)
                data_sort[sat[0]][sat]['val'].append(data[stamp][sat])
        for csys in data_sort:
            for sat in data_sort[csys]:
                plt.scatter(data_sort[csys][sat]['time'],data_sort[csys][sat]['val'],s=1)
            # plt.ylim([-60,30])
            plt.xlabel('day of year')
            plt.ylabel(conf['ylabel'][ext][csys]+'/meters')
            plt.grid()
            if conf['lim']['open']:
                if cfile.find(conf["rcv"])!=-1 :
                    plt.ylim(conf["lim"][ext]["rcv"])
                    plt.title(conf['title'][ext]['rcv'])
                else :
                    plt.ylim(conf["lim"][ext][csys])
                    plt.title(conf['title'][ext][name])

            plt.savefig(os.path.join(outdir,os.path.basename(cfile)+'.'+csys+'.png'))
            plt.close()
    plot()