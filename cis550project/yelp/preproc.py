__author__ = 'erhanhu'
from queries import *


# It converts a mysql query
# result to a python array.
def sql_result_to_arr(result):
    arr = []
    row = result.fetch_row()
    while len(row) > 0:
        arr.append(row[0])
        row = result.fetch_row()
    return arr


# returns popular zipcodes for homepage suggestion:
def gen_popular_zipcodes():
    result = sql_connect(sql_popular_zipcodes())
    return sql_result_to_arr(result)


# TEST AREA (test these before using in views.py)
print(gen_popular_zipcodes())