from nearest_ITN import *
from error_handling import *
from shapely.geometry import Point, Polygon
from highest_point import *
from GUI import *
from shortestpath import *
from Map_plotting import *
from task6 import *
import os
import sys
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import requests
import json

def main():
    global getx,gety,getcoord,window,shp_file,json_file,asc_file
    window = tk.Tk()
    window.title('Welcome to User Coordinate Input!')
    window.geometry('560x300')
    lb1 = tk.Label(window, text='Your location X coordinate:').place(x=10, y=15)
    lb2 = tk.Label(window, text='Your location Y coordinate:').place(x=10, y=45)
    lb3 = tk.Label(window, text='Please insert your postcode:').place(x=10, y=75)
    lb4 = tk.Label(window, text='').place(x=10, y=100)
    getx = tk.Entry()
    getx.place(x=250, y=15)
    shp_file=''
    json_file=''
    asc_file=''
    gety = tk.Entry()
    gety.place(x=250, y=45)
    getcoord = tk.Entry()
    getcoord.place(x=250, y=75)
    bt1 = tk.Button(window, text='Insert your coordinate', height=1, width=18, command=user_input)
    bt1.place(x=50, y=150)
    bt2 = tk.Button(window, text='Reset your coordinate', height=1, width=18, command=reset)
    bt2.place(x=200, y=150)
    bt3 = tk.Button(window, text='Exit', height=1, width=18, command=close)
    bt3.place(x=350, y=150)
    bt4 = tk.Button(window, text='Choose your asc file', height=1, width=18, command=get_asc)
    bt4.place(x=50, y=200)
    bt5 = tk.Button(window, text='Choose your shape file', height=1, width=18, command=get_shp)
    bt5.place(x=200, y=200)
    bt6 = tk.Button(window, text='Choose your json file', height=1, width=18, command=get_json)
    bt6.place(x=350, y=200)
    bt6 = tk.Button(window, text='Go running', height=1, width=18, command=gorunning)
    bt6.place(x=200, y=250)
    window.mainloop()
    

def gorunning():
    global getx,gety,getcoord,shp_file,json_file,asc_file
    if getx=='':
        print('please input x')
        return
    if gety=='':
        print('please input y')
        return
    if getcoord=='':
        print('please input x')
        return
    if shp_file=='':
        print('please input shp.file')
        return
    if json_file=='':
        print('please input json.file')
        return
    if asc_file=='':
        print('please input asc.file')
        return
    coord_e = float(getx.get())
    coord_n = float(gety.get())
    ## TASK 1
    # creating window using the UserInput class
    # root = UserInput()
    # coord = root.user_input()
    # root.window.mainloop()

    # TASK 2
    pt = Point(coord_e, coord_n)
    root = os.path.dirname(os.getcwd())
    island_path = shp_file
    elevation_path = asc_file
    itn_path = json_file

    # Task 6
    # Testing whether the user point is on the island.
    inisl = InIsland(pt, island_path)
    if inisl.is_inside() is True:
        print('You are confirmed to be on the island! \n'
              'The software will continue')
    else:
        print('Unfortunately, you are not on the Isle of Wight, so this program cannot help you. \n'
              'This software is now shutting down')
        sys.exit()


    out_loc = r'clip.tif'
    print('Clipping your input raster to a 5km Buffer...')
    hp = HighestPoint(pt, island_path, elevation_path, out_loc)
    clipped_path = hp.clip_elevation()
    highest_point_in_area = hp.find_highest_point(clipped_path)
    print(f'The highest point in your area is {highest_point_in_area}')

    # TASK 3
    # example of input coordinate, this will change when we merge the tasks together

    # Get the error handling from sep document
    json_file = Errors.json_input()
    itn = ITN(json_file)
    print('Calculating the nearest road nodes to you...')

    # TASK 4
    # find the closest node for closest algorithm
    user_itn = itn.user_itn()
    node_set = itn.make_tree()[1]
    node_near_user = itn.nearest_node(pt)
    node_near_high_point = itn.nearest_node(highest_point_in_area)
    print(f'The node nearest you is {node_near_user} \n'
          f'The node nearest to the highest point is {node_near_high_point}')

    nr = NearestRoad(elevation_path, node_near_user, node_near_high_point,user_itn,node_set)

    g = nr.get_road()
    print(f'The road of your journey is: {g}')
    dijkstra = nr.get_nearest_path(g)

    #TASK 5
    # plot background
    bg_file = 'raster-50k_2724246.tif'
    bg_path = os.path.join(root, 'Material', 'background', bg_file,)
    nearest_node = Point(node_set[node_near_user[0]][1])
    highest_node = Point(node_set[node_near_high_point[0]][1])
    plot_bg = MapPlotting(bg_path,dijkstra,pt,highest_point_in_area,nearest_node,highest_node,clipped_path).plot_map()
    
def user_input():
        global getx,gety,getcoord,window
        x_coord = getx.get()
        y_coord = gety.get()
        postcode = getcoord.get()
        if x_coord != "" and y_coord != "":
            while True:
                try:
                    x = float(x_coord)
                    y = float(y_coord)
                except ValueError:
                    pc = str(postcode).replace("","")
                    resp = requests.get('https://api.postcodes.io/postcodes/' + str(pc))
                    if api.status_code != 404:
                        json_data = json.loads(resp.text)
                        pce = json_data["result"]["eastings"]
                        pcn = json_data["result"]["nortings"]
                        x = float(pce)
                        y = float(pcn)
                        break
                    else:
                        tk.messagebox.showinfo(title='Error', message='Sorry! Your postcode is wrong!')
                        return
                else:
                    if (425000 < x < 470000) and (75000 < y < 100000):
                        tk.messagebox.showinfo(title='Welcome', message='Your coordinate is within the study area!')
                        coord_e = x
                        coord_n = y
                        return
                    else:
                        tk.messagebox.showinfo(title='Error',
                                               message='Sorry! Your coordinate is not within the study area!')
                        return
        elif x_coord == "" or y_coord == "":
            tk.messagebox.showinfo(title='Error', message='Sorry! Please Enter Coordinate in right formal! ')
            return
        window.destroy()
        return


def reset():
    global getx,gety,getcoord
    getx.delete(0, 'end')
    gety.delete(0, 'end')
    getcoord.delete(0, 'end')
    return


def close():
    global window
    if tk.messagebox.askokcancel("Close", "Do you want to close the software?"):
        window.destroy()
        print("Closed by User")
    return


def get_shp():
    global shp_file
    filetypes = [("shape_file", "*.shp")]
    shp_file = filedialog.askopenfilename(title='Please choose your .shp work file', filetypes=filetypes)
    return shp_file


def get_json():
    global json_file
    filetypes = [("itn_file", "*.json")]
    json_file = filedialog.askopenfilename(title='Please choose your .json work file', filetypes=filetypes)
    print(f'This is the json file {json_file}')
    return json_file

def get_asc():
    global asc_file
    filetypes = [("asc_file", "*.asc")]
    asc_file = filedialog.askopenfilename(title='Please choose your .shp work file', filetypes=filetypes)
    return asc_file






if __name__ == "__main__":
    main()

