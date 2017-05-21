from foursquare import FourSquareApi

#Test location

if False:
    location = FourSquareApi("Austin, Texas").location
    print 'lat = ' + str(location.latitude) + ' and long = ' + str(location.longitude)

import re



from fuzzywuzzy import fuzz
from fuzzywuzzy import process






if  True:
    fsapi = FourSquareApi("119 Nueces St, Austin, TX 78701")
    for venue in fsapi.searchForVenues("Bar"):
        print venue
        


# Test Categories
# for category in FourSquareApi("Austin, Texas").categories:
#     print category["shortName"]
