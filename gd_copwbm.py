from glob import glob 

import geopandas as gpd 
import os 
import ee 
import time 
from concurrent.futures import ThreadPoolExecutor
from g_utils import grab_copwbm_patch,get_tilename
from g_vars import dir_geepatch, dir_gpkg,scale, cpus 


name = 'COPWBM'

#dir_geepatch = "/media/ljp238/6tb/Joseph/aoi_datasets/geepatch/"
#dir_gpkg = "/media/ljp238/6tb/Joseph/aoi_datasets/geepatch/geepatch_vectors/"

try:
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
except:
    ee.Authenticate()
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')

dir_s1path = os.path.join(dir_geepatch,'COPWBM')
os.makedirs(dir_s1path, exist_ok=True)


if __name__ == '__main__':
    ti = time.perf_counter()
    gpkg_files = glob(f'{dir_gpkg}/*/*.gpkg', recursive=True); print(len(gpkg_files))
     

    print(gpkg_files)
    with ThreadPoolExecutor(cpus) as TEX:
        for fi in range(len(gpkg_files)):
            #if fi > 0: break
        
            gfile = gpkg_files[fi]
            g = gpd.read_file(gfile)
            g[['minx','miny','maxx','maxy']] = g.bounds
            print('gfile', gfile)
            tile_name = get_tilename(g)
            dir_tile_name = os.path.join(dir_s1path, tile_name)
            os.makedirs(dir_tile_name, exist_ok=True)

            for i in range(g.shape[0]):
                #grab_copwbm_patch(i,g,dir_tile_name,scale,name)
                #if i > 3: break
                TEX.submit(grab_copwbm_patch, i,g,dir_tile_name,scale,name)

               

    tf = time.perf_counter() - ti
    print(f'run.time {tf/60} min (s)')
