import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
from config import project_folder

path = project_folder + "code/Preliminary_Single_User_Expts/"
# path = '/home/shivam/coursework/user engagement/User-Engagement-Video/code/'
# file = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'


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
