import json
import re
import os
import csv
from config import project_folder


path = project_folder + "logdumps_organisationX/"


def load_json():
    with open(path + 'logdump_2000000.json') as json_data:
        d = json.load(json_data)

    return d


def extract_course_id(client_msg):
    # print client_msg
    if "Course : " in client_msg:
        return client_msg.split("Course : ")[1].split(" :")[0]
    elif "course_id: " in client_msg:
        return client_msg.split("course_id: '")[1].split("'")[0]

    return "null"


def extract_video_id(client_msg):
    # print client_msg
    if ": video" in client_msg:
        if ": video id" in client_msg:
            return client_msg.split("video id  : ")[1].split(" :")[0]
        elif ": video" in client_msg:
            return client_msg.split("video : ")[1].split(" :")[0]

    if "youtube_id: " in client_msg:
        return client_msg.split("youtube_id: '")[1].split("'")[0]

    return "null"


def extract_kenlist_id(client_msg):
    # print client_msg
    if "kenlistID :" in client_msg:
        if "at : " in client_msg.split("kenlistID : ")[1]:
            return re.sub("[^0-9]", "", client_msg.split("kenlistID : ")[1].split(" :")[0])
        else:
            return client_msg.split("kenlistID : ")[1].split("'")[0]

    if "playlist_id: '" in client_msg:
        return client_msg.split("playlist_id: '")[1].split("'")[0]

    return "null"


def extract_time_in_seconds(client_msg):
    if "kenlistID :" in client_msg:
        if "at : " in  client_msg.split("kenlistID : ")[1]:
            time = re.sub("[^0-9.]", "", client_msg.split("kenlistID : ")[1].split(" : ")[1])
            if time[-1] == '.':
                time = time[:-1]

            return time

    if "User playing time" in client_msg:
        client_msg.split("User playing time")[1].split(":")

    return "null"


def extract_user_action(client_msg):
    if "content_id :" in client_msg:
        return client_msg.split("msg: ")[1].split(" content_id :")[0][1:]

    else:
        if "curriculum" in client_msg or "leaderboard" in client_msg:
            if "msg:'" not in client_msg and "msg: '" not in client_msg:
                return client_msg.split("msg: ")[1][:-3]
            else:
                if "msg: '" in client_msg:
                    return client_msg.split("msg: '")[1].split("'")[0]
                elif "msg:'" in client_msg:
                    return client_msg.split("msg:'")[1].split("'")[0]
        else:
            if "msg: '" in client_msg:
                return client_msg.split("msg: '")[1].split("'")[0]
            elif "msg:'" in client_msg:
                return client_msg.split("msg:'")[1].split("'")[0]


def check_if_video_log(client_msg):
    if "quiz" in client_msg or "Quiz" in client_msg:
        return "false"
    if "log:" in client_msg:
        return "true"

    return "false"


def count_unique_user():
    email_list = []
    for file in os.listdir(path):
        if file != '.gitignore':
            print file, len(email_list)
            with open(path + file) as json_data:
                d = json.load(json_data)

            for feature in d:
                if feature['email_id'] not in email_list:
                    email_list.append(feature['email_id'])

    print len(email_list)
    return email_list


def export_email_list_to_file(email_list):
    for email in email_list:
        hello = [[email]]

        with open('email_list.csv', 'a') as testfile:     # append it data to the csv file
            csv_writer = csv.writer(testfile)
            csv_writer.writerow(hello[0])


def extract_features():
    # d = load_json()
    file_count = 0
    for file in os.listdir(path):
        output = {}
        file_count += 1
        print file_count
        if file != ".gitignore":
            with open("result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json", 'a') as fp:
                print file
                count = 0
                with open(path + file) as json_data:
                    d = json.load(json_data)
                for feature in d:
                    if feature['email_id'] == 'fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef':
                        count += 1
                        try:
                            data = {}
                            # print feature['client_msg'].encode('utf-8').strip()

                            data['email_id'] = feature['email_id']
                            data['timestamp'] = feature['timestamp']
                            data['@timestamp'] = feature['@timestamp']
                            data['date'] = feature['@timestamp'].split("T")[0]
                            data['time'] = feature['@timestamp'].split("T")[1][:-2]
                            data['email_id'] = feature['email_id']
                            data['offset'] = feature['offset']
                            data['Course_Id'] = extract_course_id(feature['client_msg'].encode('utf-8').strip())
                            data['Video_Id'] = extract_video_id(feature['client_msg'].encode('utf-8').strip())
                            data['Kenlist_Id'] = extract_kenlist_id(feature['client_msg'].encode('utf-8').strip())
                            data['time_in_seconds'] = extract_time_in_seconds(feature['client_msg'].encode('utf-8').strip())
                            data['user_action'] = extract_user_action(feature['client_msg'].encode('utf-8').strip())
                            data['video_log'] = check_if_video_log(feature['client_msg'].encode('utf-8').strip())

                            json.dump(data, fp)
                            fp.write('\n')
                        except:
                            print "issue in " + file + "  on line no " + str(count)

    print count


def create_json_user_wise():
    file_count = 0
    for file in os.listdir(path):
        file_count += 1
        print file_count
        if file != ".gitignore":
            print file
            count = 0
            with open(path + file) as json_data:
                d = json.load(json_data)
            for feature in d:
                with open("./userdata/result_"+feature['email_id']+".json", 'a') as fp:
                    count += 1
                    try:
                        data = {}
                        # print feature['client_msg'].encode('utf-8').strip()

                        data['email_id'] = feature['email_id']
                        data['timestamp'] = feature['timestamp']
                        data['@timestamp'] = feature['@timestamp']
                        data['date'] = feature['@timestamp'].split("T")[0]
                        data['time'] = feature['@timestamp'].split("T")[1][:-2]
                        data['email_id'] = feature['email_id']
                        data['offset'] = feature['offset']
                        data['Course_Id'] = extract_course_id(feature['client_msg'].encode('utf-8').strip())
                        data['Video_Id'] = extract_video_id(feature['client_msg'].encode('utf-8').strip())
                        data['Kenlist_Id'] = extract_kenlist_id(feature['client_msg'].encode('utf-8').strip())
                        data['time_in_seconds'] = extract_time_in_seconds(feature['client_msg'].encode('utf-8').strip())
                        data['user_action'] = extract_user_action(feature['client_msg'].encode('utf-8').strip())
                        data['video_log'] = check_if_video_log(feature['client_msg'].encode('utf-8').strip())

                        json.dump(data, fp)
                        fp.write('\n')
                    except:
                        print "issue in " + file + "  on line no " + str(count)

    print count


# extract_features()
# email_list = count_unique_user()
# export_email_list_to_file(email_list)
create_json_user_wise()