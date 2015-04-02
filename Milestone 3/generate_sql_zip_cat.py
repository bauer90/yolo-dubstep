__author__ = 'erhanhu'
import json

JSON_FILE_INPUT = 'business.json'
SQL_SCRIPT_OUTPUT = 'categories.sql'
TABLE_NAME = 'ZIPCAT'


def get_zip(s):
    return s[s.rfind(' ')+1:]


def del_special_char(s):
    return (''.join(c for c in s if c.isalnum() or c == ' ')).replace('  ', ' ')


fi = open(JSON_FILE_INPUT, 'r')
fo = open(SQL_SCRIPT_OUTPUT, 'w')
line = fi.readline()
arr = []
while line:
    j = json.loads(line)
    if j.get('open'):
        cats = j.get('categories')
        zip = get_zip(del_special_char(j.get('full_address')))
        print(len(cats))
        for cat in cats:
            arr.append((zip, cat))
            stmt = "INSERT INTO " + TABLE_NAME + " (zipcode, category) values"
            stmt += ("('{0}','{1}');\n").format(zip, del_special_char(cat))
            fo.write(stmt)
    line = fi.readline()
