# Packages for the main tasks
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import Point, LineString
import os
import numpy as np
from rtree import index
from cartopy import crs
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from pyproj import CRS

# Packages for the creative tasks
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import json
from shapely.geometry import asShape
import requests
import pyproj
import sys

# Define the global variables for Tkinter GUI
global getx, gety, getradius, getaddress


class UserInput:

    def __init__(self):
        """
        This class will include the GUI windows and tell user how to use the escape system. The main window let user
        choose work files and choose coordinate or address they want to insert,and then insert it and choose escape way.
        """
        global getx, gety, getradius

        self.root = tk.Tk()
        self.root.title('Welcome to files choose system!')
        self.lb1 = tk.Label(
            self.root,
            text="How to use this software: \n"
                 "\n"
                 "1. Firstly input your data. Click on each button and locally find your file\n"
                 "2. The .asc file is the elevation data for your island and the .tif is for map plotting \n"
                 "3. If you file has the correct extension, the button will turn green. Else, it will turn red. \n"
                 "4. Ensure that all 4 types of file are inputted before using the software\n"
                 "\n"
                 "This software will either except exact coordinates (BNG) or a Google Maps Search \n"
                 "5. Click the button to choose how you will input your location \n"
                 "\n"
                 "In the box below, you will receive information about your chosen route.",
            bg='white',
            anchor="center",
            justify="left",
            fg="red",
            heigh=12,
            width=70).place(
            x=50,
            y=15)
        self.bt1 = tk.Button(
            self.root,
            text='Insert Coordinate', font='10',
            height=2,
            width=25,
            command=self.insert_coord)
        self.bt1.place(x=50, y=300)
        self.bt2 = tk.Button(
            self.root,
            text='Choose asc file',
            height=1,
            width=12,
            command=self.get_asc)
        self.bt2.place(x=20, y=250)
        self.bt3 = tk.Button(
            self.root,
            text='Choose shape file',
            height=1,
            width=15,
            command=self.get_shp)
        self.bt3.place(x=170, y=250)
        self.bt4 = tk.Button(
            self.root,
            text='Choose json file',
            height=1,
            width=15,
            command=self.get_json)
        self.bt4.place(x=320, y=250)
        self.bt5 = tk.Button(
            self.root,
            text='Choose tif file',
            height=1,
            width=15,
            command=self.get_tif)
        self.bt5.place(x=470, y=250)
        self.bt6 = tk.Button(
            self.root,
            text='Insert Address', font='10',
            height=2,
            width=25,
            command=self.insert_addr)
        self.bt6.place(x=310, y=300)
        self.shp_file = ''
        self.asc_file = ''
        self.tif_file = ''
        self.json_file = ''
        self.pt = ''
        self.get_radius = ''

        # Root window show in mid screen
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        width = 600
        height = 380
        midshow = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(midshow)

    def insert_coord(self):
        """
        Design a user insert coordinate GUI use Insert coordinate button to check the coordinate point position.
        Reset button clear the user insert label. Get radius button to insert the escape radius.
        Go running button to calculate the escape path.
        Exit button let user to close the window.
        """

        global getx, gety, getradius

        if self.shp_file == '' or self.json_file == '' or self.asc_file == '' or self.tif_file == '':
            tk.messagebox.showwarning(
                title='Lack of work file',
                message='Please check your four choose file buttons, follow the instruction and make them turn green.')
            return

        insert_coord = tk.Toplevel(self.root)
        insert_coord.title('Please insert your coordinates!')
        insert_coord.geometry('550x380')

        lb2 = tk.Label(
            insert_coord,
            text='Your location\'s X coordinate:')
        lb2.place(
            x=50,
            y=190)
        lb3 = tk.Label(
            insert_coord,
            text='Your location\'s Y coordinate:')
        lb3.place(
            x=50,
            y=220)
        lb4 = tk.Label(insert_coord,
                       text='Please insert your search radius (m):\n For example: 5000m = 5km')
        lb4.place(x=50, y=250)
        lb5 = tk.Label(insert_coord,
                       text="1. Please enter your coordinates into the text boxes above\n"
                            "2. To check if you are on the island, please click the 'Insert Coordinates' button\n"
                            "3. If you would like to re-enter your location, please click 'Reset Coordinates' \n"
                            "4. If the prompt is successful, if you are planning to walk to the highest point \n"
                            "   please enter a buffer (in m). Then press the 'Insert Search Radius'\n"
                            "5. Alternatively, if you want the shortest drive to the highest point on the island \n"
                            "   please press 'By Vehicle', you do not need to insert radius.\n"
                            "\n"
                            "Results of your chosen journey is provided in the original window. \n",
                       bg='white', anchor="center", justify="left", fg="red", height=10, width=61)
        lb5.place(x=50, y=15)
        getx = tk.Entry(insert_coord)
        getx.place(x=250, y=190)
        gety = tk.Entry(insert_coord)
        gety.place(x=250, y=220)
        default_radius = tk.StringVar()
        default_radius.set(5000)
        getradius = tk.Entry(
            insert_coord,
            textvariable=default_radius)
        getradius.place(x=250, y=250)
        bt7 = tk.Button(insert_coord, text='Insert coordinates', height=1, width=18,
                        command=self.user_coord)
        bt7.place(x=50, y=310)
        bt8 = tk.Button(insert_coord, text='Reset coordinates', height=1, width=18,
                        command=self.reset_coord)
        bt8.place(x=200, y=310)
        bt9 = tk.Button(insert_coord, text='Insert search radius', height=1, width=18,
                        command=self.insert_radius)
        bt9.place(x=350, y=310)
        bt10 = tk.Button(
            insert_coord,
            text='Go running',
            height=1,
            width=18,
            command=self.gorunning)
        bt10.place(x=50, y=340)
        bt11 = tk.Button(
            insert_coord,
            text='By vehicle',
            height=1,
            width=18,
            command=self.drive)
        bt11.place(x=200, y=340)
        bt12 = tk.Button(
            insert_coord,
            text='Exit this window',
            height=1,
            width=18,
            command=insert_coord.destroy)
        bt12.place(x=350, y=340)
        # text_2 = tk.Text(insert_coord, width='54', height='6')
        # text_2.place(x=50, y=390)

    def insert_addr(self):
        global getaddress, getradius
        """
        Design a user insert address GUI use Insert address button to convert address to coordinate point,
        Reset button clear the user insert label. Get radius button to insert the escape radius.
        Go running button to calculate the escape path.
        Exit button let user to close the window.
        """

        if self.shp_file == '' or self.json_file == '' or self.asc_file == '' or self.tif_file == '':
            tk.messagebox.showwarning(
                title='Lack of work file',
                message='Please check your four choose file buttons, follow the instruction and make them turn green.')
            return

        insert_addr = tk.Toplevel(self.root)
        insert_addr.title('Please insert address!')
        insert_addr.geometry('600x380')
        lb7 = tk.Label(insert_addr,
                       text="1. Please enter your address into the text box above, an example is provided.\n"
                            "2. To check if your address is on the island, please click the 'Insert Address' button\n"
                            "3. If you would like to re-enter your address, please click 'Reset Address' \n"
                            "4. If the prompt is successful, if you are planning to walk to the highest point \n"
                            "   please enter a buffer (in m). Then press the 'Insert Search Radius'\n"
                            "5. Alternatively, if you want the shortest drive to the highest point on the island \n"
                            "   please press 'By Vehicle', you do not need to insert radius.\n"
                            "\n"
                            "Results of your chosen journey is provided in the original window. \n",
                       bg='white', anchor="center", justify="left", fg="red", heigh=12, width=70)
        lb7.place(x=50, y=15)
        lb6 = tk.Label(insert_addr,
                       text='Please insert your search radius (m):\n For example: 5000m = 5km')
        lb6.place(x=10, y=250)
        lb8 = tk.Label(insert_addr,
                       text='Please insert your address:')
        lb8.place(x=10, y=220)
        bt13 = tk.Button(
            insert_addr,
            text='Insert address',
            height=1,
            width=18,
            command=self.user_addr)
        bt13.place(x=50, y=300)
        bt14 = tk.Button(
            insert_addr,
            text='Reset address',
            height=1,
            width=18,
            command=self.reset_addr)
        bt14.place(x=200, y=300)
        bt15 = tk.Button(insert_addr, text='Insert Search Radius', height=1, width=18,
                         command=self.insert_radius)
        bt15.place(x=350, y=300)
        bt16 = tk.Button(
            insert_addr,
            text='Go running',
            height=1,
            width=18,
            command=self.gorunning)
        bt16.place(x=50, y=330)
        bt17 = tk.Button(
            insert_addr,
            text='By vehicle',
            height=1,
            width=18,
            command=self.drive)
        bt17.place(x=200, y=330)
        bt18 = tk.Button(
            insert_addr,
            text='Exit this window',
            height=1,
            width=18,
            command=insert_addr.destroy)
        bt18.place(x=350, y=330)
        default_radius = tk.StringVar()
        default_radius.set(5000)
        getradius = tk.Entry(
            insert_addr,
            textvariable=default_radius)
        getradius.place(x=210, y=250)
        default_addr = tk.StringVar()
        default_addr.set('Blackwater Mill, Blackwater, Newport, PO30 3BJ')
        getaddress = tk.Entry(
            insert_addr,
            width=50,
            textvariable=default_addr)
        getaddress.place(x=210, y=220)

        # text = tk.Text(insert_addr, width='70', height='6')
        # text.place(x=50, y=380)

        return

    def gorunning(self):
        """
        Put highest point, nearest ITN, shortest path in here.First check the user position is not null.
        Then calculate the path to escape, by highest_point(task 2), nearest_ITN(task 3) and shortestpath(task 4).
        Finally use Map_plotting(task 5) to plot the escape path.
        """
        if self.pt == '':
            tk.messagebox.showwarning(
                title='Please insert your coordinate or address!',
                message='Please insert your coordinate or address!')

        if self.get_radius == '':
            tk.messagebox.showwarning(
                title='Please insert your radius!',
                message='Please insert your radius!')

        # TASK 2
        island_path = self.shp_file
        elevation_path = self.asc_file
        itn_path = self.json_file
        try:
            buffer_range = int(self.get_radius)
        except TypeError:
            tk.messagebox.showerror(title='Error', text='Please enter a buffer distance.')

        out_loc = r'clip.tif'
        print(f'Clipping your input raster to a {buffer_range}m Buffer...')
        hp = HighestPoint(
            self.pt,
            island_path,
            elevation_path,
            out_loc,
            buffer_range)

        clipped_path = hp.clip_elevation()
        highest_point_in_area = hp.find_highest_point(clipped_path)
        print(f'The highest point in your area is {highest_point_in_area} \n')

        # TASK 3
        # example of input coordinate, this will change when we merge the tasks
        itn = ITN(itn_path, self.pt, buffer_range)

        # TASK 4
        # find the closest node for closest algorithm
        user_itn = itn.user_itn()
        node_set = itn.make_tree()[1]
        node_near_user = itn.nearest_node(self.pt)
        node_near_high_point = itn.nearest_node(highest_point_in_area)
        if node_near_user == node_near_high_point:
            print('You are already at the highest point in the area. The system will now exit.')
            sys.exit()
        nearest_node = Point(node_set[node_near_user[0]][1])
        highest_node = Point(node_set[node_near_high_point[0]][1])

        nr = NearestRoad(
            clipped_path,
            self.pt,
            node_near_user,
            node_near_high_point,
            user_itn,
            node_set,
            self.get_radius)

        g = nr.get_road_walk()
        print(f'The route of your journey is displayed on a pop-up map.')
        dijkstra = nr.get_nearest_path(g)
        nr.get_road_drive()

        # TASK 5
        # plot background
        bg_path = self.tif_file
        plot = MapPlotting(
            bg_path,
            dijkstra[0],
            self.pt,
            highest_point_in_area,
            nearest_node,
            highest_node,
            clipped_path)
        plot.plot_map(buffer_range)

    def drive(self):
        """
        Put highest point, nearest ITN, shortest path in here.First check the user position is not null.
        Then calculate the path to escape, by highest_point(task 2), nearest_ITN(task 3) and shortestpath(task 4).
        Finally use Map_plotting(task 5) to plot the escape path.
        """
        if self.pt == '':
            tk.messagebox.showwarning(
                title='Please insert your coordinate or address!',
                message='Please insert your coordinate or address!')

        # TASK 2 -- Find the coordinates of the highest point
        island_path = self.shp_file
        elevation_path = self.asc_file
        itn_path = self.json_file

        buffer_range = self.get_radius
        out_loc = r'clip.tif'
        hp = HighestPoint(
            self.pt,
            island_path,
            elevation_path,
            out_loc,
            buffer_range)
        clipped_path = hp.clip_elevation()
        highest_point_in_area = hp.find_highest_point(clipped_path)
        print(f'The highest point in your area is {highest_point_in_area}')
        # text_1.insert(1.1, str_1)

        # TASK 3 -- Find the closest node to the user's location and the highest point in their buffer size.
        itn = ITN(itn_path, self.pt, buffer_range)

        # TASK 4 -- Calculating the Shortest path between two two nodes from ITN class.
        user_itn = itn.user_itn()
        node_set = itn.make_tree()[1]
        node_near_user = itn.nearest_node(self.pt)
        node_near_high_point = itn.nearest_node(highest_point_in_area)
        if node_near_user == node_near_high_point:
            print('You are already at the highest point in the area. The system will now exit.')
            sys.exit()

        nearest_node = Point(node_set[node_near_user[0]][1])
        highest_node = Point(node_set[node_near_high_point[0]][1])

        nr = NearestRoad(
            clipped_path,
            self.pt,
            node_near_user,
            node_near_high_point,
            user_itn,
            node_set,
            buffer_range)

        g = nr.get_road_walk()
        print(f'The road of your journey is: {g}')
        dijkstra = nr.get_nearest_path(g)
        dijkstra_drive = nr.get_road_drive()
        length_drive = dijkstra_drive[1]
        print(f'Taking vehicles to the highest point in this island may take you {length_drive} minutes')

        # TASK 5 -- Plot the Dijkstra's calculated route.
        bg_path = self.tif_file
        plot = MapPlotting(
            bg_path,
            dijkstra,
            self.pt,
            highest_point_in_area,
            nearest_node,
            highest_node,
            clipped_path)
        plot.plot_drive_path(dijkstra_drive[0])

    def user_coord(self):
        global getx, gety
        """
        First check the user insert point is in the coordinate area, and then check whether the point on the island?
        """
        # Original Task 1, input point.
        x_coord = getx.get()
        y_coord = gety.get()
        x = ''
        y = ''
        if x_coord != "" and y_coord != "":
            try:
                x = float(x_coord)
                y = float(y_coord)
            except NameError:
                tk.messagebox.showerror(
                    title='Wrong insert type',
                    message='Please insert your coordinates in number!')
            if (425000 < x < 470000) and (75000 < y < 100000):
                tk.messagebox.showinfo(
                    title='Welcome', message='Your coordinate is within the study area!')
                # Add task6 to limit the point on the island.
                coord_pt = Point(x, y)
                island_path = self.shp_file
                inisl = InIsland(coord_pt, island_path)
                if inisl.is_inside() is True:
                    self.pt = coord_pt
                    tk.messagebox.showinfo(
                        title='Congratulations',
                        message='You are confirmed to be on the island!')
                    return
                else:
                    tk.messagebox.showinfo(
                        title='Sorry',
                        message='Your position is on the sea, Please check it! \n The programme will stop, '
                                'insert right coordinate or address')
                    return
            else:
                tk.messagebox.showinfo(title='Error',
                                       message='Sorry! Your coordinate is not within the tif area!')
                return
        elif x_coord == "" or y_coord == "":
            tk.messagebox.showerror(title='Error',
                                    message='Sorry! Please Input Coordinate! ')
            return

    def user_addr(self):
        global getaddress
        """
        Check the user input point whether on the island and convert the address to a coordinate point.
        """
        address = ''
        try:
            address = str(getaddress.get())
        except NameError:
            tk.messagebox.showerror(
                title='Wrong insert type',
                message='Please insert your address in string!')
        pt_finder = GoogleMaps(address)
        addr_pt = pt_finder.get_shapely_point()
        island_path = self.shp_file
        inisl = InIsland(addr_pt, island_path)
        if inisl.is_inside() is True:
            tk.messagebox.showinfo(
                title='Congratulations',
                message='You are confirmed to be on the island! Prepare to run!')
            self.pt = addr_pt
            return
        else:
            tk.messagebox.showwarning(
                title='Please confirm your address',
                message='Your are not on the island!')
            return

    def reset_coord(self):
        """
        :return: Resets the coordinate entry boxes on the GUI.
        """
        global getx, gety
        getx.delete(0, 'end')
        gety.delete(0, 'end')
        self.pt = ''
        return

    def reset_addr(self):
        """
        :return:  Resets the address entry boxes on the GUI.
        """
        global getaddress
        getaddress.delete(0, 'end')
        self.pt = ''
        return

    def insert_radius(self):
        """
        :return:  Resets the search radius box on the GUI.
        """
        global getradius
        get_radius_1 = getradius.get()
        if get_radius_1 == '':
            tk.messagebox.showwarning(title='Error', message='Please insert your radius')
            return

        try:
            get_radius_1 = float(getradius.get())
        except NameError:
            tk.messagebox.showerror(
                title='Error', message='Please insert a number!')
        self.get_radius = int(get_radius_1)

        return

    def get_shp(self):
        """
        Get shp file path, and check user choose shp or not by button background.
        """
        filetypes = [("shape_file", "*.shp")]
        self.shp_file = filedialog.askopenfilename(
            title='Please choose your .shp work file', filetypes=filetypes)
        if self.shp_file != '':
            self.bt3.configure(bg='green')
        else:
            self.bt3.configure(bg='red')
        return

    def get_json(self):
        """
        Get json file path, and check user choose shp or not by button background.
        """
        filetypes = [("itn_file", "*.json")]
        self.json_file = filedialog.askopenfilename(
            title='Please choose your .json work file', filetypes=filetypes)
        if self.json_file != '':
            self.bt4.configure(bg='green')
        else:
            self.bt4.configure(bg='red')
        return

    def get_asc(self):
        """
        Get asc file path, and check user choose shp or not by button background.
        """
        filetypes = [("asc_file", "*.asc")]
        self.asc_file = filedialog.askopenfilename(
            title='Please choose your .shp work file', filetypes=filetypes)
        if self.asc_file != '':
            self.bt2.configure(bg='green')
        else:
            self.bt2.configure(bg='red')
        return

    def get_tif(self):
        """
        Get tif file path, and check user choose shp or not by button background.
        """
        filetypes = [("tif_file", "*.tif")]
        self.tif_file = filedialog.askopenfilename(
            title='Please choose your .tif work file', filetypes=filetypes)
        if self.tif_file != '':
            self.bt5.configure(bg='green')
        else:
            self.bt5.configure(bg='red')
        return


