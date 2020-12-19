from nearest_ITN import *
from error_handling import *
from shapely.geometry import Point, Polygon
from highest_point import *
from GUI import *
import os


def main():
    # creating window using the UserInput class
    root = UserInput()
    coord = root.user_input()
    root.window.mainloop()


    pt = Point(450000, 92000)
    root = os.path.dirname(os.getcwd())
    island_file = 'isle_of_wight.shp'
    elevation_file = 'SZ.asc'
    island_path = os.path.join(root, 'Material', 'shape', island_file)
    elevation_path = os.path.join(root, 'Material', 'elevation', elevation_file)

    out_loc = r'clip.tif'
    hp = HighestPoint(pt, island_path, elevation_path, out_loc)
    clipped_path = hp.clip_elevation()
    highest_point_in_area = hp.find_highest_point(clipped_path)

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


if __name__ == "__main__":
    main()