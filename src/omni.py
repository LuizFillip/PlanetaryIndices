import pandas as pd
import datetime as dt
import numpy as np 
import base as b 


INDEX_PATH = 'database/indices/omni_hourly.txt'
FORMAT_PATH = 'database/indices/omni_format_hourly.txt'


def dt2dttime(y, d, hour):
    dn = (dt.date(int(y), 1, 1) + 
          dt.timedelta(int(d) - 1))
    return dt.datetime(
        dn.year, 
        dn.month, 
        dn.day, 
        int(hour)
        )

def doy2date(df):
    return (dt.date(int(df.year), 1, 1) + 
            dt.timedelta(int(df.doy) - 1))

def set_names():

    f = open(FORMAT_PATH).readlines()
    
    names = {}
    for i in f:
        ln = i.split()
        
        try:
            name =  ln[1].replace('index', '').replace('_', '')
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
        
    df.index =  (pd.to_datetime(df['date']) +
                 pd.to_timedelta(df['hour'], unit='h'))
    
    df.drop(
        columns = ['year', 'doy', 'hour', 'date'], 
        inplace = True
        )
    return df
    

def process(infile):
    try:
        names = set_names().values()
        ds = OMNI2(infile, names)
        
        ds.to_csv(infile)
        
    except:
        print('file already convert')
        pass
    

# process(INDEX_PATH )


# names = set_names().values()
# ds = OMNI2(INDEX_PATH, names)

# ds