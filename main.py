# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 11:05:19 2022

@author: Luiz
"""
import datetime
import pandas as pd
import os 


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
        
        return datetime.date(year, month, day)
    
    aptimes_ = [int(num.strip()) for num in aptimes.split()]
    
    result.append(_str_to_date(date))
    result.extend(kptimes_)
    result.append(sumkp)
    result.extend(aptimes_)
    result.append(int(Ap.strip()))

    return (result)


def KpAp_indices_KyotoData(infile:str, 
                           filename: str, 
                           year: int = 2014) -> pd.DataFrame:

    with open(infile + filename) as f:
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
    
    """Read data from """
    df = pd.read_csv(infile + filename, 
                     header = 39, delim_whitespace=(True))
    
    
    df.index  = pd.to_datetime(dict(year = df['#YYY'], 
                                    month = df['MM'], 
                                    day = df['DD']))
    
    return df.loc[(df["#YYY"]  == year), [parameter]]




def SYM_ASY_Data(infile: str, 
                 filename: str, 
                 frequency = "1D"):
    
    '''IAGA-2002 format like'''
    
    df = pd.read_csv(infile + filename, 
                     header = 14, 
                     delim_whitespace = True)
    
    df.index = pd.to_datetime(df["DATE"] + " " + 
                              df["TIME"])
    
    df = df.loc[:, ["ASY-D", "ASY-H", 
                    "SYM-D", "SYM-H"]]
    
    df = df.resample(frequency).asfreq()
    
    return df

def concat_files(infile: str, 
                 save = True) -> pd.DataFrame:
    
    _, _, files  = next(os.walk(infile))

    out = []
    for filename in files:
        
        out.append(SYM_ASY_Data(infile, 
                                filename))
    
    df = pd.concat(out)
    
    if save:
        df.to_csv("Database/asy_sym.txt", 
                      index = True, 
                      sep = " ")
        
    else:
        return df

def main():
    infile = "Database/ASY/"
    
    df = concat_files(infile, save = True)
    
    
    
#main()