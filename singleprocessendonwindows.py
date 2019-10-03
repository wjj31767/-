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
def trans(path_0,path_1):
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
# trans(path_0,path_1)
# sorting the original data
def sorting(path_0):
    filelist = os.listdir(path_0)
    for file in filelist:
        dir_path = os.path.join(path_0,file)
        nn = pd.read_csv(dir_path)
        nn=nn.sort_values(by=['y','x'],ascending=True)
        nn.reset_index(drop=True, inplace=True)
        file = 's'+file
        dir_path = os.path.join(path_0,file)
        nn.to_csv(dir_path)
#sorting(path_1)
import matplotlib.pyplot as plt
import seaborn as sns
def isotherm(path_0):
    filelist = os.listdir(path_0)
    f4_dir_path = str(path_0[:3])+'.csv'
    print(f4_dir_path)
    f4minx = open(f4_dir_path,'w')
    f4minx.write('x,y')
    f4minx.write('\n')
    for file in filelist:
        if file[0]!='s':
            continue
        dir_path = os.path.join(path_0, file)
        print(dir_path)
        nn = pd.read_csv(dir_path)
        file1 = 'i'+file
        dir_path1 = os.path.join(path_0,file1)
        print(dir_path1)
        tl = open(dir_path1,'w')
        tl.write('x,y,T')
        tl.write('\n')
        nn = pd.read_csv(dir_path)
        nn = pd.DataFrame(data=nn,dtype=np.int)
        lower_T=1500000
        tmp=nn[(nn['T']>=lower_T)].groupby('y')['x'].idxmin()
        for i in tmp:
            if nn.loc[i,:]['y']==nn.loc[i-1,:]['y']:
                #print(nn.loc[i,:],nn.loc[i-1,:])
                b=nn.loc[i,:]
                s=nn.loc[i-1,:]
                # interpolating
                xd = (lower_T-s['T'])/(b['T']-s['T'])*(b['x']-s['x']) +s['x']
                tl.write(str(xd))
                tl.write(',')
                tl.write(str(b['y']))
                tl.write(',')
                tl.write(str(lower_T))
                tl.write('\n')
        tmpr = nn[(nn['T']>=lower_T)].groupby('y')['x'].idxmax()
        for i in tmpr:
            if i+1<len(nn) and nn.loc[i,:]['y']==nn.loc[i+1,:]['y']:
                #print(nn.loc[i,:],nn.loc[i-1,:])
                b=nn.loc[i,:]
                s=nn.loc[i+1,:]
                # interpolating
                xd = (lower_T-s['T'])/(b['T']-s['T'])*(b['x']-s['x']) +s['x']
                tl.write(str(xd))
                tl.write(',')
                tl.write(str(b['y']))
                tl.write(',')
                tl.write(str(lower_T))
                tl.write('\n')
        tl.close()
        tmp = pd.read_csv(dir_path)
        plt.scatter(tmp['x']/100000,tmp['y']/100000,c=tmp['T']/1000,cmap='gray')
        plt.colorbar()
        tt=pd.read_csv(dir_path1)
        plt.scatter(tt['x']/100000,tt['y']/100000,marker='.',s=1)
        plt.xlim(0, 0.008)
        plt.ylim(0, 0.032)
        file_name = os.path.splitext(file1)[0]  # 文件名
        save_dir_path=os.path.join(path_0,str(file_name)+'.png')
        plt.savefig(save_dir_path)
        plt.show()
        f4 = pd.read_csv(dir_path1)
        tmp = f4.iloc[f4['x'].idxmin(),:]
        f4minx.write(str(tmp['x']))
        f4minx.write(',')
        f4minx.write(str(tmp['y']))
        f4minx.write('\n')
    f4minx.close()
    tmp = pd.read_csv(f4_dir_path)
    file_name = os.path.splitext(f4_dir_path)[0]  # 文件名
    sns.kdeplot(tmp['x']/100000,shade=True)
    plt.savefig(file_name + '.png')
    plt.show()
#isotherm(path_1)
tmp = pd.read_csv('a20.csv')
sns.kdeplot(tmp['x']/100000,shade=True)
plt.show()
