import json
import re
import csv


path = '/home/shivam/coursework/user engagement/User-Engagement-Video/logdumps_organisationX/'


def load_json():
    with open(path + 'logdump_2000000.json') as json_data:
        d = json.load(json_data)

    return d


def extract_course_id(client_msg):
    # print client_msg
    if "Course : " in client_msg and ": video" in client_msg:
        return client_msg.split("Course : ")[1].split(" :")[0]

    return "null"


def extract_video_id(client_msg):
    # print client_msg
    if "Course : " in client_msg and ": video" in client_msg:
        if ": video id" in client_msg:
            return client_msg.split("video id : ")[1].split(" :")[0]
        elif ": video" in client_msg:
            return client_msg.split("video : ")[1].split(" :")[0]

    return "null"


def extract_kenlist_id(client_msg):
    print client_msg
    if "kenlistID :" in client_msg:
        return re.sub("[^0-9]", "", client_msg.split("kenlistID : ")[1].split(" :")[0])

    return "null"


def extract_features():
    count = 0
    d = load_json()

    for feature in d:
        data = {}
        count += 1
        if count > 1:
            break

        print feature['timestamp'], feature['@timestamp'], feature['email_id'], feature['offset']

        data['timestamp'] = feature['timestamp']
        data['@timestamp'] = feature['@timestamp']
        data['email_id'] = feature['email_id']
        data['offset'] = feature['offset']
        data['Course_Id'] = extract_course_id(feature['client_msg'].encode('utf-8').strip())
        data['Video_Id'] = extract_video_id(feature['client_msg'].encode('utf-8').strip())
        data['Kenlist_Id'] = extract_kenlist_id(feature['client_msg'].encode('utf-8').strip())


extract_features()
