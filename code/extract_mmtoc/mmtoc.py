import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
from config import project_folder

# project_folder = "/home/shivam/coursework/user engagement/User-Engagement-Video/"
path = project_folder + "code/userdata/"


def extract_week_number(raw_date):
    year = raw_date[:4]
    month = raw_date[5:7]
    day = raw_date[8:]
    dt = datetime.date(int(year), int(month), int(day))
    wk = dt.isocalendar()[1]
    return wk


def create_mmtoc_dictionary(min_week, max_week):
    phrase_cloud_clicks = {}
    for i in range(min_week, max_week + 1):
        phrase_cloud_clicks[i] = 0.0

    return phrase_cloud_clicks


def extract_mmtoc_clicks():
    print "mmtoc"
    user_log = {}
    count = 0
    for file in os.listdir(path):
        mmtoc_clicks = create_mmtoc_dictionary(18, 37)
        count += 1
        print count
        # if count > 100:
        #     break
        if file != ".gitginore":
            with open(path + file, 'r') as data_file:
                for line in data_file.readlines():
                    data = json.loads(line)

                    if data['user_action'] != None and "mmtoc" in data['user_action']:
                        week_number = extract_week_number(data['date'])
                        if week_number in mmtoc_clicks:
                            mmtoc_clicks[week_number] += 1
                        else:
                            mmtoc_clicks[week_number] = 1.0

                user_log[file.split("_")[1].split(".")[0]] = mmtoc_clicks

    max_click = 0
    for user in user_log:
        for week in user_log[user]:
            if user_log[user][week] > max_click:
                max_click = user_log[user][week]

    # print "max click ", max_click
    for user in user_log:
        for week in user_log[user]:
            user_log[user][week] /= max_click

    return user_log


def mmtocplot_behaviour():
    mmtoc_clicks = extract_mmtoc_clicks()

    for user in mmtoc_clicks:
        # print user
        keys = mmtoc_clicks[user].keys()
        values = mmtoc_clicks[user].values()

        Z1 = sorted(keys)
        Z2 = [x for _, x in sorted(zip(keys, values))]
        plt.plot(Z1, Z2)

    plt.savefig("mmtoc.png")
    plt.show()


# extract_mmtoc_clicks()
# mmtocplot_behaviour()