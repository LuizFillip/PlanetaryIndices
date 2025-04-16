import datetime as dt
import os 
import pandas as pd
import numpy as np


PYGLOW_PATH = os.path.dirname(__file__)

columns = [
    'YYY',
     'MM',
     'DD',
 'days',
     'days_m',
     'Bsr',
     'dB',
     'Kp1',
     'Kp2',
     'Kp3',
     'Kp4',
     'Kp5',
     'Kp6',
     'Kp7',
     'Kp8',
     'ap1',
     'ap2',
     'ap3',
     'ap4',
     'ap5',
     'ap6',
     'ap7',
     'ap8',
     'Ap',
     'SN',
     'F10.7obs',
     'F10.7adj',
     'D']

def GFZ():
    
    kpap = pd.read_csv(
        PYGLOW_PATH +'/kpap/Kp_ap_Ap_SN_F107_since_1932.txt',
        delim_whitespace = True, 
        comment = '#', 
        header = None,
        names = columns
        )
    
    hourly = {
        'kp': [], 
        'ap': []
        }
    
    hourly_index = []
    daily_index = []
    
    
    daily = {
        'kp_sum': [], 
        'ap_mean': [], 
        'kp_max': [],
        'ap_max': [], 
        'f107': []
        
        }
    
    for j in range(len(kpap)):
    
        vals = kpap.iloc[j, :].values
        
        year, month, day = tuple(int(x) for x in vals[:3])
        
        
        for i, hour in enumerate(range(0, 24, 3)):
            hourly_index.append(dt.datetime(year, month, day, hour))
        
            hourly['kp'].append(vals[7 + i])
            hourly['ap'].append(vals[15 + i])
            
        daily_index.append(dt.datetime(year, month, day))
        
        daily['kp_sum'].append(np.sum(vals[7:15]))
        daily['ap_mean'].append(np.mean(vals[15:23]))
        daily['kp_max'].append(np.max(vals[7:15]))
        daily['ap_max'].append(np.max(vals[15:23]))
        daily['f107'].append(vals[26])
           
    df_dialy = pd.DataFrame(daily, index = daily_index)
    #df_hourly = pd.DataFrame(hourly, index = hourly_index)
        
    df_dialy['f107'] = df_dialy['f107'].replace(
        (-1, 0), (np.nan, np.nan)
        )
    
    df_dialy['f107a'] = df_dialy['f107'].rolling(
        window = 81).mean()
    
    return df_dialy#, df_hourly


def get_kap():
    
    kpap = pd.read_csv(
        PYGLOW_PATH +'/kpap/Kp_ap_Ap_SN_F107_since_1932.txt',
        delim_whitespace = True, 
        comment = '#', 
        header = None,
        names = columns
        )
    
    kp = {}
    ae = {}
    
    daily_kp = {}
    daily_ae = {}
    
    f107 ={}
    f107a ={}
    
    for j in range(len(kpap)):
    
        vals = kpap.iloc[j, :].values
        
        year, month, day = tuple(int(x) for x in vals[:3])
        
        dn = dt.datetime(year, month, day)
        
        for i, hour in enumerate(range(0, 24, 3)):
            
            delta = dt.timedelta(hours = hour)
            kp[dn + delta] = vals[7 + i]
            ae[dn + delta] = vals[15 + i]
        
        daily_kp[dn] = np.sum(vals[7:15])
        daily_ae[dn] = np.mean(vals[15:23]
                                                     )
        
        try:
            temp = float(vals[26])  # f107
        except ValueError:
            temp = float('NaN')  # If the string is empty, just use NaN

        if temp == 0.:  # Replace 0's of f107 with NaN
            temp = float('NaN')

        if temp == -1:  # Replace -1's of f107 with NaN
            temp = float('NaN')

        f107[dt.datetime(year, month, day)] = temp
        
        # Caculate f107a:
    for dn, value in f107.items():
        f107_81values = []
        for dday in range(-40, 41):  # 81 day sliding window
            delta = dt.timedelta(dday)
            try:
                f107_81values.append(f107[dn+delta])
            except KeyError:
                f107_81values.append(float('NaN'))
        f107a[dn] = np.nan if all(np.isnan(f107_81values)) else \
            np.nanmean(f107_81values)

    return kp, daily_kp, ae, daily_ae, f107, f107a

import glob


# plt.plot(f107a.keys(), f107a.values())
# df_dialy['f107a'].plot()
def get_dst():
    
    dst = {}
    
    oldies = ['1957_1969', '1970_1989', '1990_2004']
    dst_path = '%s/dst/' % PYGLOW_PATH
    files = glob.glob('%s??????' % dst_path)  
    old_files = ['%s%s' % (dst_path, old) for old in oldies]
    files.extend(old_files)  # a list of every dst file
    for fn in files:
        with open(fn, 'r') as f:
            s = f.readlines()
        for x in s:
            if len(x) <= 1:
                break  # reached last line. Done with this file.
            yr23 = x[3:5]  # 3rd and 4th digits of year
            month = int(x[5:7])
            day = int(x[8:10])
            yr12 = x[14:16]  # 1st and 2nd digits of year
            base = int(x[16:20])  # "Base value, unit 100 nT"
            year = int('%02s%02s' % (yr12, yr23))
            dst_per_hour = np.zeros(24)
            for i in range(24):
                dsthr = base*100 + int(x[20+4*i:24+4*i])
                if dsthr == 9999:
                    dsthr = np.nan
                dst_per_hour[i] = dsthr
            dst[dt.datetime(year, month, day)] = dst_per_hour
            
    return dst

def get_ae():
    ae = {}
    
    
    ae_path = '%s/ae/' % PYGLOW_PATH
    files = glob.glob('%s*' % ae_path)  # find files like 1975
    for fn in files:
        with open(fn, 'r') as f:
            s = f.readlines()
            
        for x in s:
            if len(x) <= 1:
                break  
            dn, aehr = tuple(x.split())
        
            aehr = int(aehr)
            
            if aehr == 99999:
                aehr = np.nan
                
           
            hour = int(x[6:8])
            if hour == 0:
                ae_per_hour = np.zeros(24)
            aehr = int(x[8:14])
            if aehr == 99999:
                aehr = np.nan
            ae_per_hour[hour] = aehr
            ae[dt.datetime.strptime(dn, '%y%m%d%H')] = ae_per_hour
            
    return ae
    
