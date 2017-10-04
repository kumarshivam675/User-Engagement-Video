import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
import pafy
import time, datetime
from config import project_folder

# project_folder = "/home/shivam/coursework/user engagement/User-Engagement-Video/"
path = project_folder + "code/userdata/"


# path = '/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/'
# file1 = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'


def extract_week_number(raw_date):
    # print raw_date
    year = raw_date[:4]
    month = raw_date[5:7]
    day = raw_date[8:]
    # print year, month, day
    dt = datetime.date(int(year), int(month), int(day))
    wk = dt.isocalendar()[1]
    return wk


def get_video(file):
    videos = []
    with open(path + file, 'r') as data_file:
        for line in data_file.readlines():
            data = json.loads(line)
            if data['video_log'] == "true":
                if data['Video_Id'] not in videos:
                    videos.append(data['Video_Id'])

    return videos


def get_video_duration():
    f = open('video_duration.csv', 'r')
    videos_on_youtube = []
    videos_duration = []
    with f:
        reader = csv.DictReader(f)
        for row in reader:
            videos_on_youtube.append(row['video_id'])
            videos_duration.append(row['duration'])
    videos_duration_seconds = []
    for i in videos_duration:
        a = time.strptime(i, "%H:%M:%S")
        b = datetime.timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).seconds
        videos_duration_seconds.append(b)
    dictionary = dict(zip(videos_on_youtube, videos_duration_seconds))
    return dictionary


def get_log_single_video(video, email):
    # a = []
    date_wise = {}
    with open(path + "result_" + email + ".json", 'r') as data_file:
        for line in data_file.readlines():
            data = json.loads(line)
            if data['Video_Id'] == video and data['video_log'] == 'true':
                if data['date'] in date_wise:
                    date_wise[data['date']].append([data['@timestamp'], data['user_action'], data['time_in_seconds']])
                else:
                    date_wise[data['date']] = [[data['@timestamp'], data['user_action'], data['time_in_seconds']]]

                    # a.append([data['@timestamp'], data['date'], data['user_action'], data['time_in_seconds']])

    for key in date_wise:
        date_wise[key].sort(key=lambda x: x[0])
        # a.sort(key=lambda x: x[0])

    return date_wise


def extract_watch_duration(video, length):
    date_wise_duration = {}
    for date in video:
        # print date
        # print "\n\n"
        duration = 0.0
        prev_state = "None"
        time_ptr = 0.0
        try:
            for action in video[date]:
                # print date, action
                if "pause" in action[1] and prev_state == "playing":
                    duration += abs(float(action[2]) - time_ptr)
                    time_ptr = float(action[2])
                    prev_state = "pause"

                elif "playing" in action[1]:
                    prev_state = "playing"

                elif "buffering" in action[1]:
                    prev_state = "buffering"

                elif "User watched" in action[1] and prev_state == "playing":
                    prev_state = "watched"
                    duration += abs(length - time_ptr)

                elif "User watched" in action[1]:
                    prev_state = "watched"

                if prev_state != "watched":
                    time_ptr = float(action[2])

            date_wise_duration[date] = duration
        except:
            print "error while recording the duration"
            for action in video[date]:
                print date, action
            print "\n\n"
            # print duration

    return date_wise_duration


def get_log_user(video_access, email):  # list of all videos of a given user
    json_object = []
    video_dict = get_video_duration()
    for video in video_access:
        if video in video_dict:
            video_length = video_dict[video]
            single_video = get_log_single_video(video, email)
            date_wise_duration = extract_watch_duration(single_video, video_length)
            for date in date_wise_duration:
                data = {}
                data['Video_Id'] = video
                data['email_id'] = email
                data['date'] = date
                data['week'] = extract_week_number(date)
                data['duration'] = date_wise_duration[date]
                data['video_length'] = video_length
                json_object.append(data)

    with open("./uservideodata/video_" + email + ".json", 'a') as fp:
        for data in json_object:
            json.dump(data, fp)
            fp.write('\n')


def create_video_log():
    # for file in ['result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json']:
    count = 0
    for file in os.listdir(path):
        print file
        count += 1
        print count
        videos_access = get_video(file)
        get_log_user(videos_access, file.split("_")[1].split(".")[0])


# videos_access = get_video(file1)
# get_log_user(videos_access, "123")

create_video_log()
