# CHEN START HERE

OK you don't need to worry too much about my side of the work. I've done all the dataset assembling
and it's ready to both:

* Run the reviews that match a noise filter (which isn't well done at this point) through Watson, and update the model with that added feature
** This perhaps should at this point be the tone analyzer  - I don't know if you'll have time to train up a classifier
* Build a scoring mechanism.
 
 I think to keep from stepping on each other and wasting time and API calls, you should just pick up the my output file, decorate, and
 create your own updated output file (from Watson), decorate with noise score, then save again as the file the webservice will
 read into memory and cache for API calls
 
 I created you a stub/sample in watsonfeatures.py that loads the file my code outputs into a dataframe.
 
 We probably don't have time to implement geo search but the lat/lon is there if we decide to - not sure yet how to do that
 but maybe I can dig into that tomorrow while you are adding features.
 
 I have a limited set in the datafile presented here, but I'm letting a large set run overnight (this isn't a fast thing with all the API calls)

 Here's a sample record as it stands:
 
 ```$json
 {
 	'google_reviews_to_check': [],
 	'name': u 'Pure Austin Fitness',
 	'google_id': u 'ChIJO2DDHBK1RIYRdJxB2BxVCCg',
 	'google_hours': {
 		u 'weekday_text': [u 'Monday: 5:30 AM \u2013 10:00 PM', u 'Tuesday: 5:30 AM \u2013 10:00 PM', u 'Wednesday: 5:30 AM \u2013 10:00 PM', u 'Thursday: 5:30 AM \u2013 10:00 PM', u 'Friday: 5:30 AM \u2013 8:00 PM', u 'Saturday: 8:00 AM \u2013 7:00 PM', u 'Sunday: 9:00 AM \u2013 6:00 PM'],
 		u 'open_now': False,
 		u 'periods': [{
 			u 'close': {
 				u 'day': 0,
 				u 'time': u '1800'
 			},
 			u 'open': {
 				u 'day': 0,
 				u 'time': u '0900'
 			}
 		}, {
 			u 'close': {
 				u 'day': 1,
 				u 'time': u '2200'
 			},
 			u 'open': {
 				u 'day': 1,
 				u 'time': u '0530'
 			}
 		}, {
 			u 'close': {
 				u 'day': 2,
 				u 'time': u '2200'
 			},
 			u 'open': {
 				u 'day': 2,
 				u 'time': u '0530'
 			}
 		}, {
 			u 'close': {
 				u 'day': 3,
 				u 'time': u '2200'
 			},
 			u 'open': {
 				u 'day': 3,
 				u 'time': u '0530'
 			}
 		}, {
 			u 'close': {
 				u 'day': 4,
 				u 'time': u '2200'
 			},
 			u 'open': {
 				u 'day': 4,
 				u 'time': u '0530'
 			}
 		}, {
 			u 'close': {
 				u 'day': 5,
 				u 'time': u '2000'
 			},
 			u 'open': {
 				u 'day': 5,
 				u 'time': u '0530'
 			}
 		}, {
 			u 'close': {
 				u 'day': 6,
 				u 'time': u '1900'
 			},
 			u 'open': {
 				u 'day': 6,
 				u 'time': u '0800'
 			}
 		}]
 	},
 	'nearby_noisemakers': [{
 		'rating': 5,
 		'geo_location': {
 			u 'lat': Decimal('30.26651999999999'),
 			u 'lng': Decimal('-97.7429367')
 		},
 		'name': u 'Premiere Booth Austin'
 	}, {
 		'rating': 4,
 		'geo_location': {
 			u 'lat': Decimal('30.2676989'),
 			u 'lng': Decimal('-97.74266009999999')
 		},
 		'name': u "Brian's Brew Coffee"
 	}, {
 		'rating': Decimal('3.8'),
 		'geo_location': {
 			u 'lat': Decimal('30.26678979999999'),
 			u 'lng': Decimal('-97.7435823')
 		},
 		'name': u 'Speakeasy'
 	}, {
 		'rating': Decimal('4.2'),
 		'geo_location': {
 			u 'lat': Decimal('30.267655'),
 			u 'lng': Decimal('-97.742527')
 		},
 		'name': u "Jimmy John's"
 	}, {
 		'rating': Decimal('4.3'),
 		'geo_location': {
 			u 'lat': Decimal('30.267085'),
 			u 'lng': Decimal('-97.7434988')
 		},
 		'name': u "Shiner's Saloon"
 	}, {
 		'rating': '',
 		'geo_location': {
 			u 'lat': Decimal('30.2665372'),
 			u 'lng': Decimal('-97.74294160000001')
 		},
 		'name': u 'Food Safety Administration (Corporate HQ)'
 	}, {
 		'rating': 4,
 		'geo_location': {
 			u 'lat': Decimal('30.26675'),
 			u 'lng': Decimal('-97.74243869999999')
 		},
 		'name': u 'Kingdom'
 	}, {
 		'rating': Decimal('3.8'),
 		'geo_location': {
 			u 'lat': Decimal('30.2667648'),
 			u 'lng': Decimal('-97.7423206')
 		},
 		'name': u 'Karma Lounge Ltd'
 	}, {
 		'rating': '',
 		'geo_location': {
 			u 'lat': Decimal('30.267153'),
 			u 'lng': Decimal('-97.74306079999999')
 		},
 		'name': u 'Ozarka Bottled Water Delivery Austin'
 	}, {
 		'rating': Decimal('4.6'),
 		'geo_location': {
 			u 'lat': Decimal('30.26704939999999'),
 			u 'lng': Decimal('-97.74354699999999')
 		},
 		'name': u 'Ethics Music Lounge'
 	}, {
 		'rating': 5,
 		'geo_location': {
 			u 'lat': Decimal('30.26683449999999'),
 			u 'lng': Decimal('-97.7437439')
 		},
 		'name': u 'Terrace59'
 	}, {
 		'rating': Decimal('3.9'),
 		'geo_location': {
 			u 'lat': Decimal('30.2669573'),
 			u 'lng': Decimal('-97.743697')
 		},
 		'name': u 'Cielo Lounge'
 	}, {
 		'rating': '',
 		'geo_location': {
 			u 'lat': Decimal('30.2676989'),
 			u 'lng': Decimal('-97.74266009999999')
 		},
 		'name': u 'Capital Minerals LLC'
 	}, {
 		'rating': '',
 		'geo_location': {
 			u 'lat': Decimal('30.267153'),
 			u 'lng': Decimal('-97.7430607')
 		},
 		'name': u 'Avery Ranch'
 	}, {
 		'rating': '',
 		'geo_location': {
 			u 'lat': Decimal('30.267153'),
 			u 'lng': Decimal('-97.74306079999999')
 		},
 		'name': u 'La Fonda San Miguel'
 	}, {
 		'rating': '',
 		'geo_location': {
 			u 'lat': Decimal('30.267153'),
 			u 'lng': Decimal('-97.74306079999999')
 		},
 		'name': u 'Oliver Gardern'
 	}, {
 		'rating': 5,
 		'geo_location': {
 			u 'lat': Decimal('30.2675768'),
 			u 'lng': Decimal('-97.7429695')
 		},
 		'name': u 'Carousels Cupcakery'
 	}, {
 		'rating': '',
 		'geo_location': {
 			u 'lat': Decimal('30.2679365'),
 			u 'lng': Decimal('-97.7431945')
 		},
 		'name': u 'Acot Theater Hotline'
 	}, {
 		'rating': '',
 		'geo_location': {
 			u 'lat': Decimal('30.26793'),
 			u 'lng': Decimal('-97.7433248')
 		},
 		'name': u 'Revolution tattoo'
 	}, {
 		'rating': '',
 		'geo_location': {
 			u 'lat': Decimal('30.267153'),
 			u 'lng': Decimal('-97.74306079999999')
 		},
 		'name': u 'Hill Top Motel And Cafe'
 	}],
 	'score': 100,
 	'fs_id': u '566df7ac498eadbfb79e3088',
 	'address': u 'Austin, TX United States',
 	'lat': 30.267153,
 	'lng': -97.7430608,
 	'fs_reviews_to_check': [],
 	'google_rating': Decimal('4.1')
 }

```
## Files

