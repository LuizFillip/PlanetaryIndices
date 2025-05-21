import os
import urllib.request

DIR_FILE = os.path.dirname(__file__)

src = 'omni2_2023.dat'
src = 'omni2.text'
url = f'https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/{src}'
dst = f'indices/src/omni/data/{src}'
urllib.request.urlretrieve(url, dst)
