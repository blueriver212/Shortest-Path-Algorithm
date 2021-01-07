import networkx as nx
import pandas as pd
import rasterio
from shapely.geometry import Point
import geopandas as gpd
from shapely.geometry import LineString


class NearestRoad:

    def __init__(self, ele_path, user_input, node_near_user, node_near_high_point, user_itn, node_set, buffer_range):
        self.elevation = rasterio.open(ele_path)
        self.read_elevation = self.elevation.read(1)
        self.user_input = user_input
        self.nearest_node = node_near_user[0]
        self.highest_node = node_near_high_point[0]
        self.user_itn = user_itn
        self.road_links = user_itn["roadlinks"]
        self.nodes_table = pd.DataFrame(user_itn['roadnodes'])
        self.node_set = node_set
        self.nodes_name_list = self.nodes_table.columns.tolist()
        self.buffer_range = buffer_range
        self.nearest_node_p = Point(self.node_set[node_near_user[0]][1])
        self.highest_node_p = Point(self.node_set[node_near_high_point[0]][1])

    def get_road_walk(self):
        """
        Create a weighted network graph to the search for the nearest road
        :return: A network graph of the road links
        """
        g = nx.Graph()
        for link in self.road_links:
            start = self.road_links[link]["start"]
            end = self.road_links[link]["end"]
            road = self.road_links[link]["coords"]
            n = 0
            within = 0
            # Determine if the road exceeds the buffer zone
            for p in road:
                point = Point(tuple(road[n]))
                n += 1
                if point.distance(self.user_input) >= self.buffer_range:
                    within += 1
            if within != 0:
                g.add_edge(
                    start, end,
                    fid=link,
                    weight=float("inf"))
            else:
                # Get the coordinates of the start and end points of the road in the buffer
                coord_start = Point(tuple(self.nodes_table[start]["coords"]))
                coord_end = Point(tuple(self.nodes_table[end]["coords"]))
                row_start, col_start = self.elevation.index(
                    coord_start.x, coord_start.y)
                row_end, col_end = self.elevation.index(
                    coord_end.x, coord_end.y)
                ele_start = self.read_elevation[row_start, col_start]
                ele_end = self.read_elevation[row_end, col_end]
                ele_gap = ele_end - ele_start
                # Due to the difference in elevation, different weights are given to the uphill and downhill road.
                if ele_gap > 0:
                    g.add_edge(
                        start, end,
                        fid=link,
                        weight=self.road_links[link]['length'] / 5000 * 60 + ele_gap / 10)
                else:
                    g.add_edge(
                        start, end,
                        fid=link,
                        weight=self.road_links[link]['length'] / 5000 * 60)

        return g

    def get_road_drive(self):
        """
        Assuming you have a vehicle, you can quickly reach the highest point on the island
        (we assume the speed of your vehicle is 30km/h)
        :return: The shortest route to the highest point using a vehicle
        """

        g_drive = nx.Graph()
        for link in self.road_links:
            start = self.road_links[link]["start"]
            end = self.road_links[link]["end"]
            g_drive.add_edge(
                start, end,
                fid=link,
                weight=self.road_links[link]['length']/30000*60)
        path_drive = nx.dijkstra_path(
            g_drive,
            source=self.node_set[self.nearest_node][0],
            target="osgb5000005136697688")
        length_drive = nx.dijkstra_path_length(
            g_drive,
            source=self.node_set[self.nearest_node][0],
            target="osgb5000005136697688")
        print(f'Taking vehicles to the highest point in this island may take you {length_drive} minutes')
        links = []
        geom = []
        first_node = path_drive[0]
        for node in path_drive[1:]:
            link_fid = g_drive.edges[first_node, node]['fid']
            links.append(link_fid)
            geom.append(LineString(self.road_links[link_fid]['coords']))
            first_node = node
        shortest_path_drive = gpd.GeoDataFrame({'fid': links, 'geometry': geom})

        return shortest_path_drive

    def get_nearest_path(self, g):
        """
        A method finding the shortest path based on the network graph created before
        :param g:
        :return:
        """
        path = nx.dijkstra_path(g,
                                source=self.node_set[self.nearest_node][0],
                                target=self.node_set[self.highest_node][0])
        length = nx.dijkstra_path_length(g,
                                         source=self.node_set[self.nearest_node][0],
                                         target=self.node_set[self.highest_node][0])

        # If there is no path within the buffer to reach the target node
        # Draw the shortest path partly outside the buffer
        if length == float("inf"):
            print("You only have one path partly outside the buffer zone to reach your destination")
        else:
            print(f'Walking to the highest point within 5km will takes you {length} minutes')

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
