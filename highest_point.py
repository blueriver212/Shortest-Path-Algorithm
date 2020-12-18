import rasterio
import shapefile
from shapely.geometry import Point, Polygon
import rasterio.mask
import numpy as np


class HighestPoint:
    """

    """

    def __init__(self, user_point, island_path, ele_path,):
        self.__user_point = user_point
        self.__island_path = island_path
        self.__ele_path = ele_path

    def read_island(self):
        file_island = shapefile.Reader(self.__island_path)
        features = file_island.shapes()[0].__geo_interface__
        points = features["coordinates"][3][0]
        island = Polygon(points)
        return island

    def read_elevation(self):
        elevation = rasterio.open(self.__ele_path)
        return elevation

    def clip_elevation(self):
        """
        Limit the highest point range to a 5km buffer
        :return:
        """
        buffer = self.__user_point.buffer(5000)
        features_buffer = [buffer.__geo_interface__]
        out_image, out_transform = rasterio.mask.mask(
            self.read_elevation(), features_buffer, crop=False)
        reshape_area = out_image.reshape(
            out_image.shape[1], out_image.shape[2])
        return reshape_area

    def find_highest_point(self):
        """
        Find the highest point and return the coordinates of the highest point
        :return:
        """

        highest_index = np.where(
            self.clip_elevation() == np.max(
                self.clip_elevation()))
        [row, col] = highest_index[0]
        coordinate = self.read_elevation().xy(row, col)
        print(coordinate)
        print(np.max(self.clip_elevation()))

        return coordinate


def main():
    coord = [float(input('x=')), float(input('y='))]
    pt = Point(coord)

    get_highest_point = HighestPoint(
        pt,
        "Material/shape/isle_of_wight.shp",
        "Material/elevation/SZ.asc").find_highest_point()


if __name__ == "__main__":
    main()
