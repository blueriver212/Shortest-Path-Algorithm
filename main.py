<<<<<<< HEAD
import tkinter as tk
import tkinter.messagebox
=======
from input_from_user import *
from nearest_ITN import *
from error_handling import *
from shapely.geometry import *
>>>>>>> 0f6b9fc8aa8ae5be5d1b67811ea0e2fa1d0598ee

class UserInput:

<<<<<<< HEAD
    def __init__(self):

        self.window = tk.Tk()
        self.window.title('Welcome to User Coordinate Input!')
        self.window.geometry('450x300')
        self.lb1 = tk.Label(self.window, text='Your location X coordinate:').place(x=10, y=15)
        self.lb2 = tk.Label(self.window, text='Your location Y coordinate:').place(x=10, y=45)
        self.lb3 = tk.Label(self.window, text='').place(x=10, y=100)
        self.getx = tk.Entry()
        self.getx.place(x=170, y=15)
        self.gety = tk.Entry()
        self.gety.place(x=170, y=45)
        self.bt1 = tk.Button(self.window, text='Insert your coordinate', command=self.user_input)
        self.bt1.place(x=50, y=150)
        self.bt2 = tk.Button(self.window, text='Reset your coordinate', command=self.reset)
        self.bt2.place(x=200, y=150)
        self.bt3 = tk.Button(self.window, text='Exit', command=self.close)
        self.bt3.place(x=350, y=150)


    def user_input(self):
        x_coord = self.getx.get()
        y_coord = self.gety.get()
        if x_coord != "" and y_coord != "":
            while True:
                try:
                    x = float(x_coord)
                    y = float(y_coord)
                except ValueError:
                    tk.messagebox.showinfo(title='Error', message='Sorry! Your coordinate should in float!')
                    return
                else:
                    if (430000 < x < 465000) and (80000 < y < 95000):
                        tk.messagebox.showinfo(title='Welcome', message='Your coordinate is within the study area!')
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
        getx.delete(0, 'end')
        gety.delete(0, 'end')
        return


    def close(self):
        if tk.messagebox.askokcancel("Close", "Do you want to close the software?"):
            self.window.destroy()
            print("Closed by User")

def main():
    # creating window using the UserInput class
    root = UserInput()
    root.window.mainloop()
=======
def task1():
    coordinate = user()
    coord_input(coordinate)

def task2():
    pass

def task3():
    # example of input coordinate, this will change when we merge the tasks together
    coord = Point(434000, 90000)
    highest = Point(439619, 85800)

    # Get the error handling from sep document
    json_file = Errors.json_input()
    itn = ITN(json_file)

    # find the closest node for closest algorithm
    node_near_user = itn.nearest_node(coord)
    node_near_high_point = itn.nearest_node(highest)
    print(node_near_user, node_near_high_point)

>>>>>>> 0f6b9fc8aa8ae5be5d1b67811ea0e2fa1d0598ee

if __name__ == "__main__":
    task1()
    task2()
    task3()