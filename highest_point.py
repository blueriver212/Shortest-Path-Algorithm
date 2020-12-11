import pyproj
from Shapely import Point, Polygon



#British National Grid Projection
bng=pyproj.Proj(init='epsg:27700')

def create_buffer(coord):
    """
    A function to create a buffer of 5km around the given coordinate.
    :param coord:
    :return:
    """

    coord_input = Point[coord[0], coord[1]]



