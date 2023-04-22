import boto3
import sys
import pyproj
import os
import geopandas as gp
from shapely.geometry import Polygon
import numpy as np

# python3 utils/gridding/create-grid.py "EPSG:3310"

def main():
    s3 = get_creds()

    runBbox = get_proj_bbox(EPSG)
    
    df = gp.GeoDataFrame(index=[0], crs="epsg:4326", geometry=[runBbox]) 
    
    gp_reproj = gp.GeoDataFrame(df, crs = "epsg:4326").to_crs(EPSG)

    # Grid Bbox
    print("Gridding Bbox")
    proj_minx = gp_reproj.geometry.bounds['minx'].values[0]
    proj_maxx = gp_reproj.geometry.bounds['maxx'].values[0]
    proj_miny = gp_reproj.geometry.bounds['miny'].values[0]
    proj_maxy = gp_reproj.geometry.bounds['maxy'].values[0]

    # Set grid size here. Note: Use projection units
    rows = abs(int(np.ceil((proj_maxy-proj_miny) / HEIGHT)))
    cols = abs(int(np.ceil((proj_maxx-proj_minx) / WIDTH)))
    XleftOrigin = proj_minx
    XrightOrigin = proj_minx + WIDTH
    YtopOrigin = proj_maxy
    YbottomOrigin = proj_maxy - HEIGHT
    polygons = []
    for i in range(cols):
        Ytop = YtopOrigin
        Ybottom = YbottomOrigin
        for j in range(rows):
            gridNum = str(i) + str(j)
            prefixNum = os.path.join(GRID_PATH, gridNum)
            writeGeom = Polygon([(XleftOrigin, Ytop), (XrightOrigin, Ytop), (XrightOrigin, Ybottom), (XleftOrigin, Ybottom)])
            polygons.append(
                {
                'row': i,
                'column': j,
                'grid_num': gridNum,
                'xmin': XleftOrigin,
                'xmax': XrightOrigin,
                'ymin': Ybottom,
                'ymax': Ytop,
                's3_prefix': prefixNum,
                'geometry': writeGeom
                }
            ) 
            Ytop = Ytop - HEIGHT
            Ybottom = Ybottom - HEIGHT
        XleftOrigin = XleftOrigin + WIDTH
        XrightOrigin = XrightOrigin + WIDTH

    print("Writing polygons")
    grid = gp.GeoDataFrame(polygons, crs=EPSG).to_file(f"{GRID_PATH}/{str(EPSG.split(':')[-1])}-grid-index.gpkg", driver="GPKG")

def get_creds():    
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    
    return s3

def get_proj_bbox(EPSG):
    
    crs = pyproj.CRS(EPSG)
    minx = crs.area_of_use.bounds[0]
    maxx = crs.area_of_use.bounds[2]
    miny = crs.area_of_use.bounds[3]
    maxy = crs.area_of_use.bounds[1]
    
    return Polygon([[minx, miny],
                    [maxx, miny],
                    [maxx, maxy],
                    [minx, maxy],
                    [minx, miny]])

if __name__ == "__main__":
    
    EPSG = sys.argv[1]
    BUCKET = os.environ.get("AWS_BUCKET")
    GRID_PATH = "proj-grids"
    WIDTH = 1000
    HEIGHT = 1000

    os.makedirs(GRID_PATH, exist_ok=True)
    
    main()





