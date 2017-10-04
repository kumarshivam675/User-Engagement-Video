import json
import os

import savetocsv
from code.config import project_folder

path = project_folder + "logdumps_organisationX/"


for file in os.listdir(path):
    print file
    count = 0
    if file != '.gitignore':
        with open(path + file) as json_data:
            d = json.load(json_data)

            for feature in d:
                count += 1
                timestamp = ""
                pid = ""
                client_message = ""
                offset = ""
                timestamp_2 = ""
                if feature['email_id'] == '9db9c3e9d33364b57be6ad1f5707c011e76a26bfe15e653cf8d8d189':
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

