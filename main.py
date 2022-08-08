# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 11:05:19 2022

@author: Luiz
"""
import datetime
import pandas as pd

def row(contents: str):
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
        
        return datetime.date(year, month, day)
    
    aptimes_ = [int(num.strip()) for num in aptimes.split()]
    
    result.append(_str_to_date(date))
    result.extend(kptimes_)
    result.append(sumkp)
    result.extend(aptimes_)
    result.append(int(Ap.strip()))

    return (result)


def KyotoData(infile:str = "Database/PlanetaryIndicators/", 
              filename: str = "Kp.txt", 
              year: int = 2014) -> pd.DataFrame:

    with open(infile + filename) as f:
        data = [line.strip() for line in f.readlines()]
        
    outside = []
    
    for num in range(1, len(data)):
        contents = data[num]
    
        outside.append(row(contents))
        
    
    names = ["date", 'kp0', 'kp3', 
                 'kp6', 'kp9', 'kp12', 
                 'kp15', 'kp18', 'kp21',
                 'kpsum', 'ap3', 'ap6', 
                 'ap9', 'ap12', 'ap15', 
                 'ap18', 'ap21', 'ap24', "Ap"]
    
    df = pd.DataFrame(outside, columns = names)
    
    df.index = pd.to_datetime(df["date"])
    
    df = df.loc[df.index.year == year, :]
    return df


def OMNI2Data(infile: str, 
              filename: str,
              year: int = 2014, 
              parameter:str = "dst") -> pd.DataFrame:
    
    
    names =  ["year", "doy", "hour", "kp", 
              "dst", "ap", "f107", 
              "ae", "al", "au"]
    
    df = pd.read_csv(infile + filename, 
                     header = None, 
                     names = names, 
                     delim_whitespace = True)
    
    
    df["kp"] = df["kp"] / 10
    dates = []
    
    def doy_to_date(y: int, d:int) -> datetime.date:
        
        return (datetime.date(int(y), 1, 1) + 
                datetime.timedelta(int(d) - 1))
    
    year_and_doy = zip(df.year.values, df.doy.values)
  
    df.index = [doy_to_date(y, d) for y, d in year_and_doy]
    
    if parameter == None:
       parameter = names[3:]

    return df.loc[(df["year"]  == year), parameter]



def postdamData(infile:str, 
                filename:str, 
                parameter:str = "Ap", 
                year:int = 2014):
    
    
    df = pd.read_csv(infile + filename, 
                     header = 39, delim_whitespace=(True))
    
    
    df.index  = pd.to_datetime(dict(year = df['#YYY'], 
                                    month = df['MM'], 
                                    day = df['DD']))
    
    return df.loc[(df["#YYY"]  == year), [parameter]]