class GoogleMaps:
    def __init__(self, address):
        """
        This class will return a shapely point from a google maps search. You can search in any format
        that you like an example (has to be a string): 'Blackwater, Newport, PO30 3BJ'
        :param address: A string of a google maps search
        """
        self.__address = address

    def get_shapely_point(self):
        # You can get a free google maps api key here: https://console.cloud.google.com/
        api_key = '<INSERT YOUR GOOGLE MAPS API KEY>'

        params = {
            'key': api_key,
            'address': self.__address,
        }

        base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        response = requests.get(base_url, params=params)

        geometry = response.json()['results'][0]['geometry']
        lat = geometry['location']['lat']
        lng = geometry['location']['lng']

        wgs84 = pyproj.Proj('+init=EPSG:4326')
        osgb36 = pyproj.Proj('+init=EPSG:27700')

        res = pyproj.transform(wgs84, osgb36, lng, lat)
        users_point = Point(res)

        return users_point


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


class HighestPoint:

    def __init__(self, user_point, island_path, ele_path, out_loc, buffer_range):
        self.__user_point = user_point
        self.__island_path = island_path
        self.__ele_path = ele_path
        self.__out_loc = out_loc
        self.__buffer_range = buffer_range

    def read_island(self):
        """
        Using Geopandas opens and returns a shapefile
        :return: A geopandas shapefile
        """
        island_file = gpd.read_file(self.__island_path)
        return island_file

    def clip_elevation(self):
        """
        Limit the highest point range to a 5km buffer
        Code Adapted from: https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html
        :return: A string path of the clipped elevation raster file (.tif)
        """
        # Open the main raster
        data = rasterio.open(self.__ele_path)

        # Create a 5km buffer from the point first, then turn to gdf
        buffer = self.__user_point.buffer(self.__buffer_range)
        geo = gpd.GeoDataFrame({'geometry': buffer}, index=[0], crs=CRS.from_epsg(27700))

        # Function to parse features from GeoDataFrame in such a manner that rasterio wants them
        clip_extent = [json.loads(geo.to_json())['features'][0]['geometry']]
        out_image, out_transform = rasterio.mask.mask(data, clip_extent, crop=True)
        out_meta = data.meta.copy()

        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform}
                        )

        # Sets the output .tif location
        root = os.path.dirname(os.getcwd())
        out_tif = os.path.join(root, 'Material', 'elevation', self.__out_loc)

        with rasterio.open(out_tif, 'w', **out_meta) as dest:
            dest.write(out_image)

        return out_tif

    @staticmethod
    def find_highest_point(clipped_path):
        """
        Find the highest point and return the coordinates of the highest point
        :return: A shapely point of the highest point in an elevation file (EPSG: 27700)
        """
        with rasterio.open(clipped_path, 'r') as ds:
            arr = ds.read(1)  # read all raster values
            high_point = np.amax(arr)
            res = np.where(arr == high_point)
            highest = ds.xy(res[0], res[1])
            highest_point = Point(highest[0][0], highest[1][0])
            print(f'Your highest point is {highest_point}')

        return highest_point


