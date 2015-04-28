__author__ = 'erhanhu'
from queries import *
from yelp_api import *
from bing import *
import re


# It converts a mysql query
# result to a python array.
def sql_result_to_arr(result):
    arr = []
    row = result.fetch_row()
    while len(row) > 0:
        arr.append(get_alnum_row(row[0]))
        row = result.fetch_row()
    return arr


def remove_non_alnum(text):
    return re.sub(r'[^.\w\-_]', ' ', text)


def get_alnum_row(tup):
    result = []
    for i in range(0, len(tup)):
        result.append(remove_non_alnum(str(tup[i])))
    return result


def gen_zipcode_result(zipcode, category):
    if category == 'all_cat':
        category = '%'
    result = sql_connect(sql_search_zipcode(zipcode, category))
    return sql_result_to_arr(result)


def gen_zipcodes_nearby(zipcode):
    center_result = sql_connect(sql_zip_center(zipcode))
    center = sql_result_to_arr(center_result)
    lati = float(center[0][0])
    longi = float(center[0][1])
    zipcodes_result = sql_connect(sql_nearby_zipcodes(lati, longi, float(0.1)))
    zipcodes = sql_result_to_arr(zipcodes_result)
    return zipcodes


# returns popular zipcodes for homepage suggestion:
def gen_popular_zipcodes():
    result = sql_connect(sql_popular_zipcodes())
    arr_raw = sql_result_to_arr(result)
    arr = []
    for item in arr_raw:
        if len(item[2]) == 5 and item[2].isdigit():
            arr.append(item)
    return arr


def gen_popular_zipcodes_for_state(state):
    result = sql_connect(sql_popular_zipcodes_for_state(state))
    arr_raw = sql_result_to_arr(result)
    arr = []
    for item in arr_raw:
        if len(item[1]) == 5 and item[2].isdigit():
            arr.append(item)
    return arr


def add_image_to_zipcode_result(arr):
    businesses = []
    for b in arr:
        businesses.append(b)
    return get_business_picture_parallel(businesses)


def add_bing_to_zipcode_result(arr):
    businesses = []
    for b in arr:
        if len(b) == 0:
            businesses.append(['','','',''])
        else:
            businesses.append(b)
    return get_bing_description_parallel(businesses)


def gen_id_info(id):
    result = sql_connect(sql_id_info(id))
    arr = sql_result_to_arr(result)
    return [] if len(arr) == 0 else arr[0]


def gen_tips(id):
    result = sql_connect(sql_tips(id))
    arr = sql_result_to_arr(result)
    return arr


# TEST AREA (test these before using in views.py)
# print(gen_popular_zipcodes())
if __name__ == '__main__':
    print(gen_id_info(''))