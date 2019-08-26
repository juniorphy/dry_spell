import numpy as np
import pandas as pd
import glob
mun_name = pd.read_csv('days_dry_2017.csv', sep=';')
mun_name = np.array(mun_name['Municipio'])
#print(len(mun_name))

ndd = np.load('number_days_dry_month.npy')

def sum_months(data, scale):
    
    XS = []
    for i in range(scale):
        XS.append(data[i:len(data)-scale+i+1])
    XS = np.array(XS).T
    if scale != 1:
        glue = XS.sum(axis=1)
    else:
        glue = XS
    A = np.full(data.shape, np.nan)
    A[scale-1:] = glue
    return A

ndd_full = np.full((4, ndd.shape[0], ndd.shape[1]) , np.nan)

for c,ii in enumerate([2, 3, 4, 6 ]):
    for m in range(len(mun_name)):
       # print(mun_name[m])
        ndd_full[c,m, :] = sum_months(ndd[m, :], ii )

print(ndd_full[0,0,:])
print(ndd[0, ...])
#     ndd_3m = sum_months(ndd[0, :], 3 ))
#     ndd_4m = sum_months(ndd[0, :], 4 ))
# ndd_6m = sum_months(ndd[0, :], 6 ))
