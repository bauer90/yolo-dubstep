__author__ = 'erhanhu'
import json

JSON_FILE_INPUT = 'business.json'
SQL_SCRIPT_OUTPUT = 'categories.sql'
TABLE_NAME = 'CATEGORIES'


def del_special_char(s):
    return (''.join(c for c in s if c.isalnum() or c == ' ')).replace('  ', ' ')


fi = open(JSON_FILE_INPUT, 'r')
fo = open(SQL_SCRIPT_OUTPUT, 'w')
line = fi.readline()
while line:
    j = json.loads(line)
    if j.get('open'):
        cat = j.get('categories')
        b_id = j.get('business_id')
        if len(cat) > 0:
            stmt = "INSERT INTO " + TABLE_NAME + " (business_id, category) values"
            stmt += ("('{0}','{1}');\n").format(b_id, del_special_char(' '.join(cat)))
            fo.write(stmt)
    line = fi.readline()
