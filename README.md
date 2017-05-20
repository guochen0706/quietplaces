

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


# Data Opportunities
* Foursquare
* Yelp: https://www.yelp.com/developers/documentation/v2/overview
* Zillow
* ZooProperty: http://www.zooproperty.com/api/