datassembler.py.NoiseAnalyzerByLocation is the primary driver and uses classes from foursquare.py, googleapis.py
 to pull data from foursquare and google, and assemble it into a cohesive recordset by location. The search
 itself is just based on the address (Galvanize, presently) at the bottom of datassembler.py.
 
For this to be productized it would need to have this data aggregated for any supported city, and processed 
as a "prechew" effort into querable aggregate/analyzed data with a geo query.



# Python Stuff

pip install watson-developer-cloud --upgrade
pip install python-google-places
pip install python-Levenshtein
pip install fuzzywuzzy


For getting it to Bluemix we need some twiddly bits to inform the bluemix runtime.

# runtime.txt

e.g.

```
python-2.7.12
```

# requirements.txt
```$bash

pip freeze > requirements.txt


# Environment Vars in Code

e.g.
```$python
vcap = os.getenv('VCAP_SERVICES')
vcap = json.loads(vcap)
# IBM Env Vars
password = vcap['tone_analyzer'][0]['credentials']['password']
username = vcap['tone_analyzer'][0]['credentials']['username']

```

# Deployment with Cloud Foundry
REF: [https://github.com/chyld/python-cloud-foundry-watson]

Download cloudfoundry, e.g. on OSX - [https://docs.cloudfoundry.org/cf-cli/install-go-cli.html]
```bash
# Set Bluemix context
cf api https://api.ng.bluemix.net
cf login 

cf push --no-start
cf bs myapp "Tone Analyzer-qs"
cf env myapp
export VCAP_SERVICES='JSON'
```

## SSH In
[https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html]

```
cf ssh MY-AWESOME-APP -i 2
```


# Algorithm
This app as a POC searches within 1/2 mile of Galvanize Austin for Hotels that are, by review analysis,
notably quieter than others.  Ideally this service would also be useful as an API add-on for other lodging
solutions such as AirBNB or Homeaway.

1. Get list of hotels by radius from Foursquare
1. Cache reviews for each place                
1. Get lat/long for each place
1. Find Hotel in google places by lat/long
1. Get reviews for hotel
1. Get list of places from Google (200 yards) from hotel which are bars/restaurant+popularity/malls/music venue
1. Add them to scoring principal  

# Data Opportunities
* Foursquare
* Yelp: https://www.yelp.com/developers/documentation/v2/overview
* Zillow
* ZooProperty: http://www.zooproperty.com/api/


Wrapped https://github.com/slimkrazy/python-google-places for google places

# Notes
There's some inconsistencies in the API wrappers that make me uncomfortable but obviously this is very
"work in progress" and all that could be refactored.