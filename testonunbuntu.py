import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import os
#
# files='0.05.dat'
# # 分离文件名和文件类型
# file_name = os.path.splitext(files)[0]  # 文件名
# file_type = os.path.splitext(files)[1]  # 文件类型
#
# file_test = open(files, 'r')
# # 将.dat文件转为.csv文件
# new_dir = os.path.join(str(file_name) + '.csv')
# xydat= open('xy.dat','r')
# print(new_dir)
# file_test2 = open(new_dir, 'w')
# file_test2.write('x,y,T')
# file_test2.write('\n')
#
# cnt = 0
#
#
# for lines in zip(file_test.readlines(),xydat.readlines()):
#     #print(lines)
#     str_data =list(lines[1].split())
#     #print(str_data)
#     str_data[0]=str_data[0].replace('.','')
#     str_data[0]=str_data[0].lstrip('0')
#     if len(str_data[0])==0:
#         str_data[0]='0'
#     str_data[1] = str_data[1].replace('.', '')
#     str_data[1]=str_data[1].lstrip('0')
#     if len(str_data[1])==0:
#         str_data[1]='0'
#     str_data=','.join(str_data)
#     file_test2.write(str_data)
#     str_data=','+lines[0].split()[1].replace('.','')
#     file_test2.write(str_data)
#     file_test2.write('\n')
# file_test.close()


# nn = open('T_interpolatedPlane.dat','r')
# nw = open('T_interpolatedPlane.csv','w')
# for lines in nn.readlines():
#     if '#' in lines:
#         continue
#     str_data=
#     print(str_data[0])
#     nw.write(str_data)
#     nw.write('\n')
# nw.close()
# nn = pd.read_csv('T_interpolatedPlane.csv')
# nn = np.concatenate((nn.values[:,0][:,np.newaxis]*100000,nn.values[:,1][:,np.newaxis]*100000,nn.values[:,3][:,np.newaxis]*10000000),axis=1)
# nn = nn.astype(np.int)
# np.savetxt('T_interpolatedPlane.csv', nn ,delimiter=',',header='x,y,T',comments='')
# nn=pd.read_csv('T_interpolatedPlane.csv')
# nn=pd.DataFrame(data=nn,dtype=np.int)
# nn = nn.sort_values(by=['y','x'],ascending=True)
# nn.index=range(len(nn))
# nn.to_csv('T_interpolatedPlane.csv')
# nn=pd.read_csv('T_interpolatedPlane.csv')
# plt.scatter(x=nn['x'],y=nn['y'],c=nn['T'])
# tt = pd.read_csv('tp.csv')
# plt.scatter(x=tt['x'],y=tt['y'])
# plt.show()

# c= np.fromfile('a20/0.051.dat',dtype=float)
# df = pd.read_table("a20/0.051.dat")

# change data from '.dat' to '.csv'

import os
# dir_path='T_interpolatedPlane.dat'
# file_test = open(dir_path, 'r')
# #     # 将.dat文件转为.csv文件
# new_dir = 'T_interpolatedPlane.csv'
#
# file_test2 = open(new_dir, 'w')
# file_test2.write('x,y,z,T')
# file_test2.write('\n')
# cnt =0
# for lines in file_test.readlines():
#     if '#' in lines:
#         print(cnt)
#         cnt+=1
#         continue
#     str_data = ",".join(lines.split())
#     file_test2.write(str_data)
#     file_test2.write('\n')
# file_test.close()
#
# path_0 = r"a20"
#
# path_1 = r"a20n"
#
# filelist = os.listdir(path_0)
#
# for files in filelist:
#
#     dir_path = os.path.join(path_0, files)
#     # 分离文件名和文件类型
#     file_name = os.path.splitext(files)[0]  # 文件名
#     file_type = os.path.splitext(files)[1]  # 文件类型
#
#     print(dir_path)
#     file_test = open(dir_path, 'r')
#     # 将.dat文件转为.csv文件
#     new_dir = os.path.join(path_1, str(file_name) + '.csv')
#
#     print(new_dir)
#
#     file_test2 = open(new_dir, 'w')
#     file_test2.write('x,T')
#     file_test2.write('\n')
#     for lines in file_test.readlines():
#         str_data = ",".join(lines.split())
#         file_test2.write(str_data)
#         file_test2.write('\n')
#     file_test.close()
from operator import itemgetter

# # get dmin
#
# nn = pd.read_csv('0.05.csv')
# nn = pd.DataFrame(nn)
#
# nn.sort_values(['y','x'],inplace=True)
# nn.reset_index(drop=True,inplace=True)
# print(nn)
# nn.to_csv('tmp.csv')
# print(nn)

# tl = open('tp.csv','w')
# tl.write('x,y,T')
# tl.write('\n')
# nn = pd.read_csv('tmp.csv')
# nn = pd.DataFrame(data=nn,dtype=np.int)
# lower_T=1500000
# tmp=nn[(nn['T']>=lower_T)].groupby('y')['x'].idxmin()
#
# for i in tmp:
#     if nn.loc[i,:]['y']==nn.loc[i-1,:]['y']:
#         #print(nn.loc[i,:],nn.loc[i-1,:])
#         b=nn.loc[i,:]
#         s=nn.loc[i-1,:]
#         # interpolating
#         xd = (lower_T-s['T'])/(b['T']-s['T'])*(b['x']-s['x']) +s['x']
#         tl.write(str(xd))
#         tl.write(',')
#         tl.write(str(b['y']))
#         tl.write(',')
#         tl.write(str(lower_T))
#         tl.write('\n')
# tl.close()
# nn=pd.read_csv('tp.csv')
# print(nn.loc[nn['x'].idxmin(),:])

# nn = nn.sort_values(by=['y','x'],ascending=True)
# nn.index = range(len(nn))
# nn.to_csv('T_interpolatedPlane.csv')
# print(nn)

# calculate the interpolation
# lower_T=1500
# tmp=nn[(nn['T']>=lower_T)].groupby('y')['x'].idxmin()
# for i in tmp:
#     if nn.loc[i-1,:]['y']!=nn.loc[i,:]['y']:
#         continue
#     if abs(nn.loc[i,:]['T']-1500)>100:
#         print(nn.loc[i,:],nn.loc[i-1,:])
# tmp=nn[(nn['T']>=lower_T)].groupby('y')['x'].idxmax()
# # filelist = os.listdir(path_1)
# print(tmp)


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


import matplotlib.pyplot as plt
import seaborn as sns
tmp = pd.read_csv('0.05.csv')
plt.scatter(tmp['x'],tmp['y'],c=tmp['T'],cmap='gray')
plt.colorbar()
tt=pd.read_csv('tp.csv')
plt.plot(tt['x'],tt['y'])
plt.show()
