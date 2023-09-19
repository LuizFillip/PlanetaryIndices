import pandas as pd
import datetime as dt
import numpy as np 


def dt2dttime(y, d, hour, minute):
    dn = (dt.date(int(y), 1, 1) + dt.timedelta(int(d) - 1))
    return dt.datetime(
        dn.year, 
        dn.month, 
        dn.day, 
        int(hour), 
        int(minute)
        )

def doy2date(df):
    return dt.date(int(df.year), 1, 1) + dt.timedelta(int(df.doy) - 1)

def set_names(
        format_file =  'database/indices/omni_format.txt'
        ):

    f = open(format_file).readlines()
    
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
    

    df = pd.read_csv(
        infile, 
        header = None, 
        names = names, 
        delim_whitespace = True
        )
    
    df.index = df.apply(lambda x: doy2date(x), axis = 1)
    
    df.replace((99999, 9999, 999.9), 
               np.nan, inplace = True)
    
    df.rename(
        columns = {'f10.7': 'f107'}, 
        inplace = True
        )

    df["f107a"] = df["f107"].rolling(window = 81).mean()

    df = df.interpolate()
    
    df['kp'] = df['kp'] / 9
    
    cols = [s.replace(',', '') for s in df.columns]
    
    df.columns =  cols
    
    del df['hour']

    return df
    



infile = "database/indices/omni.txt"


def process(infile):
    try:
        names =  set_names().values()
        ds = OMNI2(infile, names)
        
        ds.to_csv(infile)
        
    except:
        print('file already convert')
        pass
    


def refix_parameters(df): 


    df['f10.7'].replace(999.9, np.nan, 
               inplace = True)
    
    df['kp'] = df['kp']/9
    
    cols = [s.replace(',', '') for s in df.columns]
    
    df.columns =  cols
    
    del df['hour']
