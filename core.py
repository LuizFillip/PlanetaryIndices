import datetime as dt
import pandas as pd
import os 
from build import paths as p 

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


def KpAp_KyotoData(infile:str, 
                           year: int = 2014) -> pd.DataFrame:

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


def OMNI2Data(infile: str, 
              year: int = 2014, 
              parameter:str = "dst") -> pd.DataFrame:
    
    
    names =  ["year", "doy", "hour", 
              "B", "kp", 
              "dst", "ap", "f107", 
              "ae", "al", "au"]
    
    df = pd.read_csv(infile, 
                     header = None, 
                     names = names, 
                     delim_whitespace = True)
    
    
    df["kp"] = df["kp"] / 10
    
    def doy2date(y: int, d:int) -> dt.date:
        return (dt.date(int(y), 1, 1) + 
                dt.timedelta(int(d) - 1))
    
    year_and_doy = zip(df.year.values, df.doy.values)
  
    df.index = pd.to_datetime([doy2date(y, d) 
                               for y, d in year_and_doy])
    
    if parameter == None: parameter = names[3:]
      

    return df.loc[(df["year"]  == year), parameter]



def postdamData(infile: str):
    
    """Read data from GFZ postdam"""
    df = pd.read_csv(infile, 
                     header = 39, 
                     delim_whitespace = True)
    
    
    df.index  = pd.to_datetime(dict(year = df['#YYY'], 
                                    month = df['MM'], 
                                    day = df['DD']))
    
    df = df.drop(columns = ["#YYY", "MM", "DD", 
                            "days", "days_m", 
                            "Bsr", "dB"])
    
    df["F10.7a"] = df["F10.7obs"].rolling(window = 81).mean()
    
    return df.loc[df["D"] == 2] 


    
class get_indices(object):
    
    def __init__(self, date = dt.date(2014, 1, 1)):
        
        files = p("PlanetaryIndices").files
        
        df = postdamData(files[-1])
        
        self.ts = df.loc[df.index.date == date, ]
    
    def get(self, parameter):
        return self.ts[parameter].item()
    
def main():
    print(get_indices().get("Ap"))
    
