from input_from_user import *
from error_handling import *
from nearest_ITN import *
from shapely.geometry import Point

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
    node_near_highest_point = itn.nearest_node(highest)
    print(node_near_user, node_near_highest_point)




if __name__ == "__main__":
    task1()
    task2()
    task3()
