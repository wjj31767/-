import numpy as np
from scipy import interpolate
import pandas as pd
import os
import time
import multiprocessing
import matplotlib.pyplot as plt
import sys
lower_T=1500
lower_T*=1000
paths = [r"a05",r"a10",r"a20",r"a40"]
file_end = '.txt'
def tt(files):
    dir_path = os.path.join(path, files[1])
    print(dir_path, files[0],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    test = pd.read_csv(dir_path,header=None,skiprows=[0,1],sep='\s+',)
    xy = pd.read_csv('xy.dat',header=None,skiprows=[0,1],sep='\s+')
    nn = pd.concat([xy[0]*100000,xy[1]*100000,test[1]*1000],axis=1)
    nn.columns = ['x', 'y', 'T']
    nn=nn.sort_values(by=['y','x'],ascending=True)
    nn.reset_index(drop=True, inplace=True)
    nn= pd.DataFrame(data=nn,dtype=np.int)
    tmp=nn[(nn['T']>=lower_T)].groupby('y')['x'].idxmin()
    tt = []
    for i in tmp:
        if nn.loc[i, :]['y'] == nn.loc[i - 1, :]['y']:
            b = nn.loc[i, :]
            s = nn.loc[i - 1, :]
            xd = (lower_T - s['T']) / (b['T'] - s['T']) * (b['x'] - s['x']) + s['x']
            tt.append([xd,b['y']])
    tt = pd.DataFrame(tt,columns=['x','y'])
    x = tt['y']
    y = tt['x']
    spl = interpolate.splrep(x, y)
    x2 = np.arange(x.min(),x.max(),0.1)
    y2 = interpolate.splev(x2, spl)
    xnew = y[:y.idxmin()]  # x
    ynew = x[:y.idxmin()]  # y
    ttt = [[y2.min(),x2[y2.argmin()],np.degrees(np.arctan((xnew.max()-xnew.min())/(ynew.max()-ynew.min())))]]
    tttdir = os.path.join(tmppath,files[1])
    np.savetxt(tttdir,ttt)
def getmin(path):
    filelist = os.listdir(path)
    pool = multiprocessing.Pool()
    for files in enumerate(filelist):
        pool.apply_async(tt,(files,))
    pool.close()
    pool.join()
def merge(path):
    tmp = pd.DataFrame()
    for i in os.listdir(tmppath):
        dir_path = os.path.join(tmppath,i)
        tmp = tmp.append(pd.read_csv(dir_path,header=None,sep='\s+',))
    np.savetxt(path+file_end,tmp)
def draw(path,lim):
    nn = pd.read_csv(path + file_end, header=None, skiprows=[0, 1, 2], sep="\s+", )
    lim[0] = max(lim[0],nn[0].max())
    lim[1] = min(lim[1],nn[0].min())
    lim[2] = max(lim[2],nn[1].max())
    lim[3] = min(lim[3],nn[1].min())
    plt.scatter(nn[0] / 100000, nn[1] / 100000, c=nn[2],cmap = 'coolwarm_r')
    plt.text(x=nn[0].min()/100000, y=nn[1].min()/100000, s=path, fontsize=15)
if __name__=='__main__':
    
    tmppath = r'a20tmp'
    if not os.path.exists(tmppath):
        os.makedirs(tmppath)
    for i in os.listdir(tmppath):
        dir_path = os.path.join(tmppath,i)
        os.remove(dir_path)
    for path in paths:
        getmin(path)
        merge(path)
        for i in os.listdir(tmppath):
            dir_path = os.path.join(tmppath,i)
            os.remove(dir_path)
    os.removedirs('a20tmp')
    lim = [-sys.maxsize, sys.maxsize, -sys.maxsize, sys.maxsize]
    for path in paths:
        draw(path, lim)
    cb = plt.colorbar()
    cb.set_label('Angle/degree at Temperatur' + str(lower_T / 1000) + 'K')
    plt.xlim(1.7e-4, 3e-4)
    plt.ylim(0.006, 0.013)
    # plt.xlim((lim[1] - 1) / 100000, (lim[0] + 1) / 100000)
    # plt.ylim((lim[3] - 10) / 100000, (lim[2] + 10) / 100000)
    plt.grid(linestyle='-', color='0.5', linewidth=2)
    plt.xlabel('x/m')
    plt.ylabel('y/m')
    plt.savefig('final')
    plt.show()
