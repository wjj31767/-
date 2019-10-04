#!/usr/bin/env python3
import os
# 添加需要安装的扩展包名称进去
libs = {"matplotlib" , "seaborn" , "numpy" , "pandas"}
try:
    for lib in libs:
        os.system(" pip install " + lib)
        print("{}   Install successful".format(lib))
except:
    print("{}   failed install".format(lib))
import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import seaborn as sns
import multiprocessing
pool = multiprocessing.Pool()
# try to directly deal with the *tar.gz doc
# import tarfile
# tar = tarfile.open("a20.tar.gz")
# for member in tar.getmembers():
#      f = tar.extractfile(member)
#      print(f)
     # if f is not None:
     #     content = f.read()

# c= np.fromfile('a20/0.051.dat',dtype=float)
# df = pd.read_table("a20/0.051.dat")

# change data from '.dat' to '.csv'
# import os
# nn = open('T_interpolatedPlane - Copy.dat','r')
# new_dir = 'T_interpolatedPlane - Copy.csv'
#
# file_test2 = open(new_dir, 'w')
# file_test2.write('x,y,z,T')
# file_test2.write('\n')
# for lines in nn.readlines():
#     if '#' in lines:
#         continue
#     str_data = ",".join(lines.split())
#     file_test2.write(str_data)
#     file_test2.write('\n')
# nn.close()
def tt(files):
    dir_path = os.path.join(path, files)
    # 分离文件名和文件类型
    file_name = os.path.splitext(files)[0]  # 文件名
    file_type = os.path.splitext(files)[1]  # 文件类型
    file_test = open(dir_path, 'r')
    # 将.dat文件转为.csv文件
    new_dir = os.path.join(path, str(file_name) + '.csv')
    xydat = open('xy.dat', 'r')
    print('changing process', new_dir, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    file_test2 = open(new_dir, 'w')
    file_test2.write('x,y,T\n')
    for lines in zip(file_test.readlines(), xydat.readlines()):
        # print(lines)
        str_data = list(lines[1].split())
        # print(str_data)
        str_data[0] = str_data[0].replace('.', '')
        str_data[0] = str_data[0].lstrip('0')
        if len(str_data[0]) == 0:
            str_data[0] = '0'
        str_data[1] = str_data[1].replace('.', '')
        str_data[1] = str_data[1].lstrip('0')
        if len(str_data[1]) == 0:
            str_data[1] = '0'
        str_data = ','.join(str_data)
        # print(str_data)
        file_test2.write(str_data)
        str_data = ',' + lines[0].split()[1].replace('.', '')
        file_test2.write(str_data+'\n')
    file_test.close()
def trans(path):
    filelist = os.listdir(path)
    cnt = 0
    for files in filelist:
        if '.csv' in files:
            continue
        pool.apply_async(tt,(files,))
    pool.close()
    pool.join()
# sorting the original data
def ts(file):
    print('sorting process', file, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    dir_path = os.path.join(path, file)
    nn = pd.read_csv(dir_path)
    nn = nn.sort_values(by=['y', 'x'], ascending=True)
    nn.reset_index(drop=True, inplace=True)
    file = 's' + file
    dir_path = os.path.join(path, file)
    nn.to_csv(dir_path)
def sorting(path):
    filelist = os.listdir(path)
    for file in filelist:
        if 'dat' in file:
            continue
        pool.apply_async(ts,(file,))
    pool.close()
    pool.join()


def it(file,f4minx):
    dir_path = os.path.join(path, file)
    nn = pd.read_csv(dir_path)
    file1 = 'i' + file
    dir_path1 = os.path.join(path, file1)
    print('isotherm process', dir_path1, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    tl = open(dir_path1, 'w')
    tl.write('x,y,T\n')
    nn = pd.read_csv(dir_path)
    nn = pd.DataFrame(data=nn, dtype=np.int)
    lower_T = 1500000
    tmp = nn[(nn['T'] >= lower_T)].groupby('y')['x'].idxmin()
    for i in tmp:
        if nn.loc[i, :]['y'] == nn.loc[i - 1, :]['y']:
            # print(nn.loc[i,:],nn.loc[i-1,:])
            b = nn.loc[i, :]
            s = nn.loc[i - 1, :]
            # interpolating
            xd = (lower_T - s['T']) / (b['T'] - s['T']) * (b['x'] - s['x']) + s['x']
            tl.write(str(xd)+','+str(b['y']+','+str(lower_T)+'\n'))
    tmpr = nn[(nn['T'] >= lower_T)].groupby('y')['x'].idxmax()
    for i in tmpr:
        if i + 1 < len(nn) and nn.loc[i, :]['y'] == nn.loc[i + 1, :]['y']:
            # print(nn.loc[i,:],nn.loc[i-1,:])
            b = nn.loc[i, :]
            s = nn.loc[i + 1, :]
            # interpolating
            xd = (lower_T - s['T']) / (b['T'] - s['T']) * (b['x'] - s['x']) + s['x']
            tl.write(str(xd)+','+str(b['y']+','+str(lower_T)+'\n'))
    tl.close()
    tmp = pd.read_csv(dir_path)
    plt.scatter(tmp['x'] / 100000, tmp['y'] / 100000, c=tmp['T'] / 1000, cmap='gray')
    plt.colorbar()
    tt = pd.read_csv(dir_path1)
    plt.scatter(tt['x'] / 100000, tt['y'] / 100000, marker='.', s=1)
    plt.xlim(0, 0.008)
    plt.ylim(0, 0.032)
    file_name = os.path.splitext(file1)[0]  # 文件名
    save_dir_path = os.path.join(path, str(file_name) + '.png')
    plt.savefig(save_dir_path)
    f4 = pd.read_csv(dir_path1)
    tmp = f4.iloc[f4['x'].idxmin(), :]
    f4minx.write(str(tmp['x'])+','+str(tmp['y']+'\n'))
def isotherm(path):
    filelist = os.listdir(path)
    f4_dir_path = str(path[:3])+'.csv'
    f4minx = open(f4_dir_path,'w')
    f4minx.write('x,y\n')
    for file in filelist:
        if file[0]!='s':
            continue
        pool.apply_async(it, (file,))
    pool.close()
    pool.join()
    filelist=os.listdir(path)
    for file in filelist:
        if 'is' in file:
            continue
        dir_path1=os.path.join(path,file)
        f4 = pd.read_csv(dir_path1)
        tmp = f4.iloc[f4['x'].idxmin(), :]
        f4minx.write(str(tmp['x']) + ',' + str(tmp['y'] + '\n'))
    f4minx.close()

def kdef():
    files = os.listdir()
    for file in files:
        if 'csv' in file:
            nn = pd.read_csv(file)
            sns.kdeplot(nn['x']/100000,shade=True)
    plt.savefig('final.png')
if __name__=='__main__':

    paths = [r"a20/dataToThomas/a20"]
    for path in paths:
        trans(path)
        print('complete change dat to csv in {}',path,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        sorting(path)
        print('complete sorting in {}',path,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        isotherm(path)
        print('complete iostherm in {}',path,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
    kdef()
