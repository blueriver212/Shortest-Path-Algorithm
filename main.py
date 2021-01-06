from nearest_ITN import *
from error_handling import *
from highest_point import *
from GUI import *
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

        self.root = tk.Tk()
        self.root.title('Welcome to files choose system!')
        self.root.geometry('550x250')
        self.bt1 = tk.Button(
            self.root,
            text='Insert Coordinate',
            height=1,
            width=18,
            command=self.insert_coord)
        self.bt1.place(x=350, y=150)
        self.bt2 = tk.Button(
            self.root,
            text='Choose your asc file',
            height=1,
            width=18,
            command=self.get_asc)
        self.bt2.place(x=50, y=50)
        self.bt3 = tk.Button(
            self.root,
            text='Choose your shape file',
            height=1,
            width=18,
            command=self.get_shp)
        self.bt3.place(x=200, y=50)
        self.bt4 = tk.Button(
            self.root,
            text='Choose your json file',
            height=1,
            width=18,
            command=self.get_json)
        self.bt4.place(x=350, y=50)
        self.bt5 = tk.Button(
            self.root,
            text='Choose your tif file',
            height=1,
            width=18,
            command=self.get_tif)
        self.bt5.place(x=50, y=150)
        self.bt6 = tk.Button(
            self.root,
            text='Insert Address',
            height=1,
            width=18,
            command=self.insert_addr)
        self.bt6.place(x=200, y=150)
        self.coord_e = ''
        self.coord_n = ''
        self.shp_file = ''
        self.asc_file = ''
        self.tif_file = ''
        self.json_file = ''
        self.pt = ''

    def insert_coord(self):
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

        self.insert_coord = tk.Toplevel(self.root)
        self.insert_coord.title('Please insert coordinate!')
        self.insert_coord.geometry('550x300')
        self.lb1 = tk.Label(
            self.insert_coord,
            text='Your location X coordinate:').place(
            x=10,
            y=15)
        self.lb2 = tk.Label(
            self.insert_coord,
            text='Your location Y coordinate:').place(
            x=10,
            y=45)
        self.lb3 = tk.Label(self.insert_coord,
                            text='Please insert your escape radius: \n System suggest radius is 5000m').place(x=10,
                                                                                                              y=75)
        self.getx = tk.Entry(self.insert_coord)
        self.getx.place(x=250, y=15)
        self.gety = tk.Entry(self.insert_coord)
        self.gety.place(x=250, y=45)
        default_radius = tk.StringVar()
        default_radius.set('5000')
        self.getradius = tk.Entry(
            self.insert_coord,
            textvariable=default_radius)
        self.getradius.place(x=250, y=80)
        self.bt7 = tk.Button(self.insert_coord, text='Insert your coordinate', height=1, width=18,
                             command=self.user_coord)
        self.bt7.place(x=50, y=150)
        self.bt8 = tk.Button(self.insert_coord, text='Reset your coordinate', height=1, width=18,
                             command=self.reset_coord)
        self.bt8.place(x=200, y=150)
        self.bt9 = tk.Button(self.insert_coord, text='Insert escape radius', height=1, width=18,
                             command=self.insert_radius)
        self.bt9.place(x=350, y=150)
        self.bt10 = tk.Button(
            self.insert_coord,
            text='Go running',
            height=1,
            width=18,
            command=self.gorunning)
        self.bt10.place(x=200, y=250)
        self.bt11 = tk.Button(
            self.insert_coord,
            text='Exit this window',
            height=1,
            width=18,
            command=self.close)
        self.bt11.place(x=350, y=250)

    def insert_addr(self):
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

        self.insert_addr = tk.Toplevel(self.root)
        self.insert_addr.title('Please insert address!')
        self.insert_addr.geometry('550x300')
        self.lb4 = tk.Label(self.insert_addr,
                            text='Please insert your escape radius: \n System suggest radius is 5000m').place(x=10,
                                                                                                              y=75)
        self.bt12 = tk.Button(
            self.insert_addr,
            text='Insert your address',
            height=1,
            width=18,
            command=self.user_addr)
        self.bt12.place(x=50, y=150)
        self.bt13 = tk.Button(
            self.insert_addr,
            text='Reset your address',
            height=1,
            width=18,
            command=self.reset_addr)
        self.bt13.place(x=200, y=150)
        self.bt14 = tk.Button(self.insert_addr, text='Insert escape radius', height=1, width=18,
                              command=self.insert_radius)
        self.bt14.place(x=350, y=150)
        self.bt15 = tk.Button(
            self.insert_addr,
            text='Go running',
            height=1,
            width=18,
            command=self.gorunning)
        self.bt15.place(x=200, y=250)
        self.bt16 = tk.Button(
            self.insert_addr,
            text='Exit this window',
            height=1,
            width=18,
            command=self.close)
        self.bt16.place(x=350, y=250)
        default_radius = tk.StringVar()
        default_radius.set('5000')
        self.getradius = tk.Entry(
            self.insert_addr,
            textvariable=default_radius)
        self.getradius.place(x=250, y=80)
        default_addr = tk.StringVar()
        default_addr.set('eg: Blackwater, Newport, PO30 3BJ')
        self.getaddr = tk.Entry(
            self.insert_addr,
            width=60,
            textvariable=default_addr)
        self.getaddr.place(x=50, y=15)

    def gorunning(self):
        if self.pt == '':
            tk.messagebox.showwarning(
                title='Please insert your coordinate or address!',
                message='Please insert your coordinate or address!')

        # TASK 2

        self.pt = Point(self.coord_e, self.coord_n)
        root = os.path.dirname(os.getcwd())
        island_path = self.shp_file
        elevation_path = self.asc_file
        itn_path = self.json_file

        # Task 6
        # Testing whether the user point is on the island.
        inisl = InIsland(self.pt, island_path)
        if inisl.is_inside() is True:
            print('You are confirmed to be on the island! \n'
                  'The software will continue')
        else:
            print('Unfortunately, you are not on the Isle of Wight, so this program cannot help you. \n'
                  'This software is now shutting down')
            sys.exit()

        buffer_range = float(
            input("please input the radius of your buffer area:"))
        out_loc = r'clip.tif'
        print(f'Clipping your input raster to a {buffer_range}km Buffer...')
        hp = HighestPoint(
            self.pt,
            island_path,
            elevation_path,
            out_loc,
            buffer_range)
        clipped_path = hp.clip_elevation()
        highest_point_in_area = hp.find_highest_point(clipped_path)
        print(f'The highest point in your area is {highest_point_in_area}')

        # TASK 3
        # example of input coordinate, this will change when we merge the tasks
        # together

        # Get the error handling from sep document
        json_file = Errors.json_input()
        itn = ITN(json_file)
        print('Calculating the nearest road nodes to you...')

        # TASK 4
        # find the closest node for closest algorithm
        user_itn = itn.user_itn()
        node_set = itn.make_tree()[1]
        node_near_user = itn.nearest_node(self.pt)
        node_near_high_point = itn.nearest_node(highest_point_in_area)
        print(f'The node nearest you is {node_near_user} \n'
              f'The node nearest to the highest point is {node_near_high_point}')

        nr = NearestRoad(
            elevation_path,
            self.pt,
            node_near_user,
            node_near_high_point,
            user_itn,
            node_set)

        g = nr.get_road_walk()
        print(f'The road of your journey is: {g}')
        dijkstra = nr.get_nearest_path(g)
        dijkstra_drive = nr.get_road_drive()

        # TASK 5
        # plot background
        bg_path = self.tif_file
        nearest_node = Point(node_set[node_near_user[0]][1])
        highest_node = Point(node_set[node_near_high_point[0]][1])
        plot = MapPlotting(
            bg_path,
            dijkstra,
            self.pt,
            highest_point_in_area,
            nearest_node,
            highest_node,
            clipped_path)
        plot_walk = plot.plot_map(buffer_range)
        plot_drive = plot.plot_drive_path(dijkstra_drive)

    def user_coord(self):
        x_coord = self.getx.get()
        y_coord = self.gety.get()
        if x_coord != "" and y_coord != "":
            try:
                x = float(x_coord)
                y = float(y_coord)
                if (425000 < x < 470000) and (75000 < y < 100000):
                    tk.messagebox.showinfo(
                        title='Welcome', message='Your coordinate is within the study area!')
                    self.coord_e = x
                    self.coord_n = y
                    self.pt = Point(self.coord_e, self.coord_n)
                    island_path = self.shp_file
                    inisl = InIsland(self.pt, island_path)
                    if inisl.is_inside() is True:
                        tk.messagebox.showinfo(
                            title='Congratulations',
                            message='You are confirmed to be on the island!')
                        return self.pt
                    else:
                        tk.messagebox.showinfo(
                            title='Sorry',
                            message='Your position is on the sea, Please check it! \n The programme will stop, insert right coordinate or address')
                        self.insert_coord.destroy()
                else:
                    tk.messagebox.showinfo(title='Error',
                                           message='Sorry! Your coordinate is not within the tif area!')
                    return
            except BaseException:
                tk.messagebox.showerror(
                    title='Error', message='Sorry! Please input it in correct number type!')
                return
        elif x_coord == "" or y_coord == "":
            tk.messagebox.showerror(title='Error',
                                    message='Sorry! Please Input Coordinate! ')
            return

    def user_addr(self):
        address_get = self.getaddr.get()
        address = str(address_get)
        pt_finder = GoogleMaps(address)
        addr_pt = pt_finder.get_shapely_point()
        island_path = self.shp_file
        inisl = InIsland(addr_pt, island_path)
        if inisl.is_inside() is True:
            tk.messagebox.showinfo(
                title='Congratulations',
                message='You are confirmed to be on the island! Prepare to run!')
            self.pt = addr_pt
            return self.pt
        else:
            tk.messagebox.showwarning(
                title='Please confirm your address',
                message='Your are not on the island!')
            return

    def reset_coord(self):
        self.getx.delete(0, 'end')
        self.gety.delete(0, 'end')
        return

    def reset_addr(self):
        self.getaddr.delete(0, 'end')
        return

    def insert_radius(self):
        self.get_radius = float(self.getradius.get())
        return

    def close(self):
        if tk.messagebox.askokcancel(
                "Close", "Do you want to close the software?"):
            self.insert_coord.destroy()
        return

    def get_shp(self):
        filetypes = [("shape_file", "*.shp")]
        self.shp_file = filedialog.askopenfilename(
            title='Please choose your .shp work file', filetypes=filetypes)
        return

    def get_json(self):
        filetypes = [("itn_file", "*.json")]
        self.json_file = filedialog.askopenfilename(
            title='Please choose your .json work file', filetypes=filetypes)
        return

    def get_asc(self):
        filetypes = [("asc_file", "*.asc")]
        self.asc_file = filedialog.askopenfilename(
            title='Please choose your .shp work file', filetypes=filetypes)
        return

    def get_tif(self):
        filetypes = [("tif_file", "*.tif")]
        self.tif_file = filedialog.askopenfilename(
            title='Please choose your .tif work file', filetypes=filetypes)
        return


def main():
    window = UserInput()
    window.root.mainloop()


if __name__ == "__main__":
    main()
