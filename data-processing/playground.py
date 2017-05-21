import re
import collections

wanted = ['street noise', 'loud music', 'too loud', 'thin walls', 'busy street', 'noise level', 'noise factor', 'loud', 'noisy', 'road noise', 'nearby highway', 'busy highway']

if False:
    def findTargetWordsExact(input_text):
        matches = re.findall('\w+',input_text.lower())
        counts = collections.Counter(matches) # Count each occurance of words
        print counts
        return map(lambda x:(x,counts[x]),wanted) # Will print the counts for wanted words

    founds = findTargetWordsExact("NOT a good experience. Loud as hell. Room is very outdated and I'm pretty sure they didn't clean after the last guest: breakfast menu was already filled out, pee on the toilet seat, and a pubic hair on the sheets!!")

    for found in founds:
        if found[1] > 0:
            print "GOT ONE!!" + str(found)
        else:
            print found
            

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

if False:

    combined_match_max_threshold = 75
    number_of_noise_words = len(wanted)
    def findTargetWordsFuzzyMatch(input_text):
        noise_words = {}
        for noise_word in wanted:                       
            noise_words[noise_word] = fuzz.token_sort_ratio(noise_word, input_text)
            # noise_words[noise_word] = process.extract(query, choices)(noise_word, input_text)
        return noise_words

# Many ways to skin this cat...up for review.
    def submitReviewForAnalysis(input_text):
        if process.extractOne(input_text, wanted)[1] >= 50:
            return True
        else:
            return False
        # founds = findTargetWordsFuzzyMatch(input_text)
        #
        # score = 0
        # for found in founds:
        #     print found + ':'+ str(founds[found])
        #     if founds[found] >= 75:     #Any exact match says submit for sentiment and classification
        #         return True
        #     score += founds[found]
        #
        # print score / number_of_noise_words
        # if score / number_of_noise_words > combined_match_max_threshold:
        #     return True
        # else:
        #     return False

   

    inputtxt1 = "NOT a good experience.  as hell. Majorly noisy! Room is very outdated and I'm pretty sure they didn't clean after the last guest: breakfast menu was already filled out, pee on the toilet seat, and a pubic hair on the sheets!!"
    assert submitReviewForAnalysis(inputtxt1) == True

    inputtxt2 = "NOT a good experience, but very quiet place. Room is very outdated and I'm pretty sure they didn't clean after the last guest: breakfast menu was already filled out, pee on the toilet seat, and a pubic hair on the sheets!!"
    assert submitReviewForAnalysis(inputtxt2) == False

# print process.extract(inputtxt1, wanted, limit=5)
# print process.extract(inputtxt2, wanted, limit=5)
# print process.extractOne(inputtxt1, wanted)
# print process.extractOne(inputtxt2, wanted) [1]