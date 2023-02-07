import math


def roundup(x):
    return int(math.ceil(x / 10.0)) * 10
    
def compute_ticks(values, factor = 3):
    
    vmin = roundup(min(values))
    vmax = roundup(max(values))
    step = roundup((vmax - vmin) / factor)
    
    return vmin, vmax, step