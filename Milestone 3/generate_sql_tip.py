__author__ = 'erhanhu'
import json

JSON_FILE_INPUT = 'tip.json'
SQL_SCRIPT_OUTPUT = 'tip.sql'
TABLE_NAME = 'TIPS'


# removes any quotes and special characters
# but retains spaces
def del_special_char(s):
    return ''.join(c for c in s if c.isalnum() or c == ' ')


# 'date' has format YYYY-MM-DD
def get_year(s):
    return s[:s.find('-')]

fi = open(JSON_FILE_INPUT, 'r')
fo = open(SQL_SCRIPT_OUTPUT, 'w')
line = fi.readline()
while line:
    j = json.loads(line)
    # a 'tip' is considered only if it got one or more likes,
    # or it's written in 2014 or later. Also tips >= 100
    # characters are dropped.
    if len(j.get('text')) < 100 and (j.get('likes') > 0 or int(get_year(j.get('date'))) >= 2014):
        b_id = j.get('business_id')
        tip = del_special_char(j.get('text'))
        likes = j.get('likes')
        stmt = "INSERT INTO " + TABLE_NAME
        stmt += " (business_id, tip, likes) VALUES "
        stmt += ("('{0}', '{1}', {2});\n").format(b_id, tip, likes)
        fo.write(stmt)
    line = fi.readline()
