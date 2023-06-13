import pandas as pd
import datetime as dt
import numpy as np


names =  ["year", "doy", "hour", 
          "B", "kp", 
          "dst", "ap", "f107", 
          "ae", "al", "au"]

def OMNI2(infile: str, names) -> pd.DataFrame:
    

    df = pd.read_csv(infile, 
                     header = None, 
                     names = names, 
                     delim_whitespace = True)
    
        
    def dt2dttime(y, d, hour, minute):
        dn = (dt.date(int(y), 1, 1) + dt.timedelta(int(d) - 1))
        return dt.datetime(
            dn.year, 
            dn.month, 
            dn.day, 
            int(hour), 
            int(minute)
            )
    
    out = []
    for i in range(len(df)):
        y, d, h, m = tuple(df.iloc[i, slice(0, 4)].values)
        out.append(dt2dttime(y, d, h, m))
        
    df.index = out
              
    return df[names[4:]]
    
def main():
    infile = "database/PlanetaryIndices/omni.txt"
    
    df = OMNI2(infile)

    infile = "database/PlanetaryIndices/omni_2012_2015.lst"
    
    names =  ["year", "doy", "hour", 
              "minute", "Bavg", 
              "BY", "BZ", "Speed", 
              "Ey", "SymH"]
    
    df = OMNI2(infile, names)
    
    df.to_csv(infile)