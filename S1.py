import os 
import ee 
import geemap
import time 
from upaths import patches_pattern, sentinel1_dpath
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import geopandas as gpd 
from geeutils import download_sentinel1

try:
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
except:
    ee.Authenticate()
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')

cpus = int(os.cpu_count() * 0.75)
scale = 30#15 
pol = 'VV'
name = 'S1_VVVH'

gpkg_files = sorted(glob(patches_pattern),reverse=True)
print(gpkg_files)
if __name__ == '__main__':
    ti = time.perf_counter()
    for i in range(len(gpkg_files)):
        #if i > 0 : break
        gfile = gpkg_files[i]
        g = gpd.read_file(gfile)
        g[['minx','miny','maxx','maxy']] = g.bounds
        print('gfile', gfile)
        tname = os.path.basename(gfile).replace('.gpkg','')
        S1tile_path = os.path.join(sentinel1_dpath, tname)
        os.makedirs(S1tile_path, exist_ok=True)
        with ThreadPoolExecutor(cpus) as TEX:
            for j in range(g.shape[0]):
                #if j > 2: break
                print(f'{j}/{g.shape[0]} @{tname} :: {i}{len(gpkg_files)}')
                TEX.submit(
                    download_sentinel1,j,g,pol,name,S1tile_path,scale)

    tf = time.perf_counter() - ti 
    print(f'RUN.TIME {tf/60} mins')
                           
