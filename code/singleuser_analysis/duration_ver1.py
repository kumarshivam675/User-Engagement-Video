import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
import pafy
from config import project_folder

path = project_folder + "/code/userdata/"
# path = '/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/'
file1 = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'

videos = []


def create_json_user_wise():
    file_count = 0
    for file in os.listdir(path):
        file_count += 1
        print file_count
        if file != ".gitignore":
            print file
            count = 0
            with open(path + file, 'r') as data_file:
                for line in data_file.readlines():
                    data = json.loads(line)
                    if data['video_log'] == "true":
                        if data['Video_Id'] not in videos:
                            videos.append(data['Video_Id'])

    return videos


def get_video_duration(videos):
    url = "https://www.youtube.com/watch?v="
    count = 0
    for i in videos:
        count = count + 1
        print count, " ", i
        try:
            if i != 'null':
                v = url + i.encode('utf-8').strip()
                video = pafy.new(v)
                videos_duration[i] = video.duration

        except:
            print 'Error'
    return videos_duration


def save(video_id, duration):
    details = [[video_id, duration]]
    with open('video_duration.csv', 'a') as testfile:  # append it data to the csv file
        csv_writer = csv.writer(testfile)
        csv_writer.writerow(details[0])


videos_access = []
videos_access = create_json_user_wise()
print len(videos_access)
videos_duration = {}
# videos_duration = get_video_duration(videos_access)
for key in videos_duration:
    save(key, videos_duration[key])
print len(videos_duration)

f = open('video_duration.csv', 'r')
videos_exist = []
with f:
    reader = csv.DictReader(f)
    for row in reader:
        videos_exist.append(row['video_id'])
print len(videos_exist)

list3 = [item for item in videos_access if item not in videos_exist]
print len(list3)
print list3
