from foursquare import FourSquareApi

#Test location

location = FourSquareApi("Austin, Texas").location
print 'lat = ' + str(location.latitude) + ' and long = ' + str(location.longitude)

one_venue_id = ''
# Test Venues
for venue in FourSquareApi("401 S Congress Ave Austin, Texas").searchForVenues("Hotel"):
    # print venue
    print venue
    print str(venue["id"]) + ',' + venue["name"]
    one_venue_id = venue["id"]


# Test Categories                                                                                           
for category in FourSquareApi("Austin, Texas").categories:
    print category["shortName"]
# client = foursquare.Foursquare(client_id=FS_CLIENT_ID, client_secret=FS_CLIENT_SECRET, version=FS_VERSION)
# print client.venues('40a55d80f964a52020f31ee3')

# Test Tips/Text
for comment in FourSquareApi("Austin, Texas").commentsForVenue(one_venue_id):
    print comment["text"]
