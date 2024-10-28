import pandas as pd
import datetime as dt
import numpy as np 
import base as b 

PATH_DATA = 'database/indices/omni.txt'
PATH_FORMAT = 'database/indices/omni_format.txt'
INDEX_HR = 'database/indices/omni_hourly.txt'
FORMAT_HR = 'database/indices/omni_format_hourly.txt'


def dt2dttime(y, d, hour, minute):
    dn = (dt.date(int(y), 1, 1) + 
          dt.timedelta(int(d) - 1))
    return dt.datetime(
        dn.year, 
        dn.month, 
        dn.day, 
        int(hour), 
        int(minute)
        )

def doy2date(df):
    time = dt.timedelta(
        hours = int(df.hour), 
        minutes = int(df.minute)          
        )
    
    date = pd.to_datetime((
        dt.date(int(df.year), 1, 1) + 
        dt.timedelta(int(df.doy) - 1) 
        ) )
    return date + time

def set_names(FORMAT_PATH):

    f = open(FORMAT_PATH).readlines()
    
    names = {}
    for i in f:
        ln = i.split()
        
        try:
            name =  ln[1].replace('index', '').replace('_', '').replace(',', '')
            
            names[int(ln[0])] = name.replace('-', '').lower()
            
        except:
            continue
        
    return names

def OMNI2(
        infile:str, 
        names: list[str]
        ) -> pd.DataFrame:
    
    """
    
    See: https://omniweb.gsfc.nasa.gov/form/dx1.html
    """
    df = pd.read_csv(
        infile, 
        header = None, 
        names = names, 
        delim_whitespace = True
        )
    

    df['date'] =  df.apply(lambda x: doy2date(x), axis = 1)
        
    
    df.replace(
        (99999, 9999, 999.9), 
        np.nan, inplace = True
        )
    
    df.rename(
        columns = {'f10.7': 'f107'}, 
        inplace = True
        )

    df["f107a"] = df["f107"].rolling(window = 81).mean()

    df = df.interpolate()
    
    df['kp'] = df['kp'] / 9
    
    cols = [s.replace(',', '') for s in df.columns]
    
    df.columns =  cols
        
    df.index =  (
        pd.to_datetime(df['date']) +
        pd.to_timedelta(df['hour'], 
        unit='h')
        )
    
    df.drop(
        columns = ['year', 'doy', 'hour', 'date'], 
        inplace = True
        )
    return df
    

def process(PATH_DATA, PATH_FORMAT):
    try:
        names = set_names(PATH_FORMAT).values()
        ds = OMNI2(PATH_DATA, names)
        
        ds.to_csv(PATH_DATA)
        
    except:
        print('file already convert')
        pass
    


def process_omni(INDEX_PATH):
    df = b.load(INDEX_PATH)
    
    out = []
    
    for col in df.columns:
        
        a = df.groupby(df.index.date)[col]
        
        if col == 'dst':
            out.append(a.min())
        else:
            out.append(a.max())
    
    ds = pd.concat(out, axis = 1)
    
    ds.to_csv('database/indices/omni_pro2.txt')
    
    return ds
    
    
def try_load(INDEX_HR):
    return b.load(INDEX_HR)


# process(INDEX_HR, FORMAT_HR)

# df = process_omni(INDEX_HR)

# df


def process_high(year):
    
    high_path = 'database/indices/high_resolution/'

    path_format = high_path + 'format.txt'
    names = set_names(path_format).values()
    
    infile = f'{high_path}{year}.txt'
    
    df = pd.read_csv(
         infile, 
         header = None, 
         names = names, 
         delim_whitespace = True
         )
          
    df.rename(columns = {'day': 'doy'}, inplace = True)
    
    df.index =  df.apply(lambda x: doy2date(x), axis = 1)
    
    df.replace(
        (99999, 9999, 999.9), 
        np.nan, inplace = True
        )
    
    return df.iloc[:, 4:]



from tqdm import tqdm 

def run_high_resolution():

    for year in tqdm(range(2013, 2024)):
        path_to_save = f'database/indices/omni_high/{year}'
        
        process_high(year).to_csv(path_to_save)
        
        
# run_high_resolution()

