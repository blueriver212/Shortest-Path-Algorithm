import json
import networkx as nx
import pandas as pd
import rasterio
from shapely.geometry import Point
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString


class NearestRoad:

    def __init__(self, ele_path, nearest_node, highest_node,user_itn):
        self.elevation = rasterio.open(ele_path)
        self.nearest_node = nearest_node[0]
        self.highest_node = highest_node[0]
        self.user_itn = user_itn
        self.road_links = user_itn["roadlinks"]
        self.nodes_table = pd.DataFrame(user_itn['roadnodes'])
        self.nodes_name_list = self.nodes_table.columns.tolist()


    def get_road(self):
        ele_pd = self.elevation.read(1)
        g = nx.Graph()
        for link in self.road_links:
            start = self.road_links[link]["start"]
            end = self.road_links[link]["end"]
            coord_start = Point(tuple(self.nodes_table[start]["coords"]))
            coord_end = Point(tuple(self.nodes_table[end]["coords"]))
            row_start, col_start = self.elevation.index(
                coord_start.x, coord_start.y)
            row_end, col_end = self.elevation.index(
                coord_end.x, coord_end.y)
            ele_start = ele_pd[row_start, col_start]
            ele_end = ele_pd[row_end, col_end]
            ele_gap = ele_end - ele_start

            if ele_gap > 0:
                g.add_edge(
                    start, end,
                    fid=link,
                    weight=self.road_links[link]['length'] / 5000 * 6 + ele_gap / 10)
            else:
                g.add_edge(
                    start, end,
                    fid=link,
                    weight=self.road_links[link]['length'] / 5000 * 6)
        return g

    def get_nearest_path(self,g):
        path = nx.dijkstra_path(g,
                                source=self.nodes_name_list[self.nearest_node],
                                target=self.nodes_name_list[self.highest_node])

        links = []  # this list will be used to populate the feature id (fid) column
        geom = []  # this list will be used to populate the geometry column

        first_node = path[0]
        for node in path[1:]:
            link_fid = g.edges[first_node, node]['fid']
            links.append(link_fid)
            geom.append(LineString(self.road_links[link_fid]['coords']))
            first_node = node

        shortest_path_gpd = gpd.GeoDataFrame({'fid': links, 'geometry': geom})

        return shortest_path_gpd