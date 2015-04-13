__author__ = 'erhanhu'
from queries import *
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
    return re.sub(r'[^a-zA-Z0-9.-]', ' ', text)


def get_alnum_row(tup):
    result = []
    for i in range(0, len(tup)):
        result.append(remove_non_alnum(str(tup[i])))
    return result


def gen_zipcode_result(zipcode):
    result = sql_connect(sql_search_zipcode(zipcode))
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


# TEST AREA (test these before using in views.py)
#print(gen_popular_zipcodes())
gen_zipcodes_nearby('89109')