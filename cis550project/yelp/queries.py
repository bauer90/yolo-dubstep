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


# Returns the top 15 most popular
# zipcodes, trying to include every
# state.
def sql_popular_zipcodes():
    return """select distinct b.city, b.state, b.zipcode, count(b.id) from BUSINESS b
              group by b.state
              order by count(b.id) desc
              limit 15"""


def sql_popular_zipcodes_for_state(state):
    select = 'select distinct b.city, b.zipcode, count(b.id) from BUSINESS b '
    where = 'where b.state = "' + state + '" '
    group_order = 'group by b.city order by count(b.id) desc limit 10 '
    return select + where + group_order


# Returns the top 20 businesses that
# have the given zipcode, order by their
# ratings.
def sql_search_zipcode(zipcode, category):
    select = 'select distinct b.name, b.stars, b.city, b.state, b.id ' + \
             'from BUSINESS as b left join CATEGORIES as c on b.id = c.business_id '
    where = 'where b.zipcode = "' + zipcode + '" ' + 'and ' + 'c.category like ' + '"%' + category + '%" '
    order = 'order by b.stars desc limit 20 '
    return select + where + order


# Returns the 'geographical center'
# of all business with the given zipcode.
#  computed by latitude/longitude.
def sql_zip_center(zipcode):
    return """select avg(b.latitude), avg(b.longitude) from BUSINESS as b
              where b.zipcode = '""" + str(zipcode) + "'"


def sql_id_info(business_id):
    select = 'select b.name, b.latitude, b.longitude from BUSINESS as b '
    where = 'where b.id = "' + business_id + '" '
    return select + where


def sql_tips(business_id):
    select = 'select t.tip from TIPS as t '
    where = 'where t.business_id = "' + business_id + '" limit 5 '
    return select + where


# Returns the set of all zipcodes that are
# 'close enough' to the given [lati,longi]
# combination.
def sql_nearby_zipcodes(lati, longi, offset):
    return """select distinct(b.zipcode), b.city, b.state from BUSINESS as b
           where b.latitude > """ + str(lati-offset) + """ and b.latitude < """ + str(lati+offset) + """
           and b.longitude > """ + str(longi-offset) + """ and b.longitude  < """ + str(longi+offset) + """ limit 15"""


# Returns a set of categories that appear
# in at least one of the businesses who have
# the given zipcode.
def sql_local_categories(zipcode):
    return """select distinct(z.category) from ZIPCAT as z
           where z.zipcode = '""" + str(zipcode) + "'"


# Returns a set of business ids who have the
# given zipcode and category.
def sql_search_nearby(zipcode, category):
    return """select distinct(b.id) from BUSINESS as b inner join CATEGORIES as c
              on b.id = c.business_id
              where b.zipcode = '""" + str(zipcode) + """' and c.category like '%""" + category + "%'"


# TESTING AREA
if __name__ == '__main__':
    print(sql_id_info('Nfefwefwef'))
    print(sql_tips('fjwoefiwoehif'))