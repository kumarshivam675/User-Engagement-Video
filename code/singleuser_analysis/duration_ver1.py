import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
import pafy
from config import project_folder

path = project_folder + "/code/"
# path = '/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/'
file1 = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'

videos = []


def get_video():
    with open(path + file1, 'r') as data_file:
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
            print i
            v = url + i.encode('utf-8').strip()
            video = pafy.new(v)
            videos_duration[i] = video.duration
    return videos_duration


videos_access = []
videos_access = get_video()
print videos_access
videos_duration = {}
videos_duration = get_video_duration(videos_access)
print videos_duration

'''
def extract_week_number(raw_date):
    year = raw_date[:4]
    month = raw_date[5:7]
    day = raw_date[8:]
    dt = datetime.date(int(year), int(month), int(day))
    wk = dt.isocalendar()[1]
    return wk


def create_leaderboard_dictionary(min_week, max_week):
    leaderboard_access = {}
    for i in range(min_week, max_week + 1):
        leaderboard_access[i] = []

    return leaderboard_access


def extract_leaderboard_access():
    leaderboard_access = create_leaderboard_dictionary(23, 35)
    with open(path + file, 'r') as data_file:
        for line in data_file.readlines():
            data = json.loads(line)
            if "leaderboard" in data['user_action']:
                week_number = extract_week_number(data['date'])
                if week_number in leaderboard_access:
                    leaderboard_access[week_number].append(data['Video_Id'])
                else:
                    leaderboard_access[week_number] = [data['Video_Id']]

    for key in leaderboard_access:
        print key, len(set(leaderboard_access[key]))
        print "\n"

    return leaderboard_access


def plot_behaviour():
    leaderboard_access = extract_leaderboard_access()
    rowX = []
    rowY = []

    for key in leaderboard_access:
        rowX.append(key)
        rowY.append(len(leaderboard_access[key]))

    print rowX
    print rowY
    X = sorted(rowX)
    Y = [x for _, x in sorted(zip(rowX, rowY))]
    plt.plot(X, Y, )
    plt.show()
    plt.savefig('leaderboard.png')


plot_behaviour()
'''
