import rasterio
import geopandas as gpd
from shapely.geometry import Point, Polygon
import rasterio.mask
import json
from matplotlib import pyplot
import os
import numpy as np


class HighestPoint:

    def __init__(self, user_point, island_path, ele_path, out_loc):
        self.__user_point = user_point
        self.__island_path = island_path
        self.__ele_path = ele_path
        self.__out_loc = out_loc

    def read_island(self):
        island_file = gpd.read_file(self.__island_path)
        return island_file

    @staticmethod
    def get_features(gdf):
        return [json.loads(gdf.to_json())['features'][0]['geometry']]

    def clip_elevation(self):
        """
        Limit the highest point range to a 5km buffer
        :return:
        """
        # Open the main raster
        data = rasterio.open(self.__ele_path)

        # Create a 5km buffer from the point first, then turn to gdf
        buffer = self.__user_point.buffer(5000)
        geo = gpd.GeoDataFrame({'geometry': buffer}, index=[0], crs="EPSG:27700")  # crs=from_epsg(27700)
        #geo = geo.to_crs(crs=data.crs.data)
        #geo = geo.to_crs(crs=({'init': 'epsg:27700'}))
        #geo = geo.to_crs(crs="EPSG:27700")

        # Function to parse features from GeoDataFrame in such a manner that rasterio wants them
        clip_extent = [json.loads(geo.to_json())['features'][0]['geometry']]
        out_image, out_transform = rasterio.mask.mask(data, clip_extent, crop=True)
        out_meta = data.meta.copy()

        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform,
                         "crs": 'epsg:27700'}
                        )
        # Sets the output .tif location
        root = os.path.dirname(os.getcwd())
        out_tif = os.path.join(root, 'Material', 'elevation', self.__out_loc)

        with rasterio.open(out_tif, 'w', **out_meta) as dest:
            dest.write(out_image)
        # Plotting out file
        clip = rasterio.open(out_tif)

        pyplot.imshow(clip.read(1), cmap="pink")
        pyplot.show()
        return out_tif

    def find_highest_point(self, clipped_path):
        """
        Find the highest point and return the coordinates of the highest point
        :return:
        """
        with rasterio.open(clipped_path, 'r') as ds:
            arr = ds.read(1)  # read all raster values
            high_point = np.amax(arr)
            res = np.where(arr == high_point)
            highest = ds.xy(res[0], res[1])
            highest_point = Point(highest[0][0], highest[1][0])
            print(f'Your highest point is {highest_point}')



            return highest_point
