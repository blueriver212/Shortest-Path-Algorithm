# Task 1: Bringing in the user coordinate from input.

# Adding a GUI.
# Needs to have an input x and y coordinate.#

import tkinter as tk
import tkinter.messagebox

window = tk.Tk()
window.title('Welcome to User Coordinate Input!')
window.geometry('450x300')

lb1 = tk.Label(window, text='Your location X coordinate:').place(x=10, y=15)
lb2 = tk.Label(window, text='Your location Y coordinate:').place(x=10, y=45)
lb3 = tk.Label(window, text='').place(x=10, y=100)
getx = tk.Entry()
getx.place(x=170, y=15)
gety = tk.Entry()
gety.place(x=170, y=45)


def user_input():
    x_coord = getx.get()
    y_coord = gety.get()
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
    window.destroy()
    return


def reset():
    getx.delete(0, 'end')
    gety.delete(0, 'end')
    return


def close():
    if tk.messagebox.askokcancel("Close", "Do you want to close the software?"):
        window.destroy()
        print("Closed by User")


bt1 = tk.Button(window, text='Insert your coordinate', command=user_input)
bt1.place(x=50, y=150)
bt2 = tk.Button(window, text='Reset your coordinate', command=reset)
bt2.place(x=200, y=150)
bt3 = tk.Button(window, text='Exit', command=close)
bt3.place(x=350, y=150)

window.mainloop()