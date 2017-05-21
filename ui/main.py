import os
import json
import sys
from flask import Flask, jsonify, request,render_template
from watson_developer_cloud import ToneAnalyzerV3, VisualRecognitionV3, LanguageTranslatorV2
from flask_cors import CORS
from geo_search import QuietPlacesData

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
  return render_template('index.html')
	
@app.route('/version')
def version():
	return sys.version
	
@app.route('/getNoiseScores')
def getNoiseScores():
    return getLodgingsForLatLong(lat=30.268162,long=-97.7417)

def getLodgingsForLatLong(lat, lng, range=1):
    output = []
    for lodging_result in qpd.geo_search(lat=lat, lng=lng, range=range):
        lodging = {}
        lodging["lat"] = lodging_result["lat"]
        lodging["long"] = lodging_result["lng"]
        lodging["score"] = lodging_result["score"]
        lodging["name"] = lodging_result["name"]
        lodging["fs_id"] = lodging_result["lat"]
        lodging["places_id"] = lodging_result["google_id"]
        lodging["google_reviews"] = lodging_result["google_reviews"]
        if "reviews" in lodging_result: lodging["fs_reviews"] = lodging_result["reviews"]

        heatmap = lodging_result["nearby_noisemakers"]
        lodging["heatmap"] = heatmap
        output.append(lodging)
    return output

if __name__ == '__main__':
    port = int(os.getenv('PORT', 9099))
    app.run(host='0.0.0.0', port=port)
    qpd = QuietPlacesData('data_file.pkl', False)


    # tone_analyzer = ToneAnalyzerV3(username='5637355c-a50a-496c-8305-b8820d5c4b63',
#     password='53cQKHtdm2lA', 
#     version='2016-05-19')
# tone = tone_analyzer.tone('this sentance is really funny or not!!!')
# print(tone)