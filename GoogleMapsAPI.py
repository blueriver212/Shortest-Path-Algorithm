import requests
from shapely.geometry import Point
import pyproj
from task6 import *
from shapely.geometry import Point


class GoogleMaps():
    def __init__(self, address):
        """
        This class will return a shapely point from a google maps search. You can search in any format
        that you like an example (has to be a string): 'Blackwater, Newport, PO30 3BJ'
        :param address: A string of a google maps search
        """
        self.__address = address

    def get_shapely_point(self):
        # This is a personal key, and will expire halfway through Feb 2021
        API_KEY = 'AIzaSyAbfly5_3lPTuaianFfWqrBFFP_NH6GsAU'

        params = {
            'key': API_KEY,
            'address': self.__address,
        }

        base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        response = requests.get(base_url, params=params)

        geometry = response.json()['results'][0]['geometry']
        lat = geometry['location']['lat']
        lng = geometry['location']['lng']

        # wgs_point = Point(lng, lat)

        #users_point = Point(transformer.transform(wgs84, bng, wgs_point.x, wgs_point.y))


        wgs84 = pyproj.Proj('+init=EPSG:4326')
        osgb36 = pyproj.Proj('+init=EPSG:27700')

        res = pyproj.transform(wgs84, osgb36, lng, lat)
        users_point = Point(res)

        return users_point


if __name__ == "__main__":
    address = 'Blackwater Mill, Blackwater, Newport, PO30 3BJ'
    pt_finder = GoogleMaps(address)
    addr_pt = pt_finder.get_shapely_point()

    island_path = "C:/Users/Windows10Pro/OneDrive - University College London/Desktop/CEGE0096/Material/shape/isle_of_wight.shp"
    inisl = InIsland(addr_pt, island_path)
    print(inisl.is_inside())