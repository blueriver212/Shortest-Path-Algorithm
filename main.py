from nearest_ITN import *
from error_handling import *
from highest_point import *
from shortestpath import *
from Map_plotting import *
from task6 import *
from GoogleMapsAPI import *
import os
import sys
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog


class UserInput:

    def __init__(self):
        """
        This class will include the GUI windows and tell user how to use the escape system. The main window let user
        choose work files and choose coordinate or address they want to insert,and then insert it and choose escape way.
        """
        self.root = tk.Tk()
        self.root.title('Welcome to files choose system!')
        self.lb1 = tk.Label(
            self.root,
            text="Operate guide: first you need to choose four work file,when the four choose\nfile buttons turn "
                 "green, your are do it right then choose to input your coordinate\nor address, click the "
                 "corresponding button. If you do not choose the whole four\nwork files the corresponding "
                 "button will be white or red!\nFuther instructions will be show after you choose address "
                 "or coordinate.\nPlease do not type any thing on white area, this area will show your status!",
            bg='white',
            anchor="center",
            justify="left",
            fg="red",
            heigh=6,
            width=61).place(
            x=50,
            y=65)
        self.bt1 = tk.Button(
            self.root,
            text='Insert Coordinate',
            height=1,
            width=18,
            command=self.insert_coord)
        self.bt1.place(x=350, y=180)
        self.bt2 = tk.Button(
            self.root,
            text='Choose your asc file',
            height=1,
            width=18,
            command=self.get_asc)
        self.bt2.place(x=50, y=20)
        self.bt3 = tk.Button(
            self.root,
            text='Choose your shape file',
            height=1,
            width=18,
            command=self.get_shp)
        self.bt3.place(x=200, y=20)
        self.bt4 = tk.Button(
            self.root,
            text='Choose your json file',
            height=1,
            width=18,
            command=self.get_json)
        self.bt4.place(x=350, y=20)
        self.bt5 = tk.Button(
            self.root,
            text='Choose your tif file',
            height=1,
            width=18,
            command=self.get_tif)
        self.bt5.place(x=50, y=180)
        self.bt6 = tk.Button(
            self.root,
            text='Insert Address',
            height=1,
            width=18,
            command=self.insert_addr)
        self.bt6.place(x=200, y=180)
        self.coord_e = ''
        self.coord_n = ''
        self.shp_file = ''
        self.asc_file = ''
        self.tif_file = ''
        self.json_file = ''
        self.pt = ''
        self.get_radius = ''
        self.text = tk.Text(self.root, height=12, width=75)
        self.text.place(x=10, y=250)
        # Root window show in mid screen
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        width = 550
        height = 450
        midshow = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(midshow)

    def insert_coord(self):
        """
        Design a user insert coordinate GUI use Insert coordinate button to check the coordinate point position.
        Reset button clear the user insert label. Get radius button to insert the escape radius.
        Go running button to calculate the escape path.
        Exit button let user to close the window.
        :return:
        """
        if self.shp_file == '':
            tk.messagebox.showwarning(
                title='No shp file',
                message='There is no shp.file, please input shp.file')
            return
        if self.json_file == '':
            tk.messagebox.showwarning(
                title='No json file',
                message='There is no json.file, please input json.file')
            return
        if self.asc_file == '':
            tk.messagebox.showwarning(
                title='No asc file',
                message='There is no asc.file, please input asc.file')
            return
        if self.tif_file == '':
            tk.messagebox.showwarning(
                title='No tif file',
                message='There is no tif.file, please input tif.file')
            return

        insert_coord = tk.Toplevel(self.root)
        insert_coord.title('Please insert coordinate!')
        insert_coord.geometry('550x300')
        lb2 = tk.Label(
            insert_coord,
            text='Your location X coordinate:').place(
            x=10,
            y=15)
        lb3 = tk.Label(
            insert_coord,
            text='Your location Y coordinate:').place(
            x=10,
            y=45)
        lb4 = tk.Label(insert_coord,
                       text='Please insert your escape radius:\nSystem suggest radius is 5000m').place(x=10,
                                                                                                       y=75)
        lb5 = tk.Label(insert_coord,
                       text="Please enter your latitude and longitude coordinates on the island.\nExample:      "
                            "X Coordinate:439619       Y coordinate:85800 \nAfter the input is completed, "
                            "click the Insert button. If the prompt is successful,\nclick the Go Running or By vehicle "
                            "button. Otherwise, please enter the correct coordinate.\nIf you want to enter the "
                            "coordinates again, please click the Reset button.\nIf you want to enter the address, "
                            "please click the Exit button first When you click Go running or By vehicle button\n"
                            "please check your status in file choose window",
                       bg='white', anchor="center", justify="left", fg="red", heigh=6, width=61).place(x=50, y=110)
        self.getx = tk.Entry(insert_coord)
        self.getx.place(x=250, y=15)
        self.gety = tk.Entry(insert_coord)
        self.gety.place(x=250, y=45)
        default_radius = tk.StringVar()
        default_radius.set('5000')
        self.getradius = tk.Entry(
            insert_coord,
            textvariable=default_radius)
        self.getradius.place(x=250, y=80)
        bt7 = tk.Button(insert_coord, text='Insert your coordinate', height=1, width=18,
                        command=self.user_coord)
        bt7.place(x=50, y=210)
        bt8 = tk.Button(insert_coord, text='Reset your coordinate', height=1, width=18,
                        command=self.reset_coord)
        bt8.place(x=200, y=210)
        bt9 = tk.Button(insert_coord, text='Insert escape radius', height=1, width=18,
                        command=self.insert_radius)
        bt9.place(x=350, y=210)
        bt10 = tk.Button(
            insert_coord,
            text='Go running',
            height=1,
            width=18,
            command=self.gorunning)
        bt10.place(x=50, y=250)
        bt11 = tk.Button(
            insert_coord,
            text='By vehicle',
            height=1,
            width=18,
            command=self.drive)
        bt11.place(x=200, y=250)
        bt12 = tk.Button(
            insert_coord,
            text='Exit this window',
            height=1,
            width=18,
            command=insert_coord.destroy)
        bt12.place(x=350, y=250)

    def insert_addr(self):
        """
        Design a user insert address GUI use Insert address button to convert address to coordinate point,
        Reset button clear the user insert label. Get radius button to insert the escape radius.
        Go running button to calculate the escape path.
        Exit button let user to close the window.
        :return:
        """

        if self.shp_file == '':
            tk.messagebox.showwarning(
                title='No shp file',
                message='There is no shp.file, please input shp.file')
            return
        if self.json_file == '':
            tk.messagebox.showwarning(
                title='No json file',
                message='There is no json.file, please input json.file')
            return
        if self.asc_file == '':
            tk.messagebox.showwarning(
                title='No asc file',
                message='There is no asc.file, please input asc.file')
            return
        if self.tif_file == '':
            tk.messagebox.showwarning(
                title='No tif file',
                message='There is no tif.file, please input tif.file')
            return

        insert_addr = tk.Toplevel(self.root)
        insert_addr.title('Please insert address!')
        insert_addr.geometry('550x300')
        lb6 = tk.Label(insert_addr,
                       text='Please insert your escape radius:\nSystem suggest radius is 5000m').place(x=10,
                                                                                                       y=45)
        lb7 = tk.Label(insert_addr,
                       text="Please enter your address on the island.\nExample:      Address: Blackwater, Newport, "
                            "PO30 3BJ\nAfter the input is completed, click the Insert button. If the prompt is "
                            "successful,\nclick the Go Running or By vehicle button to escape.\nOtherwise, please enter"
                            "the correct address.\nIf you want to enter the address again, please click the Reset "
                            "button.\nIf you want to enter the coordinates, please click the Exit button. When you\n"
                            "click Go running or By vehicle button please check your status in file choose window",
                       bg='white', anchor="center", justify="left", fg="red", heigh=7, width=61).place(x=50, y=100)
        bt13 = tk.Button(
            insert_addr,
            text='Insert your address',
            height=1,
            width=18,
            command=self.user_addr)
        bt13.place(x=50, y=220)
        bt14 = tk.Button(
            insert_addr,
            text='Reset your address',
            height=1,
            width=18,
            command=self.reset_addr)
        bt14.place(x=200, y=220)
        bt15 = tk.Button(insert_addr, text='Insert escape radius', height=1, width=18,
                         command=self.insert_radius)
        bt15.place(x=350, y=220)
        bt16 = tk.Button(
            insert_addr,
            text='Go running',
            height=1,
            width=18,
            command=self.gorunning)
        bt16.place(x=50, y=250)
        bt17 = tk.Button(
            insert_addr,
            text='By vehicle',
            height=1,
            width=18,
            command=self.drive)
        bt17.place(x=200, y=250)
        bt18 = tk.Button(
            insert_addr,
            text='Exit this window',
            height=1,
            width=18,
            command=insert_addr.destroy)
        bt18.place(x=350, y=250)
        default_radius = tk.StringVar()
        default_radius.set('5000')
        self.getradius = tk.Entry(
            insert_addr,
            textvariable=default_radius)
        self.getradius.place(x=250, y=50)
        default_addr = tk.StringVar()
        default_addr.set('eg: Blackwater, Newport, PO30 3BJ')
        self.getaddr = tk.Entry(
            insert_addr,
            width=60,
            textvariable=default_addr)
        self.getaddr.place(x=50, y=15)

    def gorunning(self):
        """
        Put highest point, nearest ITN, shortest path in here.First check the user position is not null.
        Then calculate the path to escape, by highest_point(task 2), nearest_ITN(task 3) and shortestpath(task 4).
        Finally use Map_plotting(task 5) to plot the escape path.
        :return:
        """

        if self.pt == '':
            tk.messagebox.showwarning(
                title='Please insert your coordinate or address!',
                message='Please insert your coordinate or address!')
        if self.getradius == '':
            tk.messagebox.showwarning(
                title='Please insert your radius!',
                message='Please insert your radius!')

        # TASK 2

        root = os.path.dirname(os.getcwd())
        island_path = self.shp_file
        elevation_path = self.asc_file
        itn_path = self.json_file

        buffer_range = self.get_radius
        out_loc = r'clip.tif'
        print(f'Clipping your input raster to a {buffer_range}m Buffer...')
        str_1 = f'Clipping your input raster to a {buffer_range}m Buffer...'
        self.text.insert(1.1, str_1)
        hp = HighestPoint(
            self.pt,
            island_path,
            elevation_path,
            out_loc,
            buffer_range)
        clipped_path = hp.clip_elevation()
        highest_point_in_area = hp.find_highest_point(clipped_path)
        str_2 = f'The highest point in your area is {highest_point_in_area}'
        self.text.insert(2.1, str_2)

        # TASK 3
        # example of input coordinate, this will change when we merge the tasks
        # together

        # Get the error handling from sep document
        json_file = Errors.json_input()
        itn = ITN(json_file,self.pt, buffer_range)

        str_3 = 'Calculating the nearest road nodes to you...'
        self.text.insert(3.1, str_3)

        # TASK 4
        # find the closest node for closest algorithm
        user_itn = itn.user_itn()
        node_set = itn.make_tree()[1]
        node_near_user = itn.nearest_node(self.pt)
        node_near_high_point = itn.nearest_node(highest_point_in_area)
        nearest_node = Point(node_set[node_near_user[0]][1])
        highest_node = Point(node_set[node_near_high_point[0]][1])
        str_4 = f'The node nearest you is {node_near_user} \n ' \
                f'The node nearest to the highest point is {node_near_high_point}'
        self.text.insert(4.1, str_4)

        nr = NearestRoad(
            clipped_path,
            self.pt,
            node_near_user,
            node_near_high_point,
            user_itn,
            node_set,
            self.get_radius)

        g = nr.get_road_walk()
        str_5 = f'The road of your journey is: {g}'
        self.text.insert(6.1, str_5)
        dijkstra = nr.get_nearest_path(g)
        dijkstra_drive = nr.get_road_drive()

        # TASK 5
        # plot background
        bg_path = self.tif_file
        plot = MapPlotting(
            bg_path,
            dijkstra,
            self.pt,
            highest_point_in_area,
            nearest_node,
            highest_node,
            clipped_path)
        plot_walk = plot.plot_map(buffer_range)

    def drive(self):
        """
        Put highest point, nearest ITN, shortest path in here.First check the user position is not null.
        Then calculate the path to escape, by highest_point(task 2), nearest_ITN(task 3) and shortestpath(task 4).
        Finally use Map_plotting(task 5) to plot the escape path.
        :return:
        """

        if self.pt == '':
            tk.messagebox.showwarning(
                title='Please insert your coordinate or address!',
                message='Please insert your coordinate or address!')

        # TASK 2

        root = os.path.dirname(os.getcwd())
        island_path = self.shp_file
        elevation_path = self.asc_file
        itn_path = self.json_file

        buffer_range = self.get_radius
        out_loc = r'clip.tif'
        print(f'Clipping your input raster to a {buffer_range}m Buffer...')
        str_1 = f'Clipping your input raster to a {buffer_range}m Buffer...'
        self.text.insert(1.1, str_1)
        hp = HighestPoint(
            self.pt,
            island_path,
            elevation_path,
            out_loc,
            buffer_range)
        clipped_path = hp.clip_elevation()
        highest_point_in_area = hp.find_highest_point(clipped_path)
        str_2 = f'The highest point in your area is {highest_point_in_area}'
        self.text.insert(2.1, str_2)


        # TASK 3
        # example of input coordinate, this will change when we merge the tasks
        # together

        # Get the error handling from sep document
        json_file = Errors.json_input()
        itn = ITN(json_file, self.pt, buffer_range)

        str_3 = 'Calculating the nearest road nodes to you...'
        self.text.insert(3.1, str_3)

        # TASK 4
        # find the closest node for closest algorithm
        user_itn = itn.user_itn()
        node_set = itn.make_tree()[1]
        node_near_user = itn.nearest_node(self.pt)
        node_near_high_point = itn.nearest_node(highest_point_in_area)
        nearest_node = Point(node_set[node_near_user[0]][1])
        highest_node = Point(node_set[node_near_high_point[0]][1])
        str_4 = f'The node nearest you is {node_near_user} \n ' \
                f'The node nearest to the highest point is {node_near_high_point}'
        self.text.insert(4.1, str_4)


        nr = NearestRoad(
            clipped_path,
            self.pt,
            node_near_user,
            node_near_high_point,
            user_itn,
            node_set
            buffer_range)

        g = nr.get_road_walk()
        str_5 = f'The road of your journey is: {g}'
        self.text.insert(6.1, str_5)
        dijkstra = nr.get_nearest_path(g)
        dijkstra_drive = nr.get_road_drive()

        # TASK 5
        # plot background
        bg_path = self.tif_file
        plot = MapPlotting(
            bg_path,
            dijkstra,
            self.pt,
            highest_point_in_area,
            nearest_node,
            highest_node,
            clipped_path)
        plot_drive = plot.plot_drive_path(dijkstra_drive)

    def user_coord(self):
        """
        First check the user insert point is in the coordinate area, and then check whether the point on the island?
        :return:
        """
        # Original Task 1, input point.
        x_coord = self.getx.get()
        y_coord = self.gety.get()
        if x_coord != "" and y_coord != "":
            try:
                x = float(x_coord)
                y = float(y_coord)
            except BaseException:
                tk.messagebox.showerror(
                    title='Wrong insert type',
                    message='Please insert your coordinates in number!')
            if (425000 < x < 470000) and (75000 < y < 100000):
                tk.messagebox.showinfo(
                    title='Welcome', message='Your coordinate is within the study area!')
                self.coord_e = x
                self.coord_n = y
                # Add task6 to limit the point on the island.
                coord_pt = Point(self.coord_e, self.coord_n)
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
        """
        Check the user input point whether on the island and convert the address to a coordinate point.
        :return:
        """
        address_get = self.getaddr.get()
        try:
            address = str(address_get)
        except BaseException:
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
        Reset the user insert coordinate entry.
        :return:
        """
        self.getx.delete(0, 'end')
        self.gety.delete(0, 'end')
        return

    def reset_addr(self):
        """
        Reset the user insert address entry.
        :return:
        """
        self.getaddr.delete(0, 'end')
        return

    def insert_radius(self):
        """
        Get the user insert radius.
        :return:
        """
        try:
            get_radius_1 = float(self.getradius.get())
        except BaseException:
            tk.messagebox.showerror(
                title='Error', message='Please insert a number!')
        self.get_radius = get_radius_1
        return

    def get_shp(self):
        """
        Get shp file path, and check user choose shp or not by button background.
        :return:
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
        :return:
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
        :return:
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
        :return:
        """
        filetypes = [("tif_file", "*.tif")]
        self.tif_file = filedialog.askopenfilename(
            title='Please choose your .tif work file', filetypes=filetypes)
        if self.tif_file != '':
            self.bt5.configure(bg='green')
        else:
            self.bt5.configure(bg='red')
        return


def main():
    """
    Run the program
    :return:
    """
    window = UserInput()
    window.root.mainloop()


if __name__ == "__main__":
    main()
