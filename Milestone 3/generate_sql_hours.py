__author__ = 'erhanhu'
import json

JSON_FILE_INPUT = 'business.json'
SQL_SCRIPT_OUTPUT = 'hours.sql'
TABLE_NAME = 'HOURS'
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

fi = open(JSON_FILE_INPUT, 'r')
fo = open(SQL_SCRIPT_OUTPUT, 'w')
line = fi.readline()
while line:
    j = json.loads(line)
    if j.get('open'):
        b_id = j.get('business_id')
        hours = j.get('hours')
        if hours:
            stmt = "INSERT INTO " + TABLE_NAME
            stmt += ' (business_id, ' + ', '.join(WEEKDAYS) + ") VALUES ('" + b_id + "', "
            for idx in range(0, len(WEEKDAYS)):
                hours_that_day = hours.get(WEEKDAYS[idx])
                if hours_that_day:
                    stmt += ("'{0}-{1}',").format(hours_that_day.get('open'), hours_that_day.get('close'))
                else:
                    stmt += 'null,'
            stmt = stmt[:-1]
            stmt += ');\n'
            fo.write(stmt)
    line = fi.readline()