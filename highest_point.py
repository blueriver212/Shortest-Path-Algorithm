import pyproj
from Shapely import Point, Polygon

# British National Grid Projection
bng = pyproj.Proj(init='epsg:27700')


def create_buffer(coord):
    """
    A function to create a buffer of 5km around the given coordinate.
    :param coord:
    :return:
    """

    # First take the coordinate and turn into a point with shapely
    coord_input = Point[coord[0], coord[1]]

    # Transform the point to a British National Grid

    # Create a 5km buffer around the point

    # this is a comment to show how i am editing the file

def highest_point(coord, buffer):
    pass

    # Find the highest point in that buffer zone.
    # Return the coordinate of the highest point in the 5km buffer.
    # There is a tool called clip/extract by mask, that will cut the elevation raster into a smaller one.


