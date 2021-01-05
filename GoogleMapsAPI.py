import requests
from shapely.geometry import Point
import pyproj


class GoogleMaps():
    def __init__(self, address):
        self.__address = address

    def get_shapely_point(self):
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

        bng = pyproj.Proj(init='epsg:27700')
        wgs84 = pyproj.Proj(init='epsg:4326')

        res = pyproj.transform(wgs84, bng, lng, lat)
        users_point = Point(res)

        return users_point

