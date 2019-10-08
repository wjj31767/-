import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd
import os
import time

nn = pd.read_csv('a20n/0.05.csv')
nn= pd.DataFrame(data=nn,dtype=np.int)
lower_T=1500000
tmp=nn[(nn['T']>=lower_T)].groupby('y')['x'].idxmin()
tt = pd.DataFrame(columns = ('x','y'))
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
x2new = np.arange(x2[y2.argmin()],x.max(),0.01)
yder = interpolate.splev(x2new,spl,der=1)
save_value = 0

save_value = np.degrees(np.arctan(1/0.251))
print(save_value)
plt.figure()
plt.plot(x,y)
plt.plot(x2new, yder)
plt.legend(['Cubic Spline'])
plt.title('Derivative estimation from spline')
plt.show()
# save_file=save_file.append(pd.DataFrame({'x':[y2.min()],'y':[x2[y2.argmin()]]}),ignore_index=True)
