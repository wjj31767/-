# 没法共同拥有数组
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd
import os
import time
import multiprocessing
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
    lower_T=1500000
    tmp=nn[(nn['T']>=lower_T)].groupby('y')['x'].idxmin()
    tt = []
    for i in tmp:
        if nn.loc[i, :]['y'] == nn.loc[i - 1, :]['y']:
            # print(nn.loc[i,:],nn.loc[i-1,:])
            b = nn.loc[i, :]
            s = nn.loc[i - 1, :]
            # interpolating
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
    save_file.append([y2.min(),x2[y2.argmin()],np.degrees(np.arctan(xnew.max()-xnew.min())/(ynew.max()-ynew.min()))])
def getmin(path):
    filelist = os.listdir(path)
    cnt = 0
    pool = multiprocessing.Pool()
    for files in enumerate(filelist):
        cnt+=1
        pool.apply_async(tt,(files,))
        if cnt == 50:
            break
    pool.close()
    pool.join()
    save_file = pd.DataFrame(save_file,columns=['x','y','angle'])
    print(save_file,'pool exit')
    save_file.to_csv('minvalue.csv')
if __name__=='__main__':
    paths = [r"a20/dataToThomas/a20"]
    save_file = []
    for path in paths:
        save_file = []
        getmin(path)
    # nn = pd.read_csv('minvalue.csv')
    # plt.scatter(nn['x'] / 100000, nn['y'] / 100000, c=nn['angle'])
    # plt.colorbar()
    # plt.xlim((nn['x'].min() - 1) / 100000, (nn['x'].max() + 1) / 100000)
    # plt.ylim((nn['y'].min() - 10) / 100000, (nn['y'].max() + 10) / 100000)
    # plt.show()
