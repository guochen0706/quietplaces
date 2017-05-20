from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values
import requests # library to handle requests

FS_BASE_URL = 'https://api.foursquare.com/v2/'
FS_CLIENT_ID = "P2504I5EFCH0FAYZSXTYEWGS3BHU5STVCBRF3JALWIOESOVD"
FS_CLIENT_SECRET = "2YOTPR1XQ4N4MKOOHGRC3J44T5BUEOMSU515A5CQVMEPIYFE"
FS_VERSION = "20170511"
LIMIT = 100

# Data Containers
class Location:
    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long

class Venue:
    def __init__(self):
        self.name = ''
        self.categories = []
        self.twitter = ''
        self.location = ''
        self.menu_link = ''


class FourSquareApi:

    def __init__(self, address):
        self.address = address
        self.location = self.__getLocation()
        self.categories = self.__categories()

    def __categories(self):
        url = FS_BASE_URL + "/venues/categories?client_id={}&client_secret={}&v={}".format(FS_CLIENT_ID, FS_CLIENT_SECRET, FS_VERSION)
        # send call request and get categories
        results = requests.get(url).json()
        category_list = []

        for category in results["response"]["categories"]:
            category_list.append(category)
        return category_list

    def __getLocation(self):
        geolocator = Nominatim()
        self.location = geolocator.geocode(self.address)
        return self.location


    def searchForVenues(self, search_query):
        radius = 1000
        venue_url = FS_BASE_URL + "venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}".format(FS_CLIENT_ID, FS_CLIENT_SECRET, self.location.latitude, self.location.longitude, FS_VERSION, search_query, radius, LIMIT)
        print 'hitting:' + venue_url
        results = requests.get(venue_url).json()
        return results["response"]["venues"]

    def commentsForVenue(self, venue_id):
        tips_url = FS_BASE_URL + "venues/{}/tips?client_id={}&client_secret={}&v={}&limit={}".format(venue_id, FS_CLIENT_ID, FS_CLIENT_SECRET, FS_VERSION, LIMIT)
        results = requests.get(tips_url).json()
        return results["response"]["tips"]["items"]

