import numpy as np
import cupy as cp
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd
import os
import time
import math


def linefit(x, y):
    N = float(len(x))
    sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
    for i in range(0, int(N)):
        sx += x[i]
        sy += y[i]
        sxx += x[i] * x[i]
        syy += y[i] * y[i]
        sxy += x[i] * y[i]
    a = (sy * sx / N - sxy) / (sx * sx / N - sxx)
    b = (sy - a * sx) / N
    r = abs(sy * sx / N - sxy) / math.sqrt((sxx - sx * sx / N) * (syy - sy * sy / N))
    return a, b, r
def getmin(path):
    filelist = os.listdir(path)
    save_file = pd.DataFrame(columns=('x','y','angle'))
    for files in filelist:
        if 'csv' in files:
            continue
        dir_path = os.path.join(path, files)
        print(dir_path, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # print(dir_path)
        test = pd.read_csv(dir_path,header=None,skiprows=[0,1],sep='\s+',)
        # print(test[1]*1000)
        xy = pd.read_csv('xy.dat',header=None,skiprows=[0,1],sep='\s+')
        # print(xy[0]*100000,xy[1]*100000)
        nn = pd.concat([xy[0]*100000,xy[1]*100000,test[1]*1000],axis=1)
        nn.columns = ['x', 'y', 'T']
        # print(nn)
        nn=nn.sort_values(by=['y','x'],ascending=True)
        nn.reset_index(drop=True, inplace=True)
        nn= pd.DataFrame(data=nn,dtype=np.int)
        lower_T=1500000
        tmp=nn[(nn['T']>=lower_T)].groupby('y')['x'].idxmin()
        tt = pd.DataFrame(columns = ('x','y','angle'))
        for i in tmp:
            if nn.loc[i, :]['y'] == nn.loc[i - 1, :]['y']:
                # print(nn.loc[i,:],nn.loc[i-1,:])
                b = nn.loc[i, :]
                s = nn.loc[i - 1, :]
                # interpolating
                xd = (lower_T - s['T']) / (b['T'] - s['T']) * (b['x'] - s['x']) + s['x']
                tt=tt.append(pd.DataFrame({'x':[xd],'y':[b['y']]}),ignore_index=True)
        # print(tt)
        x = tt['y']
        y = tt['x']
        spl = interpolate.splrep(x, y)
        x2 = np.arange(x.min(),x.max(),0.01)
        y2 = interpolate.splev(x2, spl)
        xnew = y[:y.idxmin()]  # x
        ynew = x[:y.idxmin()]  # y
        xnewf = xnew[(xnew < 25) & (xnew > 20)]  # xnew - x
        ynewf = ynew[(xnew < 25) & (xnew > 20)]  # ynew - y
        a, b, r = linefit(xnewf.values, ynewf.values)
        save_file=save_file.append(pd.DataFrame({'x':[y2.min()],'y':[x2[y2.argmin()]],'angle':[90+np.degrees(np.arctan(a))]}),ignore_index=True)
    save_file.to_csv(path+'/minvalue.csv')
if __name__=='__main__':
    paths = [r"a20/dataToThomas/a20"]
    for path in paths:
        getmin(path)
    nn = pd.read_csv('a20/dataToThomas/a20/minvalue.csv')
    plt.scatter(nn['x'] / 100000, nn['y'] / 100000, c=nn['angle'])
    plt.colorbar()
    plt.xlim((nn['x'].min() - 1) / 100000, (nn['x'].max() + 1) / 100000)
    plt.ylim((nn['y'].min() - 10) / 100000, (nn['y'].max() + 10) / 100000)
    plt.show()

