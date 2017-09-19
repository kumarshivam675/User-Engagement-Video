import json
import csv
import savetocsv
import os

path = '/home/shivam/coursework/user engagement/User-Engagement-Video/logdumps_organisationX/'


for file in ['logdump_400000.json']:
    print file
    count = 0
    with open(path + file) as json_data:
        d = json.load(json_data)

        for feature in d:
            count += 1
            timestamp = ""
            pid = ""
            client_message = ""
            offset = ""
            timestamp_2 = ""
            # if feature['email_id'] == 'fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef':
            if feature['timestamp']:
                timestamp = str(feature['timestamp'])
            if feature['pid']:
                pid = str(feature['pid'])
            if feature['message']:
                client_message = feature['client_msg'].encode('utf-8').strip()
            if feature['offset']:
                offset = str(feature['offset'])
            if feature['@timestamp']:
                timestamp_2 = str(feature['@timestamp'])

            savetocsv.save(file, timestamp, pid, client_message, offset, timestamp_2)

