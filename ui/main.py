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

def getLodgingsForLatLong(lat, lng):
    createReponseObjectForResults(qpd.geo_search(lat=lat, lng=lng))

def createReponseObjectForResults(results):
    return '{"hotels": [{"lat": 30.268162,"long": -97.7417,"score": 20,"name": "Driskill Hotel","id": 1,"heatmap": []}, {"lat": 30.264444,"long": -97.74184900000002,"score": 60,"name": "Hyatt Place Downtown","id": 2,"heatmap": []}, {"lat": 30.2655492,"long": -97.7466255,"score": 90,"name": "W Austin","id": 3,"heatmap": []}]}';

if __name__ == '__main__':
    port = int(os.getenv('PORT', 9099))
    app.run(host='0.0.0.0', port=port)
    qpd = QuietPlacesData('data_file.pkl', True)


    # tone_analyzer = ToneAnalyzerV3(username='5637355c-a50a-496c-8305-b8820d5c4b63',
#     password='53cQKHtdm2lA', 
#     version='2016-05-19')
# tone = tone_analyzer.tone('this sentance is really funny or not!!!')
# print(tone)