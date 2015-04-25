import urllib2
import json
import threading
from api_info import *


# Bing Search function. Comes from
# http://stackoverflow.com/questions/27606478/search-bing-via-azure-api-using-python
# Needs to apply for a Bing Account Key from Microsoft
#  and make it available in cis550project/yelp/api_info.py by
#  BING_KEY = '<your key>'
# INPUT:
#   1st arg = the key word(s) as a string.
#   2nd arg = 'Image' for image search.
# OUTPUT:
#   Json object. e.g. we can print the 'Description' field of the first result by
#   results = bing_search(...)
#   print results[0]['Description']
def bing_search(search_string, search_type='Web', top=3, offset=0):
    credential_bing = 'Basic ' + (':%s' % BING_KEY).encode('base64')[:]
    url = 'https://api.datamarket.azure.com/Bing/Search/' + search_type + \
          '?Query=%s&$top=%d&$skip=%d&$format=json' % ('%27'+search_string+'%27', top, offset)
    request = urllib2.Request(url)
    request.add_header('Authorization', credential_bing)
    request_opener = urllib2.build_opener()
    response = request_opener.open(request)
    json_results = json.load(response)
    return json_results['d']['results']


# transforms [b_name, stars, city, state, imgurl]
# into '<b_name>+<city>+<state>' then remove any
# space
def make_search_string(business):
    return ''.join((business[0] + '+' + business[2] + '+' + business[3]).split())


# INPUT
#   'business' is [name, stars, city, state, imgurl]
# OUTPUT: appending [name, stars, city, state, imgurl, description]
#   (a storage 2D array for get_bing_description_parallel()) to result
def get_bing_description(business, result):
    response = bing_search(make_search_string(business))
    current_result = business
    current_result.append('')
    if response is not None:
        description = response[0]['Description']
        if description is not None:
            current_result[-1] = description
            result.append(current_result)
            return


# INPUT: businesses (2D array)
# [[b1_name, b1_location, b1_stars], [b2_name, b2_location, b2_stars], ...]
# where bn_location is in format of 'City, State'.
def get_bing_description_parallel(businesses):
    result = []
    threads = [threading.Thread(target=get_bing_description, args=(b, result)) for b in businesses]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result


# TESTING AREA
if __name__ == '__main__':
    pass