from geoindex import GeoGridIndex, GeoPoint
import pickle

#TODO:  Would eventually be database/doc-repo driven

class QuietPlacesData:
    def __init__(self, datafile, debug):
        self.debug = debug
        fileObject = open(datafile, 'r')
        self.data = pickle.load(fileObject)
        # print 'loaded ' + str(len(self.data)) + 'records, initializing index'
        self.__load_geo_index()
        
    def __load_geo_index(self):
        self.geo_index = GeoGridIndex()
        for lodging in self.data:
            # if self.debug: print 'loading geo for:' + lodging["name"]
            lat = float(lodging["lat"])
            lng = float(lodging["lng"])
            self.geo_index.add_point(GeoPoint(lat, lng, ref=lodging))

    def geo_search(self, lat, lng, range):
        center_point = GeoPoint(lat, lng)
        lodgings = []

        for geo_point, distance in self.geo_index.get_nearest_points(center_point, range, 'km'):
            # if self.debug: print("We found {0} in {1} km".format(geo_point.ref["name"], distance))
            lodgings.append(geo_point.ref)
        return lodgings


# def getLodgingsForLatLong(lat, lng, range=1):
#     output = []
#
#     for lodging_result in qpd.geo_search(lat=lat, lng=lng, range=range):
#         #Target:
#         # {"hotels": [{"lat": 30.268162,"long": -97.7417,"score": 20,"name":
#         #    "Driskill Hotel","id": 1,"heatmap": []}, {"lat": 30.264444,"long":
#         #    -97.74184900000002,"score": 60,"name": "Hyatt Place Downtown","id":
#         #    2,"heatmap": []}, {"lat": 30.2655492,"long": -97.7466255,"score":
#         #    90,"name": "W Austin","id": 3,"heatmap": []}]}
#         lodging = {}
#         lodging["lat"] = lodging_result["lat"]
#         lodging["long"] = lodging_result["lng"]
#         lodging["score"] = lodging_result["score"]
#         lodging["name"] = lodging_result["name"]
#         lodging["fs_id"] = lodging_result["lat"]
#         lodging["places_id"] = lodging_result["google_id"]
#         lodging["google_reviews"] = lodging_result["google_reviews"]
#         if "reviews" in lodging_result: lodging["fs_reviews"] = lodging_result["reviews"]
#
#         heatmap = lodging_result["nearby_noisemakers"]
#         lodging["heatmap"] = heatmap
#         output.append(lodging)
#
#     return output


# qpd = QuietPlacesData('data_file.pkl', True)
# print getLodgingsForLatLong(lat=30.268162, lng=-97.7417, range=1)
