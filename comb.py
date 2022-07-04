from datetime import datetime
import numpy as np
import sys
import json

from rnxin import *


def combobs(obs, coef):  # return [time][sat]
    combed = {}
    for time in obs:
        if combed.get(time) == None:
            combed[time] = {}  # time flag
        for sat in obs[time]:
            combval = 0.0
            if coef.get(sat[0]) == None:  # system mask
                continue
            for ind in coef[sat[0]]:
                if ind >= len(obs[time][sat]) or obs[time][sat][ind] == None or coef[sat[0]].get(ind) == None:
                    combval = None
                    break
                combval += obs[time][sat][ind] * coef[sat[0]][ind]
            if combval == None:
                continue
            combed[time][sat] = combval
    return combed


if __name__ == '__main__':
    code, obs, coef, ofile = None, None, None, None
    for i in range(len(sys.argv)):
        # if sys.argv[i] == '-o':
        #     i += 1
        #     if i < len(sys.argv):
        #         ofiles = sys.argv[i]
        #         # code,obs = readobs(sys.argv[i])
        #         # fptmp = open(sys.argv[i]+'.'+str(int(time.time()))+'.comb.tmp','w')
        #     else:
        #         exit('no obs')
        if sys.argv[i] == '-f':
            i += 1
            if i < len(sys.argv):
                with open(sys.argv[i]) as fp:
                    coef = json.load(fp)
            else:
                exit('no config')

    beg = 0
    end = 99999e99
    if coef.get('time') != None:
        if len(coef['time']) > 0:
            beg = str2stamp(coef['time'][0])
        if len(coef['time']) > 1:
            end = str2stamp(coef['time'][1])
        coef.pop('time')  # you need pop to left combs only
    if coef.get('obs') !=None:
        ofiles = coef['obs']
        coef.pop('obs')
    for ofile in ofiles.split():
        code, obs = readobs(ofile, 'm', beg, end)

        for comb in coef:
            pcoef = {}
            for csys in coef[comb]:
                if pcoef.get(csys) == None:
                    pcoef[csys] = {}
                if comb.startswith('mp'):
                    if len(coef[comb][csys]) <2 : exit('mp need 2 freq')
                    alpha = (lambof(csys,coef[comb][csys][0][0])/lambof(csys,coef[comb][csys][1][0]))**2
                    types = ['C'+coef[comb][csys][0],'L'+coef[comb][csys][0],'L'+coef[comb][csys][1]]
                    coefs = [1,-(1+2.0/(alpha-1)),2./(alpha-1)]
                    for i in range(3):
                        ind = code[csys].index(types[i])
                        if pcoef[csys].get(ind) != None:
                            exit('conflict in config')
                        pcoef[csys][ind] = coefs[i]
                else :
                    for type in coef[comb][csys]:
                        ind = code[csys].index(type)
                        if pcoef[csys].get(ind) != None:
                            exit('conflict in config')
                        pcoef[csys][ind] = coef[comb][csys][type]
            combed = combobs(obs, pcoef)
            # out print
            with open(ofile+'.'+comb, 'w') as fptmp:
                fptmp.write('## {} \n'.format(coef[comb]))
                for tstamp in combed:
                    fptmp.write('>{} {}\n'.format(datetime.strftime(
                        datetime.fromtimestamp(tstamp), ' %Y %m %d %H %M %S'), len(combed[tstamp])))
                    for sat in combed[tstamp]:
                        fptmp.write(' {} {:14.6f} \n'.format(
                            sat, combed[tstamp][sat]))
                print(fptmp.name)
                fptmp.close()
