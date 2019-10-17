import numpy as np
import pandas as pd
import time
# 第一个问题，3g文件的话，内存就算分段去计算的话也并不会少太多，70的时候就快出问题了，毕竟tmp降不下去
# 所以写到一半保存一下，释放一下内存
# 然后之后每一个bunch都合并一下？
# 第二个问题就是浮点数会不会导致组数变大了
def calchunk(tmp,final,gcnt):
    gl = len(tmp)
    tmp = pd.DataFrame(tmp)
    tmp.rename(columns={0:'a',1:'v',2:'k'},inplace=True)
    tt = tmp.groupby('a')
    print('after group',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cnt = 0
    printtime = 50000
    sumtmp = 0
    for it in tt:
        final.append([it[0],sum(it[1]['a']*it[1]['v']),sum(it[1]['v']*it[1]['k'])])
        sumtmp += len(it[1])
        cnt +=1
        if cnt%printtime==0:
            print(sumtmp/gl,printtime,'%completed',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # print(it['a'].mean(),sum(it['a']*it['v']),sum(it['v']*it['k']))
    print(gcnt,'th chunk',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
if __name__ == '__main__':
    chunksize = 10000000
    tmp = []
    final = []
    print('starttime',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    flag = False
    cnt = 0
    gcnt = 0
    for lines in zip(open('alpha.liquidMean','r'),open('V','r'),open('KlMean','r')):
        if flag:
            tmp.append([float(line[:-1]) for line in lines])
            if cnt == chunksize:
                gcnt += 1
                print(gcnt*chunksize/83762176,'completed', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                calchunk(tmp,final,gcnt)
                cnt = 0
                tmp = []
            else:
                cnt += 1
        if '(' in lines[0] or ')' in lines[0]:
            flag = not flag
    calchunk(tmp,final,gcnt)
    print('finish chunk', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    final = pd.DataFrame(final)
    final.rename(columns={0: 'a', 1: 'av', 2: 'vk'}, inplace=True)
    finalg = final.groupby('a')
    truefinal = []
    truefinal = pd.DataFrame(columns=('a','av','vk'))
    for it in finalg:
        truefinal.append([it[0], sum(it[1]['av']), sum(it[1]['vk'])])
    truefinal = pd.DataFrame(truefinal)
    truefinal.rename(columns = {0:'a',1:'av',2:'vk'},inplace = True)
    print('finish final csv', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    truefinal.to_csv('final.csv')
    print('finish write file csv', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

