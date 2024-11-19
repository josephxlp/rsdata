import os
os.environ['USE_PYGEOS'] = '0'
import time 
import json
import requests as r
import getpass, time, os, cgi
import geopandas as gpd
from glob import glob 
from pprint import pprint


def get_urls(xmin,ymin, xmax, ymax):
    #https://forum.earthdata.nasa.gov/viewtopic.php?t=503#confirm_external_link-modal

    url_bounds = f'https://cmr.earthdata.nasa.gov/search/granules.json?short_name=ASTGTM&version=003&page_size=2000&pageNum=1&bounding_box={xmin},{ymin},{xmax},{ymax}'
    req = r.get(url_bounds).json()['feed']['entry'] 
    fileList = [g['links'][0]['href'] for g in req] 
    return fileList

def get_tilename(ymin, xmin):
    if ymin > 0 :
        ta = f'N{ymin}'
        if len(ta) != 3:
            ta = f'N0{ymin}'
    elif ymin < 0: 
        ta = f'S{abs(ymin)}'
        if len(ta) != 3:
            ta = f'S0{ymin}'

    if xmin > 0 : 
        tb = f'E{xmin}'
        if len(tb) == 3: tb = f'E0{xmin}'
        elif len(tb) == 2:tb = f'E00{xmin}'
        elif len(tb) == 1:tb = f'E000{xmin}'

    elif xmin < 0: 
        tb = f'W{xmin}'
        if len(tb) == 3: tb = f'W0{xmin}'
        elif len(tb) == 2:tb = f'W00{xmin}'
        elif len(tb) == 1:tb = f'W000{xmin}'

    ta = ta.replace('-', '0')
    tb = tb.replace('-', '0')

    tile_name = f'{ta}_{tb}'
    return tile_name

def write_list2txt(tile_name_txt, url_list):
    with open(tile_name_txt, 'w') as T:
        for url in url_list:
            T.write(url+'\n')

def download_data_from_urllist(tile_name_txt,uname,pword):
    os.chdir(os.path.dirname(tile_name_txt))
    cmd = f'wget --user={uname} --password={pword} -i {tile_name_txt}'
    os.system(cmd)

# url_list = get_urls(xmin,ymin, xmax, ymax)
# write_list2txt(tile_name_txt, url_list)
# download_data_from_urllist(tile_name_txt)

