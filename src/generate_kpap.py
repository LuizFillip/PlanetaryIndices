from __future__ import division
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from datetime import datetime, timedelta, date
from pickle import load, dump
import numpy as np
import os
from numpy import nanmean
import sys
import glob
import pandas as pd


END_YEAR = date.today().year + 1
EPOCH = datetime(1932, 1, 1)
PYGLOW_PATH = os.path.dirname(__file__)
if not PYGLOW_PATH:  # Corner case: we are in the installation directory
    PYGLOW_PATH = './'

# File to store table of index file modification times:
MTIME_TABLE_FNAME = os.path.join(PYGLOW_PATH, 'mtime_table.pkl')

# File to store cached geophysical_indices array:
GEOPHYSICAL_INDICES_FNAME = os.path.join(
    PYGLOW_PATH,
    'geophysical_indices.npy',
)

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


def update_required():
    """
    Determines if new data are available to index into geophysical_indices.npy
    """
    if not os.path.isfile(MTIME_TABLE_FNAME):
        return True
    else:
        with open(MTIME_TABLE_FNAME, 'rb') as fid:
            mtime_table = load(fid)
        new_mtime_table = get_mtime_table()
        for key, val in new_mtime_table.items():
            try:
                if mtime_table[key] != new_mtime_table[key]:
                    return True
            except (IndexError, KeyError):
                # Differing keys in mtime_tables,
                # so we need to update:
                return True
        # All current file modification times matched those associated
        # with cached geophysical_indices
        return False


