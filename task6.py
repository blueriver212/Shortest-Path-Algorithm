from shapely.geometry import Point, asShape
import fiona
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
        shp = fiona.open(self.__island_path)

        shapefile_record = next(iter(shp))
        shape = asShape(shapefile_record['geometry'])

        if shape.contains(self.__point):
            return True

if __name__ == '__main__':
    pt = Point(439619, 85800)
    root = os.path.dirname(os.getcwd())
    island_file_name = 'isle_of_wight.shp'
    island_file = os.path.join(root, 'Material', 'shape', island_file_name)

    test = InIsland(pt, island_file)

    print(test.is_inside())


