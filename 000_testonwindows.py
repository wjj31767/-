import numpy as np
import pandas as pd

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

import os

path_0 = r"a20/dataToThomas/a20"

path_1 = r"a20n"

filelist = os.listdir(path_0)

for files in filelist:

    dir_path = os.path.join(path_0, files)
    # 分离文件名和文件类型
    file_name = os.path.splitext(files)[0]  # 文件名
    file_type = os.path.splitext(files)[1]  # 文件类型

    print(dir_path)
    file_test = open(dir_path, 'r')
    # 将.dat文件转为.csv文件
    new_dir = os.path.join(path_1, str(file_name) + '.csv')
    xydat= open('xy.dat','r')
    print(new_dir)
    file_test2 = open(new_dir, 'w')
    file_test2.write('x,y,T')
    file_test2.write('\n')
    for lines in zip(file_test.readlines(),xydat.readlines()):
        #print(lines)
        str_data =list(lines[1].split())
        #print(str_data)
        str_data[0]=str_data[0].replace('.','')
        str_data[0]=str_data[0].lstrip('0')
        if len(str_data[0])==0:
            str_data[0]='0'
        str_data[1] = str_data[1].replace('.', '')
        str_data[1]=str_data[1].lstrip('0')
        if len(str_data[1])==0:
            str_data[1]='0'
        str_data=','.join(str_data)
        #print(str_data)
        file_test2.write(str_data)
        str_data=','+lines[0].split()[1].replace('.','')
        file_test2.write(str_data)
        file_test2.write('\n')
    file_test.close()
# sorting
# nn = pd.read_csv('a20n/0.05.csv')
# nn=nn.sort_values(by=['y','x'],ascending=True)
# nn.reset_index(drop=True, inplace=True)
# print(nn)
# get dmin
# nn = pd.read_csv('a20n/0.05.csv')
# nn = pd.DataFrame(nn)
# #print(nn)
# lower_T=1499
# tmp=nn[(nn['T']>=lower_T)&(nn['T']<=lower_T+2)]['x'].idxmin()
# #print(nn.iloc[tmp,:])
# tt = nn[nn['T']>1500].groupby('y')['x'].idxmax()
# #print(tt)
# for i in tt:
#     tmp = nn.iloc[i,:]
#     tx = tmp['x']
#     ty = tmp['y']
#     bt = tmp['T']
#     tmps = nn[(nn['x']==(tx+0.00002))&(nn['y']==ty)]
#     print(tmps,bt)
# tt = nn[nn['T']>1500].groupby('y')['x'].idxmin()
# #print(tt)
# print(
#     tt
# )
# print()
# print(nn['x'])
# tmp=nn.loc[nn.y==0.00000].T.interpolate()
# print(tmp)
# print(nn.loc[nn.x<1500].x.max)
#
# filelist = os.listdir(path_1)
#
# dp = 'tmp.csv'
# f = open(dp,'w')
# f.write('dmin')
# f.write('\n')
# for files in filelist:
#     dir_path = os.path.join(path_1, files)
#     nn = pd.read_csv(dir_path)
#     lower_T=1500
#     tmp=nn[(nn['T']>=lower_T)&(nn['T']<=lower_T+1)].min()
#     # print(tmp['x'])
#     f.write(str(round(tmp['x'],3)))
#     f.write('\n')
# f.close()

#plot


# import matplotlib.pyplot as plt
# import seaborn as sns
# tmp = pd.read_csv('tmp.csv')
# tt=sns.distplot(tmp,hist=False)
# plt.show()


# import matplotlib.pyplot as plt
# import seaborn as sns
# nn = pd.read_csv('T_interpolatedPlane - Copy.csv')
# nn = pd.DataFrame(nn)
# sns.scatterplot(nn['x'],nn['y'])
# plt.show()

