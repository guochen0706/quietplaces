import os
import sys
import json
from flask import Flask, jsonify, request
from watson_developer_cloud import ToneAnalyzerV3
from foursquare import FourSquareApi

app = Flask(__name__)
vcap = os.getenv('VCAP_SERVICES')
vcap = json.loads(vcap)

@app.route('/')
def home():
    return "Hello World"

@app.route('/version')
def version():
    return sys.version

@app.route('/tone/<text>')
def tone(text):
    password = vcap['tone_analyzer'][0]['credentials']['password']
    username = vcap['tone_analyzer'][0]['credentials']['username']
    tone_analyzer = ToneAnalyzerV3(username=username,
                                   password=password,
                                   version='2016-05-19')

    dictionary = tone_analyzer.tone(text)
    return jsonify(dictionary)

def __validate_location(location_text):
    return FourSquareApi(location_text).location

def __get_sentiment(location):
    return 'blah'


if __name__ == '__main__':
    port = int(os.getenv("PORT", 9099))
    app.run(host='0.0.0.0', port=port)




#Test
print 'Testing Location'
ta = ['tone_analyzer']
ta[0]['credentials']['username'] =  os.environ['WATSON_USERNAME']
ta[0]['credentials']['password'] =  os.environ['WATSON_PASSWORD']
vcap = ta
