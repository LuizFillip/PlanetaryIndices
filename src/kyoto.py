import pandas as pd

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
    
    df.drop(columns = ["date", "time", "doy"], 
            inplace = True)
    
    return df

infile = "database/indices/kyoto2000.txt"


def process(infile):
    try:
    
        ds = process_kyoto_data(infile)
        
        ds.to_csv(infile)
        
    except:
        print('file already convert')
        pass
    