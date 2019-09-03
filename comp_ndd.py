import numpy as np 
import pandas as pd 
from glob import glob
from datetime import datetime
from pfct.DefineDates import index_between_dates
from calendar import monthrange

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

def count_nddm(dbin, start_date, end_date):
    cook = []
    for ii,y in enumerate(range(start_year, end_year+1)):
        for m in range(12):
            [mon, lday ] = monthrange(y,m+1)
            #print()
            #print(y*10000+(m+1)*100+lday,'and ', end_date)
            #input()
            if y*10000+(m+1)*100+lday > end_date:
                break
            else:
            #print(str(start_date),str(end_date),'{0}{1:02d}01'.format(y,m+1), '{0}{1:02d}{2}'.format(y,m+1,lday))
            
                d1, d2 = index_between_dates(str(start_date), str(end_date), '{0}{1:02d}01'.format(y,m+1), '{0}{1:02d}{2}'.format(y,m+1,lday), 'days')
 
                aux = dbin[d1:d2+1]

                if np.sum(~np.isnan(aux)) >= 21:
                    cook.append(np.nansum(aux))
                else:
                    cook.append(np.nan)
            #    print(len(cook))
    return np.array(cook)


municipios = np.sort(glob('pr_daily*/*.txt'))
calyear, calmon, calday, pr = np.loadtxt(municipios[-1], unpack=True,dtype={'names'  : ('a', 'b', 'c','d'), 'formats' : ('i4','i2','i2','f4')})

#print(calyear.shape)

start_year = calyear[0]
end_year = calyear[-1]
start_mon = calmon[0]
end_mon = calmon[-1]
start_day = calday[0]
end_day = calday[-1]

# defining variables to save things inside.

datesm = pd.date_range(datetime(start_year,start_mon,start_day), datetime(end_year,end_mon,end_day),freq='M')
calyearm = datesm.year
nddm = np.full((len(municipios),len(datesm)), np.nan)
mun_name = np.full((len(municipios),),np.nan,dtype='<U30')

for s, fin in enumerate(municipios):

    mun_name[s] = fin.split('-')[-2]
    print (mun_name[s])

    data = np.loadtxt(fin)
    pr = data[:, 3]
    pr [ pr == -999. ] = np.nan 
    pr_bin = np.copy(pr)
    pr_bin[pr < 2. ] = 1.
    pr_bin[pr  > 2. ] = 0.

    date = calyear*10000 + calmon*100 + calday
    
    date_start = calyear[0]*10000 + calmon[0]*100 + calday[0]
    date_end   = calyear[-1]*10000 + calmon[-1]*100 + calday[-1]
    
    nddm[s,:] = count_nddm(pr_bin, date_start, date_end)

np.save('nddm_municipios.npy',nddm)

nddm = np.load('nddm_municipios.npy')
ndd_full = np.full((4, nddm.shape[0], nddm.shape[1]) , np.nan)
ndd_annual = np.full(( nddm.shape[0], 46) , np.nan)

for m in range(len(mun_name)):
    
    for y in range(46):
        
        id = np.where(calyearm == y+1973)[0]
        if np.sum( ~np.isnan(nddm[m, id]))>7:
            ndd_annual[m, y] = np.nansum(nddm[m, id])

    for c,ii in enumerate([2, 3, 4, 6 ]):
    
        ndd_full[c,m, :] = sum_months(nddm[m, :], ii )
    #print(ndd_annual[m, :])

np.save('ndd_full.npy', ndd_full)
np.save('ndd_annual.npy', ndd_annual)
