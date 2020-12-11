#Task 1: Bringing in the user coordinate from input.
def user():
    """
    This is the coordinate input for the user. There is error handling here to ensure the location is added in the
    correct format.
    :return: Coordinates from the user in a tuple.
    """
    while True:
        try:
            input_from_user = input("Enter your location (x,y) format:")
            coord = [float(input_from_user.split(',')[0]), float((input_from_user.split(',')[1]))]
            break
        except ValueError:
            print('Please check the format of your points!')
    return coord

def coord_input(coord):
    """
    This takes the user inputs and calculates if it is within the study area.
    :param coord: User Input (a tuple of coordinates)
    :return: Print statements if in or out of the study area. If out, it will quit the application.
    """
    xmin, ymin, xmax, ymax = 430000, 80000, 465000, 95000

    if xmin < coord[0] < xmax and ymin < coord[1] < ymax:
        print(f'Your coordinate {coord} is within the study area')
        return True
    else:
        print(f'Sorry! Your coordinate {coord} is not within the study area! \nWe have quit the application.')
        raise SystemExit



#sjnjiojoiknxasn