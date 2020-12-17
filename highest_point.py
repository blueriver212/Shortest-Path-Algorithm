import rasterio
import pyproj
import shapefile
from shapely.geometry import Point, Polygon
import rasterio.mask
import numpy as np


def read_island(file):
    readIsland = shapefile.Reader(file)
    features = readIsland.shapeRecords()[0].__geo_interface__
    points = features["geometry"]["coordinates"][3][0]
    island = Polygon(points)
    return island


def read_elevation(file):
    elevation = rasterio.open(file)
    return elevation


def create_buffer(coord, island):
    """
        A function to create a buffer of 5km around the given coordinate.
        :param coord:
        :return:
        """
    pt = Point(coord)
    buffer = pt.buffer(5000).intersection(island)
    return buffer


def clip_elevation(buffer, elevation):
    """
        A function to create a buffer clipping elevation
        :return:
        """
    features_buffer = [buffer.__geo_interface__]
    out_image, out_transform = rasterio.mask.mask(
        elevation, features_buffer, crop=False)
    reshape_area = out_image.reshape(out_image.shape[1], out_image.shape[2])
    return reshape_area


def highest_point(reshape_area):
    """
        Find the index of highest point in buff area
        :return:
        """
    point_set = set()
    [r, c] = reshape_area.shape
    for i in range(r):
        for j in range(c):
            point_set.add(reshape_area[i, j])
    point_list = list(point_set)
    highest = max(point_list)
    highest_index = np.where(reshape_area == highest)
    return highest_index