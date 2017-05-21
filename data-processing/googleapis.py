import requests # library to handle requests
from googleplaces import GooglePlaces, types, lang

debug = True

GOOG_API_KEY = 'AIzaSyCtxmGWselcxywxamMztTrd8WS4XVruLrU'
NOISE_RADIUS_METERS = 91.44 # 100 yards

class Location:
    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long

class Google:

    def __init__(self):
        self.api_key = GOOG_API_KEY
        self.google_places = GooglePlaces(GOOG_API_KEY)

    def get_location_from_address(self, address):
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, self.api_key)
        if debug: print 'hitting:' + url
        results = requests.get(url).json()

        #Forcing to 1. Not sure what > 1 actually means for an explicit address.
        if len(results["results"]) > 0:
            location_dict = results["results"][0]["geometry"]["location"]
            return Location(location_dict["lat"], location_dict["lng"])
        else:
            return Location(0, 0)

    def get_ratings_and_reviews_for_location(self, location, name):
        query_result = self.google_places.nearby_search(lat_lng={ "lat": location.latitude, "lng": location.longitude },
                                                        name=name)

        if len(query_result.places) == 0:
            print 'Location:' + name + ' not found in google'
            return {}

        if len(query_result.places) > 1: print 'Location:' + name + ' found ' + str(len(query_result.places)) + ' times in google. Selecting first.'
        place = query_result.places[0]
        location_detail = {}
                        # TODO: Redo this as a data class, dictionary is annoying.
        # Returned places from a query are place summaries.
        location_detail["google_id"] = place.place_id
        location_detail["name"] = place.name

        # The following method has to make a further API call.
        place.get_details()
        location_detail["google_rating"] = str(place.rating)
        if "opening_hours" in place.details: location_detail["google_hours"] = place.details["opening_hours"]
        if "reviews" in place.details: location_detail["reviews"] = place.details["reviews"]

        return location_detail

    def get_ratings_for_nearby_noisemakers(self, location):

        # You may prefer to use the text_search API, instead.
        query_result = self.google_places.nearby_search(
            lat_lng={ "lat": location.latitude, "lng": location.longitude },
            radius=NOISE_RADIUS_METERS, types=[types.TYPE_AMUSEMENT_PARK,
                                               types.TYPE_AIRPORT,
                                               types.TYPE_FOOD,
                                               types.TYPE_GAS_STATION,
                                               types.TYPE_HOSPITAL,
                                               types.TYPE_MOVIE_THEATER,
                                               types.TYPE_NIGHT_CLUB,
                                               types.TYPE_SHOPPING_MALL,
                                               types.TYPE_STADIUM])
        # If types param contains only 1 item the request to Google Places API
        # will be send as type param to fullfil:
        # http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html

        nearby_noisemakers = self.__get_noisemaker_results(query_result)

        # Are there any additional pages of results?
        while query_result.has_next_page_token:
            query_result_next_page = self.google_places.nearby_search(
                pagetoken=query_result.next_page_token)
            nearby_noisemakers.append(self.__get_noisemaker_results(query_result_next_page))

        return nearby_noisemakers

    def __get_noisemaker_results(self, noisemaker_list):
        noisemakers = []
        for place in noisemaker_list.places:
            noisemakers.append(self.__get_noisemaker_result(place))
            
        return noisemakers


    def __get_noisemaker_result(self, place):

        noisemaker = {}

        # Returned places from a query are place summaries.
        noisemaker["name"] = place.name
        place.get_details()
        noisemaker["rating"] = str(place.rating)

        return noisemaker
        # The following method has to make a further API call.
        #place.get_details()
        # Referencing any of the attributes below, prior to making a call to
        # get_details() will raise a googleplaces.GooglePlacesAttributeError.
        #print place.details # A dict matching the JSON response from Google.


    # Adding and deleting a place
    # try:
    #     added_place = google_places.add_place(name='Mom and Pop local store',
    #                                           lat_lng={'lat': 51.501984, 'lng': -0.141792},
    #                                           accuracy=100,
    #                                           types=types.TYPE_HOME_GOODS_STORE,
    #                                           language=lang.ENGLISH_GREAT_BRITAIN)
    #     print added_place.place_id # The Google Places identifier - Important!
    #     print added_place.id
    #
    #     # Delete the place that you've just added.
    #     google_places.delete_place(added_place.place_id)
    # except GooglePlacesError as error_detail:
    #     # You've passed in parameter values that the Places API doesn't like..
    #     print error_detail


# google = Google()
# print google.get_ratings_and_reviews_for_location(Location(30.2682606, -97.74170910000001), name='Driskill Hotel Ballroom')
# print google.get_ratings_for_nearby_noisemakers(Location(30.2682606, -97.74170910000001))