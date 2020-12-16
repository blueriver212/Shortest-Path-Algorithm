# Task 3 - Nearest Integrated Transport Network
import json
from shapely.geometry import Point
from rtree import index
from error_handling import *


class ITN:

    def __init__(self, file):
        self.file = file

    def user_itn(self):
        """
        A method for the user to input their ITN Network (JSON file)
        :return:
        """
        with open(self.file, 'r') as f:
            user_itn = json.load(f)

        return user_itn

    def make_tree(self):
        """
        Creates an index of the input .json OS network.
        :return: A rtree index of the input.
        """
        idx = index.Index()
        coord = self.user_itn()
        coord = coord['roadnodes']

        count = 0
        for point in coord:
            idx.insert(count, coord[point]['coords'])
            count += 1

        return idx

    def nearest_node(self, point):
        """
        Finds the nearest node of a point given an Shapely Point input
        :return:
        """
        # Find the nearest node in the rTree index
        idx = self.make_tree()
        node_nearest_point = list(idx.nearest((point.x, point.y)))
        return node_nearest_point
#Delete this at the end of the project
# if __name__ == "__main__":
#     main()