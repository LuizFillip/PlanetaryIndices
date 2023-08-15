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

def _get_kap_f107_ap():
    
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
        'kp': [], 
        'ap': [],
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
        
        daily['kp'].append(np.sum(vals[7:15]))
        daily['ap'].append(np.mean(vals[15:23]))
        daily['f107'].append(vals[26])
           
    df_dialy = pd.DataFrame(daily, index = daily_index)
    df_hourly = pd.DataFrame(hourly, index = hourly_index)
        
    df_dialy['f107'] = df_dialy['f107'].replace(
        (-1, 0), (np.nan, np.nan)
        )
    
    df_dialy['f107a'] = df_dialy['f107'].rolling(
        window = 81).mean()
    
    return df_dialy, df_hourly


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
        
        for i, hour in enumerate(range(0, 24, 3)):
        
            kp[dt.datetime(year, month, day, hour)] = vals[7 + i]
            ae[dt.datetime(year, month, day, hour)] = vals[15 + i]
        
        daily_kp[dt.datetime(year, month, day)] = np.sum(vals[7:15])
        daily_ae[dt.datetime(year, month, day)] = np.mean(vals[15:23])
        
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
    
# kp= get_ae()





kp, daily_kp, ap, daily_ap, f107, f107a = get_kap()

ae = get_ae()
dst = get_dst()
END_YEAR = dt.date.today().year + 1
EPOCH = dt.datetime(1932, 1, 1)

end_day = dt.datetime.today()
total_days = (end_day - EPOCH).days + 1


total_days = len(kp.keys())
geophysical_indices = np.zeros((68, total_days))*float('nan')


for j in range(total_days - 1):
    for i, hour in enumerate(range(0, 24, 3)):
    
        dn = EPOCH + dt.timedelta(j) 
        try:
            geophysical_indices[i, j] = kp[
                dt.datetime(dn.year, dn.month, dn.day, hour)
                ]
            geophysical_indices[i + 8, j] = ap[
                dt.datetime(dn.year, dn.month, dn.day, hour)
                ]
            
            geophysical_indices[18, j] = daily_kp[
                dt.datetime(dn.year, dn.month, dn.day)
                ]
            geophysical_indices[19, j] = daily_ap[
                dt.datetime(dn.year, dn.month, dn.day)
                ]
        except KeyError:
            pass
        
        try:  # This will fail if no f10.7 data are available on this day
            geophysical_indices[16, j] = f107[
                dt.datetime(dn.year, dn.month, dn.day)
                ]
            geophysical_indices[17, j] =  f107a[
                dt.datetime(dn.year, dn.month, dn.day)
                ]
        except KeyError:
            pass

        try:  # This will fail if no dst data are available on this day
            geophysical_indices[20:44, j] = dst[dn]
        except KeyError:
            pass

        try:  # This will fail if no ae data are available on this day
            geophysical_indices[44:68, j] = ae[dn]
        except KeyError:
            pass
        
def get_mtime_table():
    """

    """
    mtime_table = {}

    # kpap files:
    for y in range(1932, END_YEAR):
        fn = PYGLOW_PATH + "/kpap/%4i" % y
        if os.path.isfile(fn):
            mtime_table[fn] = os.path.getmtime(fn)

    # dst files:
    oldies = ['1957_1969', '1970_1989', '1990_2004']
    dst_path = '%s/dst/' % PYGLOW_PATH
    files = glob.glob('%s??????' % dst_path)  # files like 201407
    old_files = [
        '%s%s' % (dst_path, old) for old in oldies
    ]  # older files listed above
    files.extend(old_files)  # a list of every dst file
    for fn in files:
        mtime_table[fn] = os.path.getmtime(fn)

    # ae files:
    ae_path = '%s/ae/' % PYGLOW_PATH
    files = glob.glob('%s*' % ae_path)  # find files like 1975
    for fn in files:
        mtime_table[fn] = os.path.getmtime(fn)

    return mtime_table

# File to store table of index file modification times:
# MTIME_TABLE_FNAME = os.path.join(PYGLOW_PATH, 'mtime_table.pkl')

# # File to store cached geophysical_indices array:
# GEOPHYSICAL_INDICES_FNAME = os.path.join(
#     PYGLOW_PATH,
#     'geophysical_indices.npy',
# )
# # from pickle import load, dump

# # with open(MTIME_TABLE_FNAME, 'wb') as fid:
# #     mtime_table = load(fid)
# #     dump(mtime_table, fid, -1)
# print("[generate_kpap.py] Generated: {}".format(GEOPHYSICAL_INDICES_FNAME))

# np.save(GEOPHYSICAL_INDICES_FNAME, geophysical_indices)

# geophysical_indices