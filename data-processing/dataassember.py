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

        #possibly_hotels = ['hotel', 'lodging', 'travel', 'residen']

        venues = self.fs_api.searchForVenues("Hotel")
        print 'retrieved:' + str(len(venues)) + ' venues'
        for venue in venues:

            is_possibly_hotel = False
            for category in venue["categories"]:
                if category["id"] == '4bf58dd8d48988d1fa931735':
                    is_possibly_hotel = True

            if is_possibly_hotel:
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
                result["fs_stats"] = venue["stats"]

                results.append(result)

        print 'of ' + str(len(venues)) + ' venues,' + str(len(results)) + ' were hotels!'
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

    def add_noise_word_count_to_dataset(self, lodgings):
        total = 0
        for lodging in lodgings:
            for review in lodging["google_reviews"]:
                total += sum(map(int, dict(self.find_target_words_exact(review)).values()))

            for review in lodging["fs_reviews"]:
                total += sum(map(int, dict(self.find_target_words_exact(review)).values()))
                
            lodging["total_noise_words"] = total
            
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
        output_list = []
        for word in self.wanted:
            # TODO: how to sum the counts if > 1
            # print [ (val,cnt) for val, cnt in output_list if cnt  == 1 ]
            if word in input_text:
                output_list.append((word, 1))

        return output_list
        # matches = re.findall('\w+',input_text.lower())
        # counts = collections.Counter(matches) # Count each occurance of words
        # if self.debug: print counts
        # return map(lambda x:(x,counts[x]),self.wanted) # Will print the counts for wanted words


#@Deprecated for now.  Not working out well.
    def findTargetWordsFuzzyMatch(self, input_text):
        noise_words = {}
        for noise_word in self.wanted:
            noise_words[noise_word] = fuzz.ratio(noise_word, input_text)
            # noise_words[noise_word] = process.extract(query, choices)(noise_word, input_text)
        return noise_words


# import operator
# test_val = [('sec', 1), ('foo', 1), ('bar', 1)]
#
# new_list = map(operator.itemgetter(1), test_val)
# print new_list

# target_words = PreWatsonNoiseAnalyzer(True).find_target_words_exact("noisy noisy noise count em bitches this shit is noise factor noisy and live music and crowded as fuck")
# print target_words
# total = sum(map(int, dict(target_words).values()))
# print total
# print map(lambda x:(target_words),x[1])

import pickle

if True: # Lets run api pull
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

    analyzer = PreWatsonNoiseAnalyzer(False)

    # Prune FS reviews
    analyzer.remove_unsuitable_fs_reviews(results_in)
    analyzer.remove_unsuitable_google_reviews(results_in)
    analyzer.add_noise_word_count_to_dataset(results_in)

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

