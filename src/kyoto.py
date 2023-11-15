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
    
    df.drop(
        columns = ["date", "time", "doy"], 
        inplace = True
        )
    
    return df

    