import os 
import ee 
import geemap
import time 
from upaths import patches_dpath, sentinel2_dpath
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import geopandas as gpd 
from geeutils import download_sentinel2

try:
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
except:
    ee.Authenticate()
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')

cpus = int(os.cpu_count() * 0.75)
band_codes = ['B4', 'B3', 'B2']#,'B8','B11']
band_names = ['Red', 'Green', 'Blue']#, 'NIR', 'SWIR1']
scale = 30 
#name = 'S2_RGBNS1'
name = 'S2_RGB'

gpkg_files = sorted(glob(f'{patches_dpath}/*.gpkg'),reverse=True)
gpkg_files
if __name__ == '__main__':
    ti = time.perf_counter()
    for i in range(len(gpkg_files)):
        #if i > 0 : break
        gfile = gpkg_files[i]
        g = gpd.read_file(gfile)
        g[['minx','miny','maxx','maxy']] = g.bounds
        print('gfile', gfile)
        tname = os.path.basename(gfile).replace('.gpkg','')
        S2tile_path = os.path.join(sentinel2_dpath, tname)
        os.makedirs(S2tile_path, exist_ok=True)
        with ThreadPoolExecutor(cpus) as TEX:
            for i in range(g.shape[0]):
                print(f'{i}/{g.shape[0]} @{tname}')
                TEX.submit(download_sentinel2,i,g,name,S2tile_path,band_codes,scale)

    tf = time.perf_counter() - ti 
    print(f'RUN.TIME {tf/60} mins')
                           
