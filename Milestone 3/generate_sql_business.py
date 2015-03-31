__author__ = 'erhanhu'
import json

JSON_FILE_INPUT = 'business.json'
SQL_SCRIPT_OUTPUT = 'business.sql'
TABLE_NAME = 'BUSINESS'


# useful when getting street address
# from full_address
def del_last_line(s):
    return s[:s.rfind('\n')]


# zipcode appears as the last segment
# of full_address
def get_zip(s):
    return s[s.rfind(' ')+1:]


# removes any quotes and special characters
# but retains spaces and newlines
def del_special_char(s):
    return ''.join(c for c in s if c.isalnum() or c == ' ' or c == '\n')


fi = open(JSON_FILE_INPUT, 'r')
fo = open(SQL_SCRIPT_OUTPUT, 'w')
line = fi.readline()
while line:
    j = json.loads(line)
    if j.get('open'):
        b_id = j.get('business_id')
        name = del_special_char(j.get('name'))
        full_addr = del_special_char(j.get('full_address'))
        street_addr = del_special_char(del_last_line(full_addr)).replace('\n', ' ')  # makes address into a single line
        city = del_special_char(j.get('city'))
        state = del_special_char(j.get('state'))
        zipcode = get_zip(full_addr)
        lat = j.get('latitude')
        long = j.get('longitude')
        stars = j.get('stars')
        stmt = "INSERT INTO " + TABLE_NAME
        stmt += " (id, name, street_address, city, state, zipcode, latitude, longitude, stars) "
        stmt += "VALUES "
        stmt += ("('{0}','{1}','{2}','{3}','{4}','{5}',{6},{7}, {8});\n").format(b_id, name, street_addr, city, state, zipcode, lat, long, stars)
        fo.write(stmt)
    line = fi.readline()
