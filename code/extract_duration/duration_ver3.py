import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
import pafy
#from config import project_folder
import time, datetime

project_folder = '/home/shivam/coursework/user engagement/User-Engagement-Video'
path = project_folder + "/code/extract_duration/uservideodata/"


# path = '/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/'

def create_unique_video_dictionary(min_week, max_week):
    temp_dict = {}
    for i in range(min_week, max_week + 1):
        temp_dict[i] = {}
    return temp_dict


def add_to_dict(week, email, video, duration, length, user_summary):
    # user_summary[week].append([video, duration/length])
    # print user_summary[week]
    if week in user_summary:
        time = duration / length
        if time > 1:
            time = 1.0
        if video in user_summary[week]:
            user_summary[week][video].append(time)
        else:
            user_summary[week][video] = [time]

    return user_summary


def get_summary(user_summary):
    user_week_summary = {}
    for week in user_summary:
        video_count = len(user_summary[week])
        duration = 0.0
        for video in user_summary[week]:
            duration += sum(user_summary[week][video]) / len(user_summary[week][video])
        if video_count == 0:
            user_week_summary[week] = 0.0
        else:
            user_week_summary[week] = duration / video_count

    for week in user_week_summary:
        print week, user_week_summary[week]
    return user_week_summary


def save(data):
    details = [data]
    with open('video_duration_user.csv', 'a') as testfile:  # append it data to the csv file
        csv_writer = csv.writer(testfile)
        csv_writer.writerow(details[0])


def create_video_log():
    # for file in ['result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json']:
    count = 0
    user_log = {}
    user_summary = create_unique_video_dictionary(18, 37)
    for file in os.listdir(path):
        if file != ".gitignore":
            print file
            count += 1
            if count > 240:
                break
            with open(path + file, 'r') as data_file:
                for line in data_file.readlines():
                    data = json.loads(line)
                    week = data['week']
                    email = data['email_id']
                    video = data['Video_Id']
                    duration = data['duration']
                    length = data['video_length']
                    user_summary = add_to_dict(week, email, video, duration, length, user_summary)

            user_summary_week_wise = get_summary(user_summary)

            user_log[file.split("_")[1].split(".")[0]] = user_summary_week_wise

    return user_log


def plot():
    result = []
    user_log = create_video_log()
    for user_summary_week_wise in user_log:
        keys = user_log[user_summary_week_wise].keys()
        values = user_log[user_summary_week_wise].values()

        Z1 = sorted(keys)
        Z2 = [x for _, x in sorted(zip(keys, values))]

        result.append(Z2)

    for i in result:
        plt.plot(Z1, i)
        # save(i)
    plt.savefig('videoduration.png')
    plt.show()


# create_video_log()
plot()