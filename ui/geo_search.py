from geoindex import GeoGridIndex, GeoPoint
import pickle

#TODO:  Would eventually be database/doc-repo driven

class QuietPlacesData:
    def __init__(self, datafile, debug):
        self.debug = debug
        fileObject = open(datafile, 'r')
        self.data = pickle.load(fileObject)
        print 'loaded ' + str(len(self.data)) + 'records, initializing index'
        self.__load_geo_index()
        
    def __load_geo_index(self):
        self.geo_index = GeoGridIndex()
        for lodging in self.data:
            if self.debug: print 'loading geo for:' + lodging["name"]
            lat = float(lodging["lat"])
            lng = float(lodging["lng"])
            self.geo_index.add_point(GeoPoint(lat, lng, ref=lodging))

    def geo_search(self, lat, lng):
        center_point = GeoPoint(lat, lng)
        lodgings = []

        for geo_point, distance in self.geo_index.get_nearest_points(center_point, 1, 'km'):
            if self.debug: print("We found {0} in {1} km".format(geo_point.ref["name"], distance))
            #
            lodgings.append(geo_point.ref)
        return lodgings
    
qpd = QuietPlacesData('data_file.pkl', True)
qpd.geo_search(lat=30.265873, lng=-97.746445)
