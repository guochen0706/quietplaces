from foursquare import FourSquareApi
from googleapis import Location
from googleapis import Google
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class NoiseAnalyzerByLocation:

    def __init__(self):
        self.wanted = ['street noise', 'loud music', 'unbearable', 'lost sleep', 'no sleep', 'unable', 'live music', 'thin walls', 'busy street', 'noise level', 'noise factor', 'loud', 'noisy', 'road noise', 'nearby highway', 'busy highway']
        self.combined_match_max_threshold = 25
        self.google = Google()

    # Many ways to skin this cat...up for review.
    def submit_review_for_analysis(self, input_text):

        # if process.extractOne(input_text, self.wanted)[1] >= 80:
        #     return True
        # else:
        #     return False
            founds = self.findTargetWordsFuzzyMatch(input_text)

            score = 0
            for found in founds:
                # print found + ':'+ str(founds[found])
                if founds[found] >= 75:     #Any exact match says submit for sentiment and classification
                    return True
                score += founds[found]

            # print score / len(self.wanted)

            if score / len(self.wanted) > self.combined_match_max_threshold:
                return True
            else:
                return False

    def findTargetWordsFuzzyMatch(self, input_text):
        noise_words = {}
        for noise_word in self.wanted:
            noise_words[noise_word] = fuzz.ratio(noise_word, input_text)
            # noise_words[noise_word] = process.extract(query, choices)(noise_word, input_text)
        return noise_words
    
    # Data structure will be a list of dictionary
    # [
    #   { fs_id:'', name:'', score:100, address: '', lat: 1, lng: 1, fs_reviews_to_check: [ ], goog_reviews_to_check: [] }
    #
    #
    #  ]
    def load_foursquare_data(self, location):
        # Test Venues   - look for venues with comments/tips with target phrases
        results = []
        fs_api = FourSquareApi(location)
        for venue in fs_api.searchForVenues("Hotel"):

            address = ' '.join(venue["location"]["formattedAddress"])
            result = { "fs_id": venue["id"], "name": venue["name"], "address": address, "score": 100 }
            location = fs_api.getLocation(address)
            result["lat"] = str(location.latitude)
            result["lng"] = str(location.longitude)
            reviews = []
            for comment in fs_api.commentsForVenue(venue["id"]):
                if self.submit_review_for_analysis(comment["text"]):
                    reviews.append(comment["text"])

            result["fs_reviews_to_check"] = reviews
            results.append(result)
            
        return results
            # search = re.search( r'.*(noise).*|.*(busy).*', line, re.M|re.I)
            # if search:
            #     print venue["id"] + ',' + venue["name"] + '::' + line
            #     print search.group()
            #     print search.group(1)
            #     print search.group(2)
            # else:
            #     print 'Nada'

    def augment_with_google_data(self, lodgings):

        for lodging in lodgings:
            # First load data for the venue itself so we can snarf the reviews
            self.augment_lodging_with_google_data(lodging)

            # Next load the potential noisemakers
            self.load_google_noisemakers(lodging)
            

    def augment_lodging_with_google_data(self, lodging):
        google_data = self.google.get_ratings_and_reviews_for_location(Location(lodging["lat"], lodging["lng"]), name=lodging["name"])

        # remove the reviews so we can curate and add what we want
        google_reviews = google_data["reviews"]
        del google_data["reviews"]

        # Add the rest
        lodging.update(google_data)

        keeper_google_reviews = []
        # Add the reviews
        for review in google_reviews:
            if review["rating"] < 4.1 and self.submit_review_for_analysis(review["text"]):
                keeper_google_reviews.append(review)
        
        lodging["google_reviews_to_check"] = keeper_google_reviews

    def load_google_noisemakers(self, lodging):
        # Then load data for the "surrounding noisemakers" and throw those in. While we were not able to
        # get ahold of "busy times" and all that good stuff maybe we can just include ratings & hours as part
        # of the noise equation

        # for noisemaker in self.google.get_ratings_for_nearby_noisemakers(Location(lodging.lat, lodging.lng)):
            # Not sure how to structure this yet but it's late so I'm going easy & nested - not so good for the calc process probably...sorry Chen...
        lodging["nearby_noisemakers"] = self.google.get_ratings_for_nearby_noisemakers(Location(lodging["lat"], lodging["lng"]))


analyzer = NoiseAnalyzerByLocation()
results = analyzer.load_foursquare_data("119 Nueces St, Austin, TX 78701")
analyzer.augment_with_google_data(results)

import pickle

outfile = open('data/aggregated_api_data.json', 'w')
pickle.dump(results, outfile)
outfile.close()


fileObject = open('data/aggregated_api_data.json', 'r')
# load the object from the file into var b
results_in = pickle.load(fileObject)

# Reading data back


print '====  FS DATA ======'
for datum in results_in:
    print datum

