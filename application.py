from config import Config
import csv
import os
import logging

from app.cucm import helper as cucm_helper

csv_columns = ['device_name', 'device_description', 'line_pattern', 'line_partition', 'potential_user', 'potential_userid']
csv_file = 'OUTPUT/results.csv'

if os.environ['LOG_LEVEL']:
    logging.basicConfig(level=int(os.environ['LOG_LEVEL']))

logging.info('Retrieving unassigned devices')
unassigned = cucm_helper.get_unassigned_devices()

results = []

for device in unassigned:
    logging.info('Processing:')
    logging.info('Name: {}; Description: {}'.format(device[0].text, device[1].text))

    current_result = {
        'device_name': device[0].text,
        'device_description': device[1].text
    }

    lines = cucm_helper.get_phone_lines(device[0].text)
    line = lines[0]

    dn = line['dirn']['pattern']

    # Check if DN has an esscaped character (\\)
    if '\\' in dn:
        logging.debug('DN contains escaped character, removing prefix')
        dn = dn.replace('\\', '')
        logging.debug('Updated DN: {}'.format(dn))

    logging.info('Looking for user with DN: {}'.format(dn))

    current_dn = {
        'line_pattern': dn,
        'line_partition': line['dirn']['routePartitionName']['_value_1']
    }

    potential_user = cucm_helper.find_user_by_telephone_number(dn)

    if potential_user:
        user = potential_user[0]
        logging.info('Found user: {} {}; Status: {}; UserID: {}; Telephone Number: {}'.format(user[0].text, user[1].text, user[2].text, user[3].text, user[4].text))
        
        current_result = {
            'device_name': device[0].text,
            'device_description': device[1].text,
            'line_pattern': dn,
            'line_partition': line['dirn']['routePartitionName']['_value_1'],
            'potential_user': '{} {}'.format(user[0].text, user[1].text),
            'potential_userid': user[3].text
        }

    else:
        logging.info('No end user with DN found')
        
        current_result = {
            'device_name': device[0].text,
            'device_description': device[1].text,
            'line_pattern': dn,
            'line_partition': line['dirn']['routePartitionName']['_value_1'],
            'potential_user': 'No Match',
            'potential_userid': 'No Match'
        }

    results.append(current_result)

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in results:
            writer.writerow(data)
except IOError:
    logging.error('I/O error')
