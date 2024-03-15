def is_int(ln):
    try:
        int(ln)
        return True
    except:
        return False

file = 'indices/src/omni/data/omni2.text'


import pandas as pd

# df = pd.read_csv(file, delim_whitespace = True)

# df

ln = open(file).read()

start = ln.find('OMNI2_YYYY.DAT FORMAT DESCRIPTION')
end = ln.find(' C O M M E N T S')
lines = ln[start: end].split('\n')[3:-3]

out = {}
for ln in lines:
     
    if is_int(ln[:2]):
        index = int(ln[:2])
        
        
        
        if index <= 17:
            meaning = ln[22:57].strip()
            nits_comments = ln[57:]
        elif index >= 18 and index <= 22:
            meaning = ln[22:37].strip()
            units_comments = ln[37:]
        else:
            meaning = ln[22:37].strip()
            
        out[index] = {
            'format': ln[2:13].strip(), 
            'fill_value': ln[13:22].strip(),
            'meaning': meaning
            }

    
out 
  