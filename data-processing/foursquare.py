from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values
import requests # library to handle requests
from googleapis import Google

FS_BASE_URL = 'https://api.foursquare.com/v2/'
FS_CLIENT_ID = "P2504I5EFCH0FAYZSXTYEWGS3BHU5STVCBRF3JALWIOESOVD"
FS_CLIENT_SECRET = "2YOTPR1XQ4N4MKOOHGRC3J44T5BUEOMSU515A5CQVMEPIYFE"
FS_VERSION = "20170511"
FS_CAT_HOTEL = '4bf58dd8d48988d1fa931735' #Disconnected keyword search query and presently hardcoing to Hotel category due to keyword innaccuracy. Then again...Foursquare "hotel cateogory"  is pretty inaccurate too. :(
LIMIT = 1
# RADIUS = 805 # Meters in 1/2 mile.
RADIUS = 1610 # Meters in 1 mile.

debug = True

class FourSquareApi:


    def __init__(self, address):
        self.address = address
        self.location = self.__getLocation()
        self.categories = self.__categories()
        self.google = Google()

    def __categories(self):
        url = FS_BASE_URL + "/venues/categories?client_id={}&client_secret={}&v={}".format(FS_CLIENT_ID, FS_CLIENT_SECRET, FS_VERSION)
        # send call request and get categories
        results = requests.get(url).json()
        category_list = []

        for category in results["response"]["categories"]:
            category_list.append(category)
        return category_list

# This started failing so had to replace with google maps API
    def getLocation(self, address):
        # geolocator = Nominatim()
        # return geolocator.geocode(address)
        return Google().get_location_from_address(address)

    def __getLocation(self):
        # geolocator = Nominatim()
        self.location = Google().get_location_from_address(self.address)
        return self.location

# Foursquare returns gyms, coffee shops, and nightclubs for a Hotel search.  Good times...BROKEN!!!
    #e.g. https://api.foursquare.com/v2/venues/search?client_id=P2504I5EFCH0FAYZSXTYEWGS3BHU5STVCBRF3JALWIOESOVD&client_secret=2YOTPR1XQ4N4MKOOHGRC3J44T5BUEOMSU515A5CQVMEPIYFE&ll=30.2656016,-97.7497388&v=20170511&category=4bf58dd8d48988d1fa931735&query=Hotel&radius=805&limit=1000
    def searchForVenues(self, search_query):

#TODO: Test for foursquare pagination ability
        keywords = ['hotel', 'suite', 'inn', 'lodge']
        all_venues = []

        for keyword in keywords:
            # venue_url = FS_BASE_URL + "venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}".format(FS_CLIENT_ID, FS_CLIENT_SECRET, self.location.latitude, self.location.longitude, FS_VERSION, search_query, RADIUS, LIMIT)
            venue_url = FS_BASE_URL + "venues/search?client_id={}&client_secret={}&ll={},{}&v={}&category={}&query={}&radius={}&limit={}".format(FS_CLIENT_ID, FS_CLIENT_SECRET, self.location.latitude, self.location.longitude, FS_VERSION, FS_CAT_HOTEL, keyword, RADIUS, LIMIT)
            if debug: print 'hitting:' + venue_url
            results = requests.get(venue_url).json()
            all_venues.extend(results["response"]["venues"])

        output_venues = []
        
        #de-dupe
        for venue_all in all_venues:
            not_found = True
            for venue_unique in output_venues:
                if venue_all["id"] == venue_unique["id"]:
                    not_found = False

            if not_found: output_venues.append(venue_all)

        return output_venues

    def commentsForVenue(self, venue_id):
        tips_url = FS_BASE_URL + "venues/{}/tips?client_id={}&client_secret={}&v={}&limit={}".format(venue_id, FS_CLIENT_ID, FS_CLIENT_SECRET, FS_VERSION, LIMIT)
        results = requests.get(tips_url).json()
        return results["response"]["tips"]["items"]

# This doesn't work:u'A user is required to call this endpoint.'
    def checkinsForVenue(self, venue_id):
        checkins_url = FS_BASE_URL + "venues/{}/stats?client_id={}&client_secret={}&v={}".format(venue_id, FS_CLIENT_ID, FS_CLIENT_SECRET, FS_VERSION)
        if debug: print checkins_url
        results = requests.get(checkins_url).json()
        return results["response"]
