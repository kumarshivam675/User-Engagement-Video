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


def create_query_dictionary(min_week, max_week):
    query_searches = {}
    for i in range(min_week, max_week + 1):
        query_searches[i] = 0.0
    return query_searches


def extract_query_clicks():
    print "query"
    user_log = {}
    count = 0
    for file in os.listdir(path):
        query_clicks = create_query_dictionary(18, 37)
        count += 1
        if file != ".gitignore":
            with open(path + file, 'r') as data_file:
                for line in data_file.readlines():
                    data = json.loads(line)
                    if data['user_action'] != None and "query" in data['user_action']:
                        week_number = extract_week_number(data['date'])
                        if week_number in query_clicks:
                            query_clicks[week_number] += 1
                        else:
                            query_clicks[week_number] = 1.0
                user_log[file.split("_")[1].split(".")[0]] = query_clicks

    max_click = 0
    for user in user_log:
        for week in user_log[user]:
            if user_log[user][week] > max_click:
                max_click = user_log[user][week]

    for user in user_log:
        for week in user_log[user]:
            user_log[user][week] /= max_click

    return user_log


def queryplot_behaviour():
    query_clicks = extract_query_clicks()

    for user in mmtoc_clicks:
        keys = query_clicks[user].keys()
        values = query_clicks[user].values()
        Z1 = sorted(keys)
        Z2 = [x for _, x in sorted(zip(keys, values))]
        plt.plot(Z1, Z2)
    plt.savefig("query.png")
    plt.show()

queryplot_behaviour()
