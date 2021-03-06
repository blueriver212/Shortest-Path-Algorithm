# Task 3 - Nearest Integrated Transport Network
import json
from rtree import index
from shapely.geometry import Point


class ITN:

    def __init__(self, file, user_input, buffer_range):
        self.file = file
        self.user_input = user_input
        self.buffer_range = buffer_range

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
        node_set = {}
        count = 0
        for point in coord:
            point_coord = coord[point]['coords'][:2]
            if Point(tuple(point_coord)).distance(self.user_input) <= self.buffer_range:
                idx.insert(count, coord[point]['coords'])
                node_set.update({count: [point, point_coord]})
                count += 1

        return idx, node_set,

    def nearest_node(self, point):
        """
        Finds the nearest node of a point given an Shapely Point input
        :return:
        """
        # Find the nearest node in the rTree index
        idx = self.make_tree()[0]
        node_nearest_point = list(idx.nearest((point.x, point.y)))
        return node_nearest_point
