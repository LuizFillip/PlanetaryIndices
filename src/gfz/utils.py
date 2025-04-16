
def hourly_kp_from_postdam():
    
    infile = "database/PlanetaryIndices/postdam.txt"
    
    df = postdam(infile)
  
    out = []
    index = []
    for dn in df.index:
        hrs = pd.date_range(dn, periods = 8, freq = "3H")
        for i in range(len(hrs)):
            out.append(df.loc[
                dn, f'Kp{i + 1}'])
            index.append(hrs[i])
            
            
    ds = pd.DataFrame({"Kp": out}, index = index)
    
    ds.to_csv("database/PlanetaryIndices/Kp_hourly.txt")
    
    
def save_solar_flux():
    save_in = "database/PlanetaryIndices/solar_flux.txt"
    infile = 'database/PlanetaryIndices/postdam.txt'   
    df = postdam(infile)
    
    df[['F10.7obs', 
        'F10.7adj', 
        'F10.7a']].to_csv(save_in)


def reapeat_for_time(dn, df):
    
    delta = dt.timedelta(hours = 23, minutes = 44)
    
    times = pd.date_range(dn, dn + delta, freq = '10min')
    
    ds = df.loc[df.index == dn]
    
    ds_repeat = ds.reindex(
        ds.index.repeat(len(times))
        )
    
    ds_repeat.index = times
    
    return ds_repeat

def repeat_values_in_data(df):

    out = [reapeat_for_time(dn, df) for dn in df.index]
        
    return pd.concat(out)
    




def save_only(df):
    
    df['kp'] = df[['Kp1', 'Kp2', 'Kp3', 
                   'Kp4', 'Kp5', 'Kp6',
                   'Kp7', 'Kp8']].max(axis = 1)
    
   
    df[['F10.7adj', 'kp', 
        'Ap', 'F10.7a']].to_csv(
            'database/PlanetaryIndices/kp_postdam.txt')
    # dialy = gd.GFZ()

    # dialy.to_csv('database/indices/indeces.txt')