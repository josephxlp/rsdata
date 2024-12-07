
import os 
import numpy as np 
from opentopographyutils import dem_types, download_globaldem
from upaths import files_pattern,OPEN_TOPOGRAPHY_DPATH
from sec import creds
from glob import glob

file_paths = glob(files_pattern)


api_key = creds['OPEN_TOPOGRAPHY_API_KEY']
varnames = np.array(list(dem_types.values()))

#for varname in varnames:
if __name__ == '__main__':
    for rpath in file_paths:

        tile = rpath.split('/')[-2]
        tile_dpath = os.path.join(OPEN_TOPOGRAPHY_DPATH,tile)
        os.makedirs(tile_dpath, exist_ok=True)
        for varname in varnames:
            tile_var_dpath = os.path.join(tile_dpath, varname)
            os.makedirs(tile_var_dpath, exist_ok=True)

            download_globaldem(outdir=tile_var_dpath, rpath=rpath, varname=varname, api_key=api_key)
            print(varname)



