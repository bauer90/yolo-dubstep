# COMES FROM YELP API SAMPLE CODE FOR PYTHON.

import json
import urllib
import urllib2
import oauth2

API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
SEARCH_LIMIT = 1

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'O56KIyVISk8jbjJccjlBIg'
CONSUMER_SECRET = 'LdiO-07Li43LCBM3XIpOIQeQrdA'
TOKEN = 'yRbjgstGKJpQhEAFS_mGHLnmhU34eOxh'
TOKEN_SECRET = 'NhylBe5QgLfN_TBnr3SBL1ljYgw'


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


def get_business_picture(business_name, location):
    result = query_api(business_name, location)
    if result is not None:
        url = result.get('image_url')
        if url is not None:
            url_big_img = url[:url.rfind('/')] + '/348s.jpg'
            print(url_big_img)
            return url_big_img
    return ""


# TEST AREA
# print(get_business_picture('eds', 'Philadelphia, PA'))