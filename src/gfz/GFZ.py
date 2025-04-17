import datetime as dt
import pandas as pd

POSTDAM_PATH = 'indices/src/gfz/kpdata.txt'

columns = [
    'YYY',
     'MM',
     'DD',
 'days',
     'days_m',
     'Bsr',
     'dB',
     'Kp1',
     'Kp2',
     'Kp3',
     'Kp4',
     'Kp5',
     'Kp6',
     'Kp7',
     'Kp8',
     'ap1',
     'ap2',
     'ap3',
     'ap4',
     'ap5',
     'ap6',
     'ap7',
     'ap8',
     'Ap',
     'SN',
     'F10.7obs',
     'F10.7adj',
     'D']

    


    
class GFZ(object):
    
    def __init__(self, date = dt.date(2014, 1, 1)):
        
        df = pd.read_csv(
            POSTDAM_PATH, 
            delim_whitespace = True, 
            comment = '#', 
            header = None,
            names = columns
            )

        df.index = pd.to_datetime(
            df[['YYY', 'MM', 'DD']].rename(
                columns = {
                    'YYY': 'year', 
                    'MM': 'month', 
                    'DD': 'day'
                    }
                )
            )

        df = df.iloc[:, 7:] 

        df["F10.7a"] = df["F10.7obs"].rolling(window = 81).mean()

        df = df.loc[df["D"] == 2] 
        
        self.ts = df.loc[df.index.date == date, ]
        self.df = df
    def get(self, parameter):
        return self.ts[parameter].item()
    
def main():
    
    vls = GFZ().get('F10.7a')
    
    print(vls)