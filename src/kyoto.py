import pandas as pd
import datetime as dt 

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


def process_kyoto_data(infile):
    f  = open(infile).readlines()
    out = []
    for num in range(len(f)):
        row = f[num].split()
       
        try:
            pd.to_datetime(row[0])
            out.append(row)
        except:
            continue
    
    df = pd.DataFrame(
        out, 
        columns = ["date", "time", 
                   "doy", "dst"]
        )
    
    df.index = pd.to_datetime(
        df["date"] + " " + df["time"]
        )
    
    df["dst"] = pd.to_numeric(df["dst"])
    
    df.drop(
        columns = ["date", "time", "doy"], 
        inplace = True
        )
    
    return df

    