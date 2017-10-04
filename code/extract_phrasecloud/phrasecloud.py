import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
from config import project_folder

# project_folder = "/home/shivam/coursework/user engagement/User-Engagement-Video"
# path = project_folder + "/code/extract_phrasecloud/user_data_test/"
path = project_folder + "code/userdata/"


def extract_week_number(raw_date):
    year = raw_date[:4]
    month = raw_date[5:7]
    day = raw_date[8:]
    dt = datetime.date(int(year), int(month), int(day))
    wk = dt.isocalendar()[1]
    return wk


def create_phrasecloud_dictionary(min_week, max_week):
    phrase_cloud_clicks = {}
    for i in range(min_week, max_week + 1):
        phrase_cloud_clicks[i] = 0

    return phrase_cloud_clicks


def extract_phrasecloud_clicks():
    # main_db = []
    user_log = {}
    count = 0
    for file in os.listdir(path):
        count += 1
        print count
        if file != ".gitignore":
            phrase_cloud_clicks = create_phrasecloud_dictionary(18, 37)
            with open(path + file, 'r') as data_file:
                for line in data_file.readlines():
                    data = json.loads(line)

                    if data['user_action'] != None and "phrase" in data['user_action']:
                        week_number = extract_week_number(data['date'])
                        if week_number in phrase_cloud_clicks:
                            phrase_cloud_clicks[week_number] += 1
                        else:
                            phrase_cloud_clicks[week_number] = 1

                user_log[file.split("_")[1].split(".")[0]] = phrase_cloud_clicks

    max_click = 0
    for user in user_log:
        for week in user_log[user]:
            if user_log[user][week] > max_click:
                max_click = user_log[user][week]

    for user in user_log:
        for week in user_log[user]:
            user_log[user][week] /= max_click

    return user_log


def save(data):
    details = [data]
    with open('phrase_cloud_user.csv', 'a') as testfile:  # append it data to the csv file
        csv_writer = csv.writer(testfile)
        csv_writer.writerow(details[0])


def plot_behaviour():
    phrase_cloud_clicks = extract_phrasecloud_clicks()

    for user in phrase_cloud_clicks:
        # print user
        keys = phrase_cloud_clicks[user].keys()
        values = phrase_cloud_clicks[user].values()

        Z1 = sorted(keys)
        # print Z1
        Z2 = [x for _, x in sorted(zip(keys, values))]
        save(Z2)
        plt.plot(Z1, Z2)

    plt.savefig("phrasecloud.png")
    plt.show()


# plot_behaviour()
