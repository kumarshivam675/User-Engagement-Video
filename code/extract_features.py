import json
import csv
import savetocsv
import os

path = '/home/shivam/coursework/user engagement/User-Engagement-Video/logdumps_organisationX/'


def extract_user_action_info(client_msg):
    if "Course : " in client_msg:
        json.loads(client_msg)
        # print client_msg.split("Course : ")
        # print client_msg.split("Course : ")[1]
        # print client_msg.split("Course : ")[1].split(" : ")[0]
        # if "video_id" in client_msg:
        #     print "hi"
            # print client_msg.split("video_id : ")[1].split(" : ")[0]



def extract_actions(email):
    for file in ['logdump_700000.json']:
        with open(path + file) as json_data:
            d = json.load(json_data)

            for feature in d:
                if feature['email_id'] == email:
                    extract_user_action_info(feature['client_msg'])




extract_actions('fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef')