class ITN:

    def __init__(self, file, user_input, buffer_range):
        self.file = file
        self.user_input = user_input
        self.buffer_range = buffer_range

    def user_itn(self):
        """
        A method for the user to input their ITN Network (JSON file)
        :return: parsed .json data
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
        :return: ID of the nearest node.
        """
        # Find the nearest node in the rTree index
        idx = self.make_tree()[0]
        node_nearest_point = list(idx.nearest((point.x, point.y)))
        return node_nearest_point


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
            within = 0
            # Determine if the road exceeds the buffer zone
            for p in road:
                point = Point(tuple(p))
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
        links = []
        geom = []
        first_node = path_drive[0]
        for node in path_drive[1:]:
            link_fid = g_drive.edges[first_node, node]['fid']
            links.append(link_fid)
            geom.append(LineString(self.road_links[link_fid]['coords']))
            first_node = node
        shortest_path_drive = gpd.GeoDataFrame({'fid': links, 'geometry': geom})

        return shortest_path_drive, length_drive

    def get_nearest_path(self, g):
        """
        A method finding the shortest path based on the network graph created before
        :param g: A network Graph
        :return: The shortest path (line) and the length (m).
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

        return shortest_path_gpd, length


class MapPlotting:

    def __init__(self, bg_path, path, user_input, highest_point, nearest_node, highest_node, clipped_path):
        self.bg_path = bg_path
        self.path = path
        self.user_input = user_input
        self.highest_point = highest_point
        self.nearest_node = nearest_node
        self.highest_node = highest_node
        self.clipped_ele = rasterio.open(clipped_path)
        self.background = rasterio.open(self.bg_path)
        self.back_array = self.background.read(1)

    def plot_map(self, buffer_area):
        """
        Draw the shortest route from the nearest node to the highest node in the buffer, the base map, your position,
        your target position, legend, scale, elevation, etc.
        :return:
        """
        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=crs.OSGB())

        # plot buffer and background
        buffer = plt.Circle((self.user_input.x, self.user_input.y), buffer_area, color="purple", alpha=0.2, zorder=2)
        ax.add_patch(buffer)
        palette = np.array([value for key, value in self.background.colormap(1).items()])
        background_image = palette[self.back_array]
        bounds = self.background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        display_extent = [self.user_input.x-buffer_area, self.user_input.x+buffer_area, self.user_input.y-buffer_area,
                          self.user_input.y+buffer_area]
        ax.imshow(background_image, origin='upper', extent=extent, zorder=0)
        ax.set_extent(display_extent, crs=crs.OSGB())

        # plot path
        self.path.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=3)

        # plot points
        your_location, = plt.plot(self.user_input.x, self.user_input.y, 'o', color='blue', markersize=0.6, zorder=4)
        highest_p, = plt.plot(self.highest_point.x, self.highest_point.y, '^', color='blue', markersize=2, zorder=4)
        nearest_n, = plt.plot(self.nearest_node.x, self.nearest_node.y, 'o', color='red', markersize=0.6, zorder=5)
        highest_n, = plt.plot(self.highest_node.x, self.highest_node.y, '^', color='red', markersize=2, zorder=5)

        # plot elevation and colorbar
        clipped_array = self.clipped_ele.read(1)
        clipped_array[clipped_array == 0] = np.NAN
        ele_bounds = self.clipped_ele.bounds
        ele_extent = [ele_bounds.left, ele_bounds.right, ele_bounds.bottom, ele_bounds.top]
        ele_show = ax.imshow(clipped_array,
                             interpolation='nearest', extent=ele_extent, origin="upper",
                             cmap='terrain', zorder=3, alpha=0.3)
        elebar = plt.colorbar(ele_show, fraction=0.07, pad=0.1)
        elebar.ax.tick_params(labelsize=4)

        # plot the scale bar,
        fontprops = fm.FontProperties(size=4)
        scalebar = AnchoredSizeBar(ax.transData,
                                   2000, '2 km', loc=4,
                                   pad=0.7, color='black', frameon=False,
                                   size_vertical=8, fontproperties=fontprops,)
        ax.add_artist(scalebar)

        # plot the north arrow
        loc_x = 0.9
        loc_y = 0.88
        width = 0.02
        height = 0.05
        pad = 0
        minx, maxx = ax.get_xlim()
        miny, maxy = ax.get_ylim()
        ylen = maxy - miny
        xlen = maxx - minx
        left = [minx + xlen * (loc_x - width * .5), miny + ylen * (loc_y - pad)]
        right = [minx + xlen * (loc_x + width * .5), miny + ylen * (loc_y - pad)]
        top = [minx + xlen * loc_x, miny + ylen * (loc_y - pad + height)]
        center = [minx + xlen * loc_x, left[1] + (top[1] - left[1]) * .4]
        triangle = mpatches.Polygon([left, top, right, center], color='k')
        ax.text(
            s='N',
            x=minx + xlen * loc_x, y=miny + ylen * (loc_y - pad + height) * 1.02,
            fontsize=6, horizontalalignment='center', verticalalignment='bottom')
        ax.add_patch(triangle)

        # plot the legend
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        buffer_l = mpatches.Patch(color="purple", alpha=0.1, label="5km Area")
        shortest_line = mlines.Line2D([], [], linewidth=1, color="blue", markersize=8, label="Shortest Path")
        plt.legend([buffer_l, shortest_line, your_location, highest_p, nearest_n, highest_n],
                   ["Buffer area", "The shortest path", "Your location", "The highest point", "The nearest node",
                    "The highest node"],
                   loc="upper left", fontsize=4)

        # plot title
        plt.title("Emergency Path Planning (for walk)", fontsize=8)
        plt.show()

        return

    def plot_drive_path(self, path):
        """
        Draw a route to the highest point on the island using transportation
        :param path:
        :return:
        """
        highest_point_island = Point(456967.5, 78547.5)
        highest_node = Point(456960.316, 78564.546)
        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=crs.OSGB())

        # plot background
        palette = np.array([value for key, value in self.background.colormap(1).items()])
        background_image = palette[self.back_array]
        bounds = self.background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        ax.imshow(background_image, origin='upper', extent=extent, zorder=0)
        ax.set_extent(extent, crs=crs.OSGB())

        # plot path
        path.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=3)

        # plot points
        your_location, = plt.plot(self.user_input.x, self.user_input.y, 'o', color='blue', markersize=0.6, zorder=4)
        highest_p, = plt.plot(highest_point_island.x, highest_point_island.y, '^', color='blue', markersize=2, zorder=4)
        nearest_n, = plt.plot(self.nearest_node.x, self.nearest_node.y, 'o', color='red', markersize=0.6, zorder=5)
        highest_n, = plt.plot(highest_node.x, highest_node.y, '^', color='red', markersize=2, zorder=5)

        # plot the scale bar,
        fontprops = fm.FontProperties(size=4)
        scalebar = AnchoredSizeBar(ax.transData,
                                   5000, '20 km',
                                   loc=4, pad=0.7, color='black', frameon=False,
                                   size_vertical=8, fontproperties=fontprops, )
        ax.add_artist(scalebar)

        # plot the north arrow
        loc_x = 0.9
        loc_y = 0.87
        width = 0.02
        height = 0.05
        pad = 0
        minx, maxx = ax.get_xlim()
        miny, maxy = ax.get_ylim()
        ylen = maxy - miny
        xlen = maxx - minx
        left = [minx + xlen * (loc_x - width * .5), miny + ylen * (loc_y - pad)]
        right = [minx + xlen * (loc_x + width * .5), miny + ylen * (loc_y - pad)]
        top = [minx + xlen * loc_x, miny + ylen * (loc_y - pad + height)]
        center = [minx + xlen * loc_x, left[1] + (top[1] - left[1]) * .4]
        triangle = mpatches.Polygon([left, top, right, center], color='k')
        ax.text(
            s='N',
            x=minx + xlen * loc_x, y=miny + ylen * (loc_y - pad + height) * 1.02,
            fontsize=6, horizontalalignment='center', verticalalignment='bottom')
        ax.add_patch(triangle)

        # plot the legend
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        shortest_line = mlines.Line2D([], [], linewidth=1, color="blue", markersize=8, label="Shortest Path")
        plt.legend([shortest_line, your_location, highest_p, nearest_n, highest_n],
                   ["The shortest path", "Your location", "The highest point", "The nearest node", "The highest node"],
                   loc="upper left", fontsize=3)

        # plot title
        plt.title("Emergency Path Planning (by vehicle)", fontsize=8)

        plt.show(block=False)

        return


def main():
    """
    Run the program
    """
    window = UserInput()
    window.root.mainloop()


if __name__ == "__main__":
    main()
