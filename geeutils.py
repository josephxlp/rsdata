import ee 
import geemap
import time 
from os.path import basename,join,isfile 


def get_ee_geometry(i, g, name):
    ig = g.iloc[i:i+1,]
    bBox = [float(ig.minx), float(ig.miny), float(ig.maxx), float(ig.maxy)]
    fname = (basename(ig.location.values[0])).replace('..tif', '.tif')
    fname = fname.replace('.tif', f'_{name}.tif')
    region = ee.Geometry.Rectangle(bBox)
    return region, fname

def get_S1_image(aoi,pol='VV', opass='ASCENDING',idate='2021-01-01',fdate='2022-12-01'):
    sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
    .filter(ee.Filter.eq('instrumentMode','IW')) \
    .filterDate(idate,fdate).filter(ee.Filter.listContains('transmitterReceiverPolarisation', pol)) \
    .filter(ee.Filter.eq('orbitProperties_pass',opass)) \
    .filter(ee.Filter.eq('resolution_meters',10)) \
    .filterBounds(aoi)\
   
    s1img = ee.Image(sentinel1.median().clip(aoi))
    s1img = s1img.select(['VV','VH'])
    return s1img

def download_sentinel1(i,g,pol,name,S1tile_path,scale):
    region, fname = get_ee_geometry(i, g,name)
    s1img = get_S1_image(region, pol)
    outpath = join(S1tile_path, fname)
    gee_download_geemap(s1img,outpath, scale)


def ee_clip_mosaic_roi(dobject,roi):
    mosaic = dobject.mosaic()
    mosaiclip = mosaic.clip(roi)
    return mosaiclip

def getDEM_files(roi):
    glo30  = ee.ImageCollection("COPERNICUS/DEM/GLO30").filterBounds(roi)
    wbm = ee_clip_mosaic_roi(glo30.select('WBM'),roi)
    hem = ee_clip_mosaic_roi(glo30.select('HEM'),roi)
    flm = ee_clip_mosaic_roi(glo30.select('FLM'),roi)
    edm = ee_clip_mosaic_roi(glo30.select('EDM'),roi)
    dem = ee_clip_mosaic_roi(glo30.select('DEM'),roi)
    return dem,edm,flm,hem,wbm


def download_sentinel2(i,g,name,S2tile_path,band_codes,scale):
    region, fname = get_ee_geometry_s2(i, g,name)
    rgb = get_S2median(region,band_codes)
    outpath = join(S2tile_path, fname)
    gee_download_geemap(rgb,outpath, scale)
    #time.sleep(0.5)

def get_ee_geometry_s2(i, g, name):
    ig = g.iloc[i:i+1,]
    # Calculate the bounding box from the geometry
    bBox = ig.geometry.bounds.iloc[0].tolist()  # [minx, miny, maxx, maxy]
    fname = (basename(ig.location.values[0]))
    fname = fname.replace('.tif', f'_{name}.tif')
    fname = fname.replace('..tif', f'_{name}.tif')
    region = ee.Geometry.Rectangle(bBox)
    return region, fname

def get_S2median(region,band_codes,CLOUD_FILTER=30):
    s2coll = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
             .filterBounds(region) \
             .filterDate('2021', '2022') \
             .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', CLOUD_FILTER))
    

    sentinel2_masked = s2coll.map(mask_clouds)
    #rgb_bands = ['B4', 'B3', 'B2','B8']
    rgb = sentinel2_masked.select(band_codes).median().clip(region)
    return rgb 


def mask_clouds(image):
    qa = image.select('QA60')
    cloudBitMask = int(2**10)
    cirrusBitMask = int(2**11)
    mask = qa.bitwiseAnd(cloudBitMask).eq(0) \
        .And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask).divide(10000)

def gee_download_geemap(image,outpath, scale):
    print(outpath)
    if isfile(outpath):
        print('Already downloaded') 
    else:
        geemap.ee_export_image(image, outpath, scale=scale)



def get_tilename(subg):
    #minx, miny, maxx, maxy  = g.total_bounds
    minx, miny, maxx, maxy  = subg.total_bounds
    print(minx, miny)
    try:
        minx = int(round(minx,1))
        miny = int(round(miny,1))
        maxx = int(maxx)
        maxy = int(maxy)
    except:
        minx = float(minx)
        miny = float(miny)
        maxx = float(maxx)
        maxy = float(maxy)
    print(minx, miny)
    lat_direction = 'N' if miny >= 0 else 'S'
    lon_direction = 'E' if minx >= 0 else 'W'
    identifier = f'{lat_direction}{abs(miny)}_{lon_direction}{abs(minx)}'
    print(identifier)
    return identifier

def initialize_gee_highvolume_api():
    try:
        ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
    except:
        ee.Authenticate()
        ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')



