from shapely.geometry import Point, asShape
import geopandas as gpd
import os

class InIsland:

    def __init__(self, point, island_path):
        self.__point = point
        self.__island_path = island_path

    def is_inside(self):
        """
        This will return either true or false depending if the point is within the island shapefile given.
        :return: Boolean Outcome.
        Taken from https://gis.stackexchange.com/questions/84114/shapely-unable-to-tell-if-polygon-contains-point
        """
        shp = gpd.read_file(self.__island_path)
        shape = asShape(shp.geometry[0])

        if shape.contains(self.__point):
            return True

if __name__ == '__main__':
    pt = Point(425000, 75000)
    root = os.path.dirname(os.getcwd())
    island_file_name = 'isle_of_wight.shp'
    island_file = os.path.join(root, 'Material', 'shape', island_file_name)

    test = InIsland(pt, island_file)

    print(test.is_inside())


