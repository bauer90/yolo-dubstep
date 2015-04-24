# COMES FROM YELP API SAMPLE CODE FOR PYTHON.

import json
import urllib
import urllib2
import oauth2
import threading
from api_info import *

API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
SEARCH_LIMIT = 1


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()
    return response


def search(term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location)
    businesses = response.get('businesses')
    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, location)
        return

    business_id = businesses[0]['id']
    response = get_business(business_id)
    return response


# INPUT
# business: [name, location, stars] where location is 'City, State'
#
# OUTPUT
# append an array [name, location, stars, imgurl] to 'result'
# (a storage 2D array for get_business_picture_parallel())
def get_business_picture(business, result):
    response = query_api(business[0], business[1])
    if response is not None:
        url = response.get('image_url')
        if url is not None:
            url_big_img = url[:url.rfind('/')] + '/348s.jpg'
            current_result = business
            current_result.append(url_big_img)
            result.append(current_result)
            return
    else:
        result.append('')


# INPUT: businesses (2D array)
# [[b1_name, b1_location, b1_stars], [b2_name, b2_location, b2_stars], ...]
# where bn_location is in format of 'City, State'.
#
# OUTPUT: [[b1_name, b1_location, b1_stars, b1_imgurl],
#          [b2_name, b2_location, b2_stars, b2_imgurl],
#          ... ]
def get_business_picture_parallel(businesses):
    result = []
    threads = [threading.Thread(target=get_business_picture, args=(b, result)) for b in businesses]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result


def ttt(t):
    t.append(5)

# TEST AREA
if __name__ == '__main__':
    pass