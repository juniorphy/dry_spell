import numpy as np 
import pandas as pd 
from glob import glob
from datetime import datetime,date
from pfct.DefineDates import index_between_dates
from calendar import monthrange
from dateutil.relativedelta import relativedelta

np.set_printoptions(threshold=99999, suppress=True, precision=4)

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

def comp_dryspell(dados_bin, scale):
    dry = np.full((19, 2), np.nan)
    if np.sum(~np.isnan(dados_bin)) > 21*scale :#for y, year in enumerate(range(start_year, end_year+1))
        dummy = []
        c = 0
        for bin in dados_bin:                        
            if   bin == 1.: 
                c += 1
            elif bin == 0 and c == 0: 
                c = 0
            elif bin == 0:
                dummy.append(c) 
                c = 0
        dummy.append(c)
                  
        dummy = np.array(dummy) #.sort(reverse = True).
        print(dummy)     
        
        cook = np.sort(dummy)
        for k in range(3,22):
            if k < 21:
                                  
                dry[k-3, :] = k,  len(np.where(dummy == k)[0])
            else:
                dry[k-3, :] = k,  len(np.where(dummy >= k)[0])
    else:
        dry[:,:] = np.nan
    return dry

municipios = np.sort(glob('pr_daily*/*.txt'))
calyear, calmon, calday, pr = np.loadtxt(municipios[-1], unpack=True,dtype={'names'  : ('a', 'b', 'c','d'), \
'formats' : ('i4','i2','i2','f4')})

start_year = calyear[0]
end_year = calyear[-1]
start_mon = calmon[0]
end_mon = calmon[-1]
start_day = calday[0]
end_day = calday[-1]

nyear = end_year - start_year + 1

# defining variables to save things on them.

datesm = pd.date_range(datetime(start_year,start_mon,start_day), datetime(end_year,end_mon,end_day),freq='M')
calyearm = datesm.year

# Matrix with dryspell for several timescales 
dry_spell_freq = np.full((len(municipios), 4, nyear, 19, 2), np.nan)

mun_name = np.full((len(municipios),),np.nan,dtype='<U30')

for s, fin in enumerate(municipios):

    mun_name[s] = fin.split('-')[-2]
    print (mun_name[s])

    data = np.loadtxt(fin)
    pr = data[:, 3]
    pr [ pr == -999. ] = np.nan 
    pr_bin = np.copy(pr)
    pr_bin[pr < 2. ] = 1.
    pr_bin[pr >= 2. ] = 0.

    date = calyear*10000 + calmon*100 + calday
    
    date_start = calyear[0]*10000 + calmon[0]*100 + calday[0]
    date_end   = calyear[-1]*10000 + calmon[-1]*100 + calday[-1]
    

    for scale in range(1,5):
        for year in range(calyear[0], calyear[-1]+1):
            for mon in range(1,13):
                initial_date = datetime(year,mon,1)
                #print(to_integer(initial_date))
                end_date = initial_date + relativedelta(months=scale) - relativedelta(days=1)
                #print(to_integer(end_date))

                test_day = to_integer(end_date)
                #print(test_day)

                if test_day > date_end:
                    #print('aaa')
                    break
                else:
                    d1, d2 = index_between_dates(str(date_start), str(date_end), datetime.strftime(initial_date,'%Y%m%d'), \
                    datetime.strftime(end_date,'%Y%m%d'), 'days')
                    #print(d1,d2)
                
                    cut_bin = pr_bin[d1: d2+1]
                    A = comp_dryspell(cut_bin, scale)
                    print(mun_name[s], scale, year, mon)
                    print(cut_bin)
                    print(A)
                    input()
                
#Veranico grau 1:   3-5 days
#Veranico grau 2:  6-10 days
#Veranico grau 3: 11-15 days
#Veranico grau 4: 16-20 days
#Veranico grau 5: 21-inf days


# for m in range(len(mun_name)):
    
#     for y in range(46):
        
#         id = np.where(calyearm == y+1973)[0]
#         if np.sum( ~np.isnan(nddm[m, id]))>7:
#             ndd_annual[m, y] = np.nansum(nddm[m, id])

#     for c,ii in enumerate([2, 3, 4, 6 ]):
    
#         ndd_full[c,m, :] = sum_months(nddm[m, :], ii )
#     #print(ndd_annual[m, :])

# np.save('ndd_full.npy', ndd_full)
# np.save('ndd_full.npy', ndd_annual)

# def count_nddm(dbin, start_date, end_date):
#     cook = []
#     for ii,y in enumerate(range(start_year, end_year+1)):
#         for m in range(12):
#             [mon, lday ] = monthrange(y,m+1)

#             if y*10000+(m+1)*100+lday > end_date:
#                 break
#             else:
            
#                 d1, d2 = index_between_dates(str(start_date), str(end_date), '{0}{1:02d}01'.format(y,m+1), '{0}{1:02d}{2}'.format(y,m+1,lday), 'days')
 
#                 aux = dbin[d1:d2+1]

#                 if np.sum(~np.isnan(aux)) >= 21:
#                     cook.append(np.nansum(aux))
#                 else:
#                     cook.append(np.nan)
#             #    print(len(cook))
#     return np.array(cook)
