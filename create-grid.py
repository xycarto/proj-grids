import sys
import pyproj
import os
import geopandas as gp
from shapely.geometry import Polygon, box
import math


def main():
    crs = pyproj.CRS(EPSG)
    
    # Make BBox from WGS84 extents of projection
    reproj = gp.GeoDataFrame(index=[0], 
                             crs=WGS, 
                             geometry=[box(*crs.area_of_use)]
                             ).to_crs(EPSG)

    # Grid size set here. Size is height and 
    # width of cell. Note: Use projection units
    rows = abs(int(math.ceil((
        reproj.bounds.loc[0, 'maxy']-reproj.bounds.loc[0, 'miny']) / HEIGHT))
        )
    cols = abs(int(math.ceil((
        reproj.bounds.loc[0, 'maxx']-reproj.bounds.loc[0, 'minx']) / WIDTH))
        )
    x_left_origin = reproj.bounds.loc[0, 'minx']
    x_right_origin = reproj.bounds.loc[0, 'minx'] + WIDTH
    y_top_origin = reproj.bounds.loc[0, 'maxy']
    y_bottom_origin = reproj.bounds.loc[0, 'maxy'] - HEIGHT
    
    # Make Polygons
    print("Making polygons...")
    polygons = []
    for i in range(cols):
        y_top = y_top_origin
        y_bottom = y_bottom_origin
        for j in range(rows):
            write_geom = box(x_left_origin, y_bottom, x_right_origin, y_top)
            polygons.append(
                {
                'row': i,
                'column': j,
                'grid_num': str(i) + str(j),
                'xmin': x_left_origin,
                'xmax': x_right_origin,
                'ymin': y_bottom,
                'ymax': y_top,
                'geometry': write_geom
                }
            ) 
            y_top = y_top - HEIGHT
            y_bottom = y_bottom - HEIGHT
        x_left_origin = x_left_origin + WIDTH
        x_right_origin = x_right_origin + WIDTH

    print("Writing polygons...")
    gp.GeoDataFrame(polygons, crs=EPSG).to_file(
        f"{GRID_PATH}/{str(EPSG.split(':')[-1])}-grid-index.gpkg", 
        driver="GPKG")

if __name__ == "__main__":    
    EPSG = sys.argv[1]
    WIDTH = int(sys.argv[2])
    HEIGHT = int(sys.argv[3])
    GRID_PATH = "proj-grids"    
    WGS = 4326

    os.makedirs(GRID_PATH, exist_ok=True)
    
    main()





