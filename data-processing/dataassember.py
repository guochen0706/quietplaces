from foursquare import FourSquareApi
from googleapis import Location
from googleapis import Google
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class ApiConsumer:
    def __init__(self, address):
        self.google = Google()
        self.fs_api = FourSquareApi(address)
        # Data structure will be a list of dictionary
    # [
    #   { fs_id:'', name:'', score:100, address: '', lat: 1, lng: 1, fs_reviews_to_check: [ ], goog_reviews_to_check: [] }
    #
    #
    #  ]
    def load_foursquare_data(self):
        # Test Venues   - look for venues with comments/tips with target phrases
        results = []

        for venue in self.fs_api.searchForVenues("Hotel"):

            address = ' '.join(venue["location"]["formattedAddress"])
            #If it's not a possibly real damned address (many are not)
            if not address[0:1].isdigit():
                continue
            result = { "fs_id": venue["id"], "name": venue["name"], "address": address, "score": 100 }
            location = self.fs_api.getLocation(address)
            result["lat"] = str(location.latitude)
            result["lng"] = str(location.longitude)
            reviews = []
            for comment in self.fs_api.commentsForVenue(venue["id"]):
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

        # Add the rest
        lodging.update(google_data)

        if "reviews" in google_data:
            lodging["all_google_reviews"] = google_data["reviews"]
        else:
            lodging["all_google_reviews"] = []

    def load_google_noisemakers(self, lodging):
        # Then load data for the "surrounding noisemakers" and throw those in. While we were not able to
        # get ahold of "busy times" and all that good stuff maybe we can just include ratings & hours as part
        # of the noise equation

        # for noisemaker in self.google.get_ratings_for_nearby_noisemakers(Location(lodging.lat, lodging.lng)):
        # Not sure how to structure this yet but it's late so I'm going easy & nested - not so good for the calc process probably...sorry Chen...
        lodging["nearby_noisemakers"] = self.google.get_ratings_for_nearby_noisemakers(Location(lodging["lat"], lodging["lng"]))

import re
import collections

# This basically exists to work around limited request calls (1k/mo) to Watson. Need to preselect the reviews.
class PreWatsonNoiseAnalyzer:

    def __init__(self, debug):
        self.wanted = ['street noise', 'loud music', 'unbearable', 'lost sleep', 'no sleep', 'unable', 'live music', 'thin walls', 'busy street', 'crowded', 'noise level', 'noise factor', 'loud', 'noisy', 'road noise', 'traffic noise', 'nearby highway', 'busy highway']
        self.combined_match_max_threshold = 25
        self.debug = debug

    def remove_unsuitable_fs_reviews(self, lodgings):
        for lodging in lodgings:
            keeping_reviews = []
            for review in lodging["fs_reviews_to_check"]:
                if self.submit_review_for_analysis(review):

                    if self.debug: print 'keeping review:' + review
                    keeping_reviews.append(review)

            lodging["fs_reviews"] = keeping_reviews
            del lodging["fs_reviews_to_check"]
    
    def remove_unsuitable_google_reviews(self, lodgings):
        for lodging in lodgings:
            keeping_reviews = []
            # Add the reviews
            for review in lodging["all_google_reviews"]:
                if float(review["rating"]) < 4.1 and self.submit_review_for_analysis(review["text"]):
                    if self.debug: print 'keeping review:' + review
                    keeping_reviews.append(review["text"])

            lodging["google_reviews"] = keeping_reviews
            del lodging["all_google_reviews"]

    # Many ways to skin this cat...up for review. Fuzzy matching was very inconsistent - tried many fuzzywuzzy variations. Switching to exact match.
    def submit_review_for_analysis(self, input_text):
        founds = self.find_target_words_exact(input_text)
        for found in founds:
            if found[1] > 0:
                if self.debug: print "GOT ONE!!" + str(found)
                return True
            else:
                if self.debug: print found
                return False
        # if process.extractOne(input_text, self.wanted)[1] >= 80:
        #     return True
        # else:
        #     return False
        #     founds = self.findTargetWordsFuzzyMatch(input_text)
        #
        #     score = 0
        #     for found in founds:
                # print found + ':'+ str(founds[found])
                # if founds[found] >= 75:     #Any exact match says submit for sentiment and classification
                #     return True
                # score += founds[found]

            # print score / len(self.wanted)

            # if score / len(self.wanted) > self.combined_match_max_threshold:
            #     return True
            # else:
            #     return False

    def find_target_words_exact(self, input_text):
        matches = re.findall('\w+',input_text.lower())
        counts = collections.Counter(matches) # Count each occurance of words
        if self.debug: print counts
        return map(lambda x:(x,counts[x]),self.wanted) # Will print the counts for wanted words


#@Deprecated for now.  Not working out well.
    def findTargetWordsFuzzyMatch(self, input_text):
        noise_words = {}
        for noise_word in self.wanted:
            noise_words[noise_word] = fuzz.ratio(noise_word, input_text)
            # noise_words[noise_word] = process.extract(query, choices)(noise_word, input_text)
        return noise_words
    


import pickle

if False: # Lets run api pull
    # Load up the data from foursquare and google. This way we get "all the data" for our baseline POC only once time.
    api_clients = ApiConsumer("119 Nueces St, Austin, TX 78701")
    results = api_clients.load_foursquare_data()
    api_clients.augment_with_google_data(results)

    # TODO: Yelp would be nice here
    # TODO: Tripadviser would be nice here

    #Pickle that up

    outfile = open('data/aggregated_api_data_all_reviews.pkl', 'w')
    pickle.dump(results, outfile)
    outfile.close()



if True: # Lets run review filtering
#Inload the pickle and pre-filter reviews
    fileObject = open('data/aggregated_api_data_all_reviews.pkl', 'r')
    # load the object from the file into var b
    results_in = pickle.load(fileObject)

    analyzer = PreWatsonNoiseAnalyzer(True)

    # Prune FS reviews
    analyzer.remove_unsuitable_fs_reviews(results_in)
    analyzer.remove_unsuitable_google_reviews(results_in)

    outfile = open('data/aggregated_api_data_keyword_filtered_reviews.pkl', 'w')
    pickle.dump(results_in, outfile)
    outfile.close()

    #Print our end result for fun
    fileObject = open('data/aggregated_api_data_keyword_filtered_reviews.pkl', 'r')
    # load the object from the file into var b
    results_in = pickle.load(fileObject)

    # Reading data back (pickle test)
    print '====  Aggregated and review-filtered DATA ======'
    for datum in results_in:
        print datum

