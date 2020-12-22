import json
import networkx as nx
import pandas as pd
import rasterio
from shapely.geometry import Point


class NearestRoad:

    def __init__(self, ele_path, nearest_node, highest_node):
        self.elevation = rasterio.open(ele_path)
        self.nearest_node = nearest_node[0]
        self.highest_node = highest_node[0]

    def get_road(self, file):
        ele_pd = self.elevation.read(1)
        with open(file, 'r') as f:
            g = nx.Graph()
            user_itn = json.load(f)
            roadlinks = user_itn["roadlinks"]
            nodes_table = pd.DataFrame(user_itn['roadnodes'])
            nodes_name_list = nodes_table.columns.tolist()

        for link in roadlinks:
            start = roadlinks[link]["start"]
            end = roadlinks[link]["end"]
            coord_start = Point(tuple(nodes_table[start]["coords"]))
            coord_end = Point(tuple(nodes_table[end]["coords"]))
            # print(coord_start,coord_end)
            row_start, col_start = self.elevation.index(
                coord_start.x, coord_start.y)
            # print(row_start, col_start)
            row_end, col_end = self.elevation.index(
                coord_end.x, coord_end.y)
            ele_start = ele_pd[row_start, col_start]
            ele_end = ele_pd[row_end, col_end]
            ele_gap = ele_end - ele_start

            if ele_gap > 0:
                g.add_edge(
                    start, end,
                    fid=link,
                    weight=roadlinks[link]['length'] / 5000 * 6 + ele_gap / 10)
            else:
                g.add_edge(
                    start, end,
                    fid=link,
                    weight=roadlinks[link]['length'] / 5000 * 6)

        return g

    def get_nearest_path(self):

        path = nx.dijkstra_path(self.get_road(),
                                source=self.nodes_name_list[self.nearest_node],
                                target=self.nodes_name_list[self.highest_node])
        nx.draw(path, font_color='white', with_labels=True)
        return path


import json
import networkx as nx
import pandas as pd
import rasterio
from shapely.geometry import Point


class NearestRoad:

    def __init__(self, ele_path, nearest_node, highest_node):
        self.elevation = rasterio.open(ele_path)
        self.nearest_node = nearest_node[0]
        self.highest_node = highest_node[0]

    def get_road(self, file):
        ele_pd = self.elevation.read(1)
        with open(file, 'r') as f:
            g = nx.Graph()
            user_itn = json.load(f)
            roadlinks = user_itn["roadlinks"]
            nodes_table = pd.DataFrame(user_itn['roadnodes'])
            nodes_name_list = nodes_table.columns.tolist()

        for link in roadlinks:
            start = roadlinks[link]["start"]
            end = roadlinks[link]["end"]
            coord_start = Point(tuple(nodes_table[start]["coords"]))
            coord_end = Point(tuple(nodes_table[end]["coords"]))
            # print(coord_start,coord_end)
            row_start, col_start = self.elevation.index(
                coord_start.x, coord_start.y)
            # print(row_start, col_start)
            row_end, col_end = self.elevation.index(
                coord_end.x, coord_end.y)
            ele_start = ele_pd[row_start, col_start]
            ele_end = ele_pd[row_end, col_end]
            ele_gap = ele_end - ele_start

            if ele_gap > 0:
                g.add_edge(
                    start, end,
                    fid=link,
                    weight=roadlinks[link]['length'] / 5000 * 6 + ele_gap / 10)
            else:
                g.add_edge(
                    start, end,
                    fid=link,
                    weight=roadlinks[link]['length'] / 5000 * 6)

        return g

    def get_nearest_path(self):

        path = nx.dijkstra_path(self.get_road(),
                                source=self.nodes_name_list[self.nearest_node],
                                target=self.nodes_name_list[self.highest_node])
        nx.draw(path, font_color='white', with_labels=True)
        return path