import json
import simplejson
from timeit import repeat

NUMBER = 100000
REPEAT = 10

def compare_json_and_simplejson(data):
    """Compare json and simplejson - dumps and loads"""
    compare_json_and_simplejson.data = data
    compare_json_and_simplejson.dump = json.dumps(data)
    assert json.dumps(data) == simplejson.dumps(data)
    result = min(repeat("json.dumps(compare_json_and_simplejson.data)", "from __main__ import json, compare_json_and_simplejson", 
                 repeat = REPEAT, number = NUMBER))
    print "      json dumps {} seconds".format(result)
    result = min(repeat("simplejson.dumps(compare_json_and_simplejson.data)", "from __main__ import simplejson, compare_json_and_simplejson", 
                 repeat = REPEAT, number = NUMBER))
    print "simplejson dumps {} seconds".format(result)
    assert json.loads(compare_json_and_simplejson.dump) == data
    result = min(repeat("json.loads(compare_json_and_simplejson.dump)", "from __main__ import json, compare_json_and_simplejson", 
                 repeat = REPEAT, number = NUMBER))
    print "      json loads {} seconds".format(result)
    result = min(repeat("simplejson.loads(compare_json_and_simplejson.dump)", "from __main__ import simplejson, compare_json_and_simplejson", 
                 repeat = REPEAT, number = NUMBER))
    print "simplejson loads {} seconds".format(result)


print "Complex real world data:" 
COMPLEX_DATA = {'status': 1, 'timestamp': 1362323499.23, 'site_code': 'testing123', 'remote_address': '212.179.220.18', 'input_text': u'ny monday for less than \u20aa123', 'locale_value': 'UK', 'eva_version': 'v1.0.3286', 'message': 'Successful Parse', 'muuid1': '11e2-8414-a5e9e0fd-95a6-12313913cc26', 'api_reply': {"api_reply": {"Money": {"Currency": "ILS", "Amount": "123", "Restriction": "Less"}, "ProcessedText": "ny monday for less than \\u20aa123", "Locations": [{"Index": 0, "Derived From": "Default", "Home": "Default", "Departure": {"Date": "2013-03-04"}, "Next": 10}, {"Arrival": {"Date": "2013-03-04", "Calculated": True}, "Index": 10, "All Airports Code": "NYC", "Airports": "EWR,JFK,LGA,PHL", "Name": "New York City, New York, United States (GID=5128581)", "Latitude": 40.71427, "Country": "US", "Type": "City", "Geoid": 5128581, "Longitude": -74.00597}]}}}
compare_json_and_simplejson(COMPLEX_DATA)
print "\nSimple data:"
SIMPLE_DATA = [1, 2, 3, "asasd", {'a':'b'}]
compare_json_and_simplejson(SIMPLE_DATA)
