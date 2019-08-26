import numpy as np
import pandas as pd
import glob
import datetime

np.set_printoptions(threshold=99999, suppress=True, precision=4)

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

mun_name = pd.read_csv('days_dry_2017.csv', sep=';')
mun_name = np.array(mun_name['Municipio'])

ndd = np.load('number_days_dry_month.npy')

startdate = datetime.datetime(1973, 1 , 1)
enddate = datetime.datetime(2019, 7, 31)

dates = pd.date_range(startdate, enddate, freq='M')
calyear = dates.year
calmon = dates.month


ndd_full = np.full((4, ndd.shape[0], ndd.shape[1]) , np.nan)
ndd_annual = np.full(( ndd.shape[0], 46) , np.nan)

for m in range(len(mun_name)):
    
    for y in range(46):
        
        id = np.where(calyear == y+1973)[0]
        if np.sum( ~np.isnan(ndd[m, id]))>7:
            ndd_annual[m, y] = np.nansum(ndd[m, id])

    for c,ii in enumerate([2, 3, 4, 6 ]):
    
        ndd_full[c,m, :] = sum_months(ndd[m, :], ii )
    print(ndd_annual[m, :])


#     ndd_3m = sum_months(ndd[0, :], 3 ))
#     ndd_4m = sum_months(ndd[0, :], 4 ))
# ndd_6m = sum_months(ndd[0, :], 6 ))
