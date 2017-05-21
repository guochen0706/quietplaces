import os
import json
import sys
from flask import Flask, jsonify, request,render_template
from watson_developer_cloud import ToneAnalyzerV3, VisualRecognitionV3, LanguageTranslatorV2
from flask_cors import CORS
from geo_search import QuietPlacesData

# app = Flask(__name__)

app = Flask("quietplaces") # Needs defining at file global scope for thread-local sharing

import random

random.seed(2342)

CORS(app)

@app.route('/')
def home():
  return render_template('index.html')
	
@app.route('/version')
def version():
	return sys.version
	
@app.route('/getNoiseScores')
def getNoiseScores():
    all_args = request.args.to_dict()
    print all_args
    # tmp = getLodgingsForLatLong(lat=float(all_args["lat"]),lng=float(all_args["lng"]), range=float(all_args["range"]))
    # from IPython import embed
    # embed()
    # return "nope"                        getLodgingsForLatLong(lat=30.268162,lng=-97.7417, range=1)
    lat = 30.268162 if "lat" not in all_args else float(all_args["lat"])
    lng = -97.7417 if "lng" not in all_args else float(all_args["lng"])
    range = 1 if "range" not in all_args else float(all_args["range"])
    return json.dumps(getLodgingsForLatLong(lat=lat,lng=lng, range=range))

def getLodgingsForLatLong(lat, lng, range=1):
    output = []
    for lodging_result in app.qpd.geo_search(lat=lat, lng=lng, range=range):
        lodging = {}
        lodging["lat"] = lodging_result["lat"]
        lodging["long"] = lodging_result["lng"]
        lodging["score"] = lodging_result["score"] #float(lodging_result["score"]) * random.random() # TODO: Get scored data back out of dataframe and into file here
        lodging["name"] = lodging_result["name"]
        lodging["fs_id"] = lodging_result["lat"]
        lodging["places_id"] = lodging_result["google_id"]
        lodging["google_reviews"] = lodging_result["google_reviews"]
        if "reviews" in lodging_result: lodging["fs_reviews"] = lodging_result["reviews"]

        heatmap = lodging_result["nearby_noisemakers"]
        lodging["heatmap"] = heatmap
        output.append(lodging)
    return output

def setup_app(app):
    app.qpd = QuietPlacesData('data_file.pkl', True)


setup_app(app)
if __name__ == '__main__':
    port = int(os.getenv('PORT', 9099))
    app.run(host='0.0.0.0', port=port)
    

    # tone_analyzer = ToneAnalyzerV3(username='5637355c-a50a-496c-8305-b8820d5c4b63',
#     password='53cQKHtdm2lA', 
#     version='2016-05-19')
# tone = tone_analyzer.tone('this sentance is really funny or not!!!')
# print(tone)