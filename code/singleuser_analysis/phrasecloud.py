import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
from config import project_folder

path = project_folder + "/code/singleuser_analysis/"
# path = '/home/shivam/coursework/user engagement/User-Engagement-Video/code/'
file = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'


def extract_week_number(raw_date):
    year = raw_date[:4]
    month = raw_date[5:7]
    day = raw_date[8:]
    dt = datetime.date(int(year), int(month), int(day))
    wk = dt.isocalendar()[1]
    return wk


def create_phrasecloud_dictionary(min_week, max_week):
    phrase_cloud_clicks = {}
    for i in range(min_week, max_week+1):
        phrase_cloud_clicks[i] = []

    return phrase_cloud_clicks


def extract_phrasecloud_clicks():
    phrase_cloud_clicks = create_phrasecloud_dictionary(23, 35)
    with open(path + file, 'r') as data_file:
        for line in data_file.readlines():
            data = json.loads(line)
            if "phrase" in data['user_action']:
                week_number = extract_week_number(data['date'])
                if week_number in phrase_cloud_clicks:
                    phrase_cloud_clicks[week_number].append(data['Video_Id'])
                else:
                    phrase_cloud_clicks[week_number] = [data['Video_Id']]

    for key in phrase_cloud_clicks:
        print key, len(set(phrase_cloud_clicks[key]))
        print "\n"

    return phrase_cloud_clicks


def plot_behaviour():
    phrase_cloud_clicks = extract_phrasecloud_clicks()
    rowX = []
    rowY = []

    for key in phrase_cloud_clicks:
        rowX.append(key)
        rowY.append(len(phrase_cloud_clicks[key]))

    print rowX
    print rowY
    X = sorted(rowX)
    Y = [x for _,x in sorted(zip(rowX, rowY))]
    plt.plot(X, Y,)
    plt.show()
    plt.savefig('phrasecloud.png')


plot_behaviour()