def generate_kpap():


    print('[generate_kpap.py] Generating geophysical indices table...')
    
    # Files have changed --- update geophysical indices"""
    mtime_table = get_mtime_table()
    
    """ Part 1: Parsing the raw data files """
    # Create empty dictionaries:
    ap = {}
    kp = {}
    f107 = {}
    daily_kp = {}
    daily_ap = {}
    f107a = {}
    dst = {}
    ae = {}
    
    kpap = pd.read_csv(PYGLOW_PATH +'/kpap/Kp_ap_Ap_SN_F107_since_1932.txt',
                       delim_whitespace=True, comment='#', header=None)
    for i in range(len(kpap)):
        vals = kpap.loc[i]
        year = int(vals[0])
        month = int(vals[1])
        day = int(vals[2])
        kp[datetime(year, month, day, 0)] = vals[7]
        kp[datetime(year, month, day, 3)] = vals[8]
        kp[datetime(year, month, day, 6)] = vals[9]
        kp[datetime(year, month, day, 9)] = vals[10]
        kp[datetime(year, month, day, 12)] = vals[11]
        kp[datetime(year, month, day, 15)] = vals[12]
        kp[datetime(year, month, day, 18)] = vals[13]
        kp[datetime(year, month, day, 21)] = vals[14]
    
        ap[datetime(year, month, day, 0)] = vals[15]
        ap[datetime(year, month, day, 3)] = vals[16]
        ap[datetime(year, month, day, 6)] = vals[17]
        ap[datetime(year, month, day, 9)] = vals[18]
        ap[datetime(year, month, day, 12)] = vals[19]
        ap[datetime(year, month, day, 15)] = vals[20]
        ap[datetime(year, month, day, 18)] = vals[21]
        ap[datetime(year, month, day, 21)] = vals[22]
    
        daily_kp[datetime(year, month, day)] = np.sum(vals[7:15])
        daily_ap[datetime(year, month, day)] = np.mean(vals[15:23])
    
        try:
            temp = float(vals[26])  # f107
        except ValueError:
            temp = float('NaN')  # If the string is empty, just use NaN
    
        if temp == 0.:  # Replace 0's of f107 with NaN
            temp = float('NaN')
    
        if temp == -1:  # Replace -1's of f107 with NaN
            temp = float('NaN')
    
        f107[datetime(year, month, day)] = temp
    del kpap
    
    # Caculate f107a:
    for dn, value in f107.items():
        f107_81values = []
        for dday in range(-40, 41):  # 81 day sliding window
            dt = timedelta(dday)
            try:
                f107_81values.append(f107[dn+dt])
            except KeyError:
                f107_81values.append(float('NaN'))
        f107a[dn] = np.nan if all(np.isnan(f107_81values)) else \
            np.nanmean(f107_81values)
    
    # Read in DST values.
    # (1) Read old files that were shipped with pyglow.
    # (2) Search the dst/ folder for all new files, and read them.
    oldies = ['1957_1969', '1970_1989', '1990_2004']
    dst_path = '%s/dst/' % PYGLOW_PATH
    files = glob.glob('%s??????' % dst_path)  # files like 201407
    # Older files listed above:
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
            dst[datetime(year, month, day)] = dst_per_hour
    
    # Read in AE values.
    ae_path = '%s/ae/' % PYGLOW_PATH
    files = glob.glob('%s*' % ae_path)  # find files like 1975
    for fn in files:
        with open(fn, 'r') as f:
            s = f.readlines()
        for x in s:
            if len(x) <= 1:
                break  # reached last line. Done with this file.
            yr23 = int(x[0:2])  # 3rd and 4th digits of year
            month = int(x[2:4])
            day = int(x[4:6])
            year = int(fn.split("/")[-1][:4])
            # in case file contains an extra day:
            if yr23 != int(str(year)[2:4]):
                break
            hour = int(x[6:8])
            if hour == 0:
                ae_per_hour = np.zeros(24)
            aehr = int(x[8:14])
            if aehr == 99999:
                aehr = np.nan
            ae_per_hour[hour] = aehr
            ae[datetime(year, month, day)] = ae_per_hour
    
    """ Part 2: placing indices in 'geophysical_indices' array """
    # time to put the values into a numpy array, geophysical_indices
    end_day = datetime.today()
    total_days = (end_day-EPOCH).days+1
    geophysical_indices = np.zeros((68, total_days))*float('nan')
    
    i = 0
    while i < total_days:  # Try every day. Some will be NaN.
        dn = EPOCH + timedelta(i)  # Increment a day
    
        try:  # This will fail if kp/ap data doesn't exist on this day:
            geophysical_indices[0, i] = \
                kp[datetime(dn.year, dn.month, dn.day, 0)]
            geophysical_indices[1, i] = \
                kp[datetime(dn.year, dn.month, dn.day, 3)]
            geophysical_indices[2, i] = \
                kp[datetime(dn.year, dn.month, dn.day, 6)]
            geophysical_indices[3, i] = \
                kp[datetime(dn.year, dn.month, dn.day, 9)]
            geophysical_indices[4, i] = \
                kp[datetime(dn.year, dn.month, dn.day, 12)]
            geophysical_indices[5, i] = \
                kp[datetime(dn.year, dn.month, dn.day, 15)]
            geophysical_indices[6, i] = \
                kp[datetime(dn.year, dn.month, dn.day, 18)]
            geophysical_indices[7, i] = \
                kp[datetime(dn.year, dn.month, dn.day, 21)]
    
            geophysical_indices[8, i] = \
                ap[datetime(dn.year, dn.month, dn.day, 0)]
            geophysical_indices[9, i] = \
                ap[datetime(dn.year, dn.month, dn.day, 3)]
            geophysical_indices[10, i] = \
                ap[datetime(dn.year, dn.month, dn.day, 6)]
            geophysical_indices[11, i] = \
                ap[datetime(dn.year, dn.month, dn.day, 9)]
            geophysical_indices[12, i] = \
                ap[datetime(dn.year, dn.month, dn.day, 12)]
            geophysical_indices[13, i] = \
                ap[datetime(dn.year, dn.month, dn.day, 15)]
            geophysical_indices[14, i] = \
                ap[datetime(dn.year, dn.month, dn.day, 18)]
            geophysical_indices[15, i] = \
                ap[datetime(dn.year, dn.month, dn.day, 21)]
    
            geophysical_indices[18, i] = \
                daily_kp[datetime(dn.year, dn.month, dn.day)]
            geophysical_indices[19, i] = \
                daily_ap[datetime(dn.year, dn.month, dn.day)]
    
        except KeyError:
            pass
    
        try:  # This will fail if no f10.7 data are available on this day
            geophysical_indices[16, i] = \
                f107[datetime(dn.year, dn.month, dn.day)]
            geophysical_indices[17, i] = \
                f107a[datetime(dn.year, dn.month, dn.day)]
        except KeyError:
            pass
    
        try:  # This will fail if no dst data are available on this day
            geophysical_indices[20:44, i] = dst[dn]
        except KeyError:
            pass
    
        try:  # This will fail if no ae data are available on this day
            geophysical_indices[44:68, i] = ae[dn]
        except KeyError:
            pass
    
        i = i + 1
    
    # Update file cache:
    with open(MTIME_TABLE_FNAME, 'wb') as fid:
        dump(mtime_table, fid, -1)
    np.save(GEOPHYSICAL_INDICES_FNAME, geophysical_indices)
    print("[generate_kpap.py] Generated: {}".format(GEOPHYSICAL_INDICES_FNAME))
    
    # update = update_required()
    
    # print(update)
    
    # if update:
    #     # Fetch indices (it will also save a file):
    #     geophysical_indices = generate_kpap()
    # else:
    #     # Update not required, load cached indices:
    #     geophysical_indices = np.load(GEOPHYSICAL_INDICES_FNAME)
    
    
    
    # def fetch():
    #     """
    #     Main interface to retrieve geophysical indices
    
    #     :return geophysical_indices: data structure containing geophysical indices
    
    #     """
    
    #     # Do we need to update / generate a file?
        
    
    #     return geophysical_indices
    # generate_kpap()
    
    # Files have changed --- update geophysical indices"""
    
