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

'''
def comp_dryspell(dados_bin, scale):
    dry = np.full((19, 2), np.nan)
    if np.sum(~np.isnan(dados_bin)) > 21*scale :
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
        #print(dummy)     
        
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
                        #  municipios   scales years months lengths [ lenghts freqency ]
dry_spell_freq = np.full((len(municipios), 4, nyear, 12, 19, 2), np.nan)

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
                    dry_spell_freq[s, scale-1, year-calyear[0],mon-1, ...] = comp_dryspell(cut_bin, scale)
#                    print(mun_name[s], scale, year, mon)
#                    print(cut_bin)
#                    print(comp_dryspell(cut_bin, scale))

np.save('dry_spell_freq_197301_201907_1-4months.npy', dry_spell_freq) 
                
#Veranico grau 1:   3-5 days
#Veranico grau 2:  6-10 days
#Veranico grau 3: 11-15 days
#Veranico grau 4: 16-20 days
#Veranico grau 5: 21-inf days

'''

dry_freq = np.load('dry_spell_freq_197301_201907_1-4months.npy')

print(dry_freq.shape)

def dry_spell_level(A):
    levs = [ 3,5, 6,10, 11,15, 16,20, 21,22 ]
    for lev in range(5):
        a = levs[lev*2] ; b = levs[lev*2+1]
        drylev[:, : ,: , :] = A[3,2,-2,2,a-2-1:b+1-2-1,1]
        print(drylev)
    return drylev
print(dry_freq[3,2,-2,2,:,:])

dry_spell_level(dry_freq)

