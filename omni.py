import pandas as pd
import datetime as dt

def OMNI2(infile: str, 
              year = None, 
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
      
    if year is not None:
        return df.loc[(df["year"]  == year), parameter]
    else:
        return df
    
def main():
    infile = "database/PlanetaryIndices/omni.txt"
    
    df = OMNI2(infile)
    
    df = df[(df.index > dt.datetime(2013, 3, 15)) &
            (df.index < dt.datetime(2013, 3, 20))]
    
    df