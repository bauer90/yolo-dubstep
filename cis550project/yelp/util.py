__author__ = 'erhanhu'
import _mysql


# The wrapper function for all SQL queries.
# Usage: result = sql_connect(some_query_string)
# then each result.fetch_row() retrieves a row.
def sql_connect(q):
    conn = _mysql.connect('mysql.cb0rrjncuorj.us-west-2.rds.amazonaws.com',
                          'erhan',
                          '550300321',
                          'mydb')
    conn.query(q)
    result = conn.use_result()
    return result


# Returns the top 25 businesses that
# have the given zipcode.
def sql_search_zipcode(zipcode):
    return """select b.name, b.state
                  from BUSINESS as b
                  where b.zipcode = '""" + str(zipcode) + "' limit 25"


# Returns the 'geographical center'
# of all business with the given zipcode.
#  computed by latitude/longitude.
def sql_zip_center(zipcode):
    return """select avg(b.latitude), avg(b.longitude) from BUSINESS as b
              where b.zipcode = '""" + str(zipcode) + "'"


# Returns the set of all zipcodes that are
# 'close enough' to the given [lati,longi]
# combination.
def sql_nearby_zipcodes(lati, longi, offset):
    return """select distinct(b.zipcode) from BUSINESS as b
           where b.latitude > """ + str(lati-offset) + """ and b.latitude < """ + str(lati+offset) + """
           and b.longitude > """ + str(longi-offset) + """ and b.longitude  < """ + str(longi+offset) + """ limit 15"""


# Returns a set of categories that appear
# in at least one of the businesses who have
# the given zipcode.
def sql_local_categories(zipcode):
    return """select distinct(z.category) from ZIPCAT as z
           where z.zipcode = '""" + str(zipcode) + "'"


# Returns a set of business id who have the
# given zipcode and category.
def sql_search_nearby(zipcode, category):
    return """select distinct(b.id) from BUSINESS as b inner join CATEGORIES as c
              on b.id = c.business_id
              where b.zipcode = '""" + str(zipcode) + """' and c.category like '%""" + category + "%'"


# TESTING AREA
# result = sql_connect(sql_zipcode_location('89109'))
# print(result.fetch_row()[0])
