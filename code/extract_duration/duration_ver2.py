import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
import pafy
# from config import project_folder
project_folder = "/home/shivam/coursework/user engagement/User-Engagement-Video/"
path = project_folder + "code/userdata/"
# path = '/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/'
file1 = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'


def get_video(file):
    videos = []
    with open(path + file, 'r') as data_file:
        for line in data_file.readlines():
            data = json.loads(line)
            if data['video_log'] == "true":
                if data['Video_Id'] not in videos:
                    videos.append(data['Video_Id'])

    return videos


def get_video_duration(videos):
    url = "https://www.youtube.com/watch?v="
    for i in videos:
        if i != 'null':
            v = url + i.encode('utf-8').strip()
            video = pafy.new(v)
            videos_duration[i] = video.duration
    return videos_duration


def get_log_single_video(video):
    # a = []
    date_wise = {}
    with open(path + file1, 'r') as data_file:
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
        # print duration

    return date_wise_duration


def get_log_user(video_access, email): #list of all videos of a given user
    json_object = []
    for video in video_access:
        video_length = 30
        single_video = get_log_single_video(video)
        date_wise_duration = extract_watch_duration(single_video, video_length)
        for date in date_wise_duration:
            data = {}
            data['Video_Id'] = video
            data['email_id'] = email
            data['date'] = date
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
