import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import requests
import json

class UserInput:

    def __init__(self):

        self.window = tk.Tk()
        self.window.title('Welcome to User Coordinate Input!')
        self.window.geometry('450x300')
        self.lb1 = tk.Label(self.window, text='Your location X coordinate:').place(x=10, y=15)
        self.lb2 = tk.Label(self.window, text='Your location Y coordinate:').place(x=10, y=45)
        self.lb3 = tk.Label(self.window, text='Please insert your postcode:').place(x=10, y=45)
        self.lb4 = tk.Label(self.window, text='').place(x=10, y=100)
        self.getx = tk.Entry()
        self.getx.place(x=170, y=15)
        self.gety = tk.Entry()
        self.gety.place(x=170, y=45)
        self.getcoord = tk.Entry()
        self.getcoord.place(x=300, y=15)
        self.bt1 = tk.Button(self.window, text='Insert your coordinate', height=1, width=18, command=self.user_input)
        self.bt1.place(x=50, y=150)
        self.bt2 = tk.Button(self.window, text='Reset your coordinate', height=1, width=18, command=self.reset)
        self.bt2.place(x=200, y=150)
        self.bt3 = tk.Button(self.window, text='Exit', height=1, width=18, command=self.close)
        self.bt3.place(x=350, y=150)
        self.bt4 = tk.Button(self.window, text='Choose your asc file', height=1, width=18, command=self.get_asc)
        self.bt4.place(x=50, y=200)
        self.bt5 = tk.Button(self.window, text='Choose your shape file', height=1, width=18, command=self.get_shp)
        self.bt5.place(x=200, y=200)
        self.bt6 = tk.Button(self.window, text='Choose your json file', height=1, width=18, command=self.get_json)
        self.bt6.place(x=350, y=200)
        self.coord_e = ""
        self.coord_n = ""


    def user_input(self):
        x_coord = self.getx.get()
        y_coord = self.gety.get()
        postcode = self.getcoord.get()
        if x_coord != "" and y_coord != "":
            while True:
                try:
                    x = float(x_coord)
                    y = float(y_coord)
                except ValueError:
                    #https://postcodes.io/docs
                    #https://github.com/ideal-postcodes/postcodes.io/
                    pc = str(postcode).replace("","")
                    r = requests.get('https://api.postcodes.io/postcodes/' + str(pt))
                    if api.status_code != 404:
                        json_data = json.loads(r.text)
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
                        self.coord_e = x
                        self.coord_n = y
                        return
                    else:
                        tk.messagebox.showinfo(title='Error',
                                               message='Sorry! Your coordinate is not within the study area!')
                        return
        elif x_coord == "" or y_coord == "":
            tk.messagebox.showinfo(title='Error', message='Sorry! Please Enter Coordinate in right formal! ')
            return
        self.window.destroy()
        return


    def reset(self):
        self.getx.delete(0, 'end')
        self.gety.delete(0, 'end')
        self.getcoord.delete(0, 'end')
        return


    def close(self):
        if tk.messagebox.askokcancel("Close", "Do you want to close the software?"):
            self.window.destroy()
            print("Closed by User")
        return


    def get_shp(self):
        filetypes = [("shape_file", "*.shp")]
        shp_file = filedialog.askopenfilename(title='Please choose your .shp work file', filetypes=filetypes)
        return shp_file


    def get_json(self):
        filetypes = [("itn_file", "*.json")]
        json_file = filedialog.askopenfilename(title='Please choose your .json work file', filetypes=filetypes)
        return json_file


    def get_asc(self):
        filetypes = [("asc_file", "*.asc")]
        asc_file = filedialog.askopenfilename(title='Please choose your .shp work file', filetypes=filetypes)
        return asc_file

