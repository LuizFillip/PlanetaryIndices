import datetime as dt
import pandas as pd

def extract_rows(contents: str):
    result = []
    
    date = contents[:8]
    kptimes = contents[9:25]
    sumkp = contents[25:28]
    aptimes = contents[28:52]
    Ap = contents[52:55] 
    
    kptimes_ = [kptimes[num: num + 2].strip() 
                for num in range(0, len(kptimes), 1) 
                if (num % 2) == 0]
    
    def _str_to_date(string_date):
        
        year = int(string_date[:4])
        month = int(string_date[4:6])
        day = int(string_date[6:8])
        
        return dt.date(year, month, day)
    
    aptimes_ = [int(num.strip()) for num in aptimes.split()]
    
    result.append(_str_to_date(date))
    result.extend(kptimes_)
    result.append(sumkp)
    result.extend(aptimes_)
    result.append(int(Ap.strip()))

    return (result)


def KpAp_Kyoto(
        infile: str, 
        year: int = 2014
        ) -> pd.DataFrame:

    with open(infile) as f:
        data = [line.strip() for line in f.readlines()]
        
    outside = []
    
    for num in range(1, len(data)):
        contents = data[num]
    
        outside.append(extract_rows(contents))
        
    
    names = ["date", 'kp0', 'kp3', 
            'kp6', 'kp9', 'kp12', 
            'kp15', 'kp18', 'kp21',
            'kpsum', 'ap3', 'ap6', 
            'ap9', 'ap12', 'ap15', 
            'ap18', 'ap21', 'ap24', "Ap"]
    
    df = pd.DataFrame(outside, columns = names)
    
    df.index = pd.to_datetime(df["date"])
    
    return df.loc[df.index.year == year, :]

def postdam(infile: str):
    
    """Read data from GFZ postdam"""
    df = pd.read_csv(infile, 
                     header = 39, 
                     delim_whitespace = True)
    
    
    df.index  = pd.to_datetime(dict(year = df['#YYY'], 
                                    month = df['MM'], 
                                    day = df['DD']))
    
    df = df.drop(
        columns = ["#YYY", "MM", "DD", 
                   "days", "days_m", 
                   "Bsr", "dB"])
    
    df["F10.7a"] = df["F10.7obs"].rolling(window = 81).mean()
    
    return df.loc[df["D"] == 2] 


    
class get_indices(object):
    
    def __init__(self, date = dt.date(2014, 1, 1)):
        
        infile = "database/PlanetaryIndices/postdam.txt"
        
        df = postdam(infile)
        
        self.ts = df.loc[df.index.date == date, ]
    
    def get(self, parameter):
        return self.ts[parameter].item()
    
def hourly_kp_from_postdam():
    infile = "database/PlanetaryIndices/postdam.txt"
    
    df = postdam(infile)
  
    out = []
    index = []
    for dn in df.index:
        hrs = pd.date_range(dn, periods = 8, freq = "3H")
        for i in range(len(hrs)):
            out.append(df.loc[dn, f'Kp{i + 1}'])
            index.append(hrs[i])
            
            
    ds = pd.DataFrame({"Kp": out}, index = index)
    
    ds.to_csv("database/PlanetaryIndices/Kp_hourly.txt")
    
    
def save_solar_flux():
    save_in = "database/PlanetaryIndices/solar_flux.txt"
    infile = 'database/PlanetaryIndices/postdam.txt'   
    df = postdam(infile)
    
    df[['F10.7obs', 
        'F10.7adj', 
        'F10.7a']].to_csv(save_in)


def reapeat_for_time(dn, df):
    
    delta = dt.timedelta(hours = 23, minutes = 44)
    
    times = pd.date_range(dn, dn + delta, freq = '10min')
    
    ds = df.loc[df.index == dn]
    
    ds_repeat = ds.reindex(
        ds.index.repeat(len(times))
        )
    
    ds_repeat.index = times
    
    return ds_repeat

def repeat_values_in_data(df):

    out = [reapeat_for_time(dn, df) for dn in df.index]
        
    return pd.concat(out)
    

def sel_dates(df):

    start = dt.datetime(2013, 1, 1)
    end = dt.datetime(2013, 12, 31)
    
    df = df[(df.index >= start) & (df.index <= end)]


def save_only(df):
    
    df['kp'] = df[['Kp1', 'Kp2', 'Kp3', 'Kp4', 'Kp5', 'Kp6', 'Kp7', 'Kp8']].max(axis = 1)
    
   
    df[['F10.7adj', 'kp', 'Ap', 'F10.7a']].to_csv('database/PlanetaryIndices/kp_postdam.txt')
    
