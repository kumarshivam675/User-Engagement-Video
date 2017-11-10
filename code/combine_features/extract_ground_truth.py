import csv
from config import project_folder
import numpy as np


# def ground_truth():
#     score = []
#     total = []
#     email = []
#
#     with open(project_folder + "code/leaderboard_data/leaderboard.csv") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             score.append(int(row['Quiz Score'].split(" out of ")[0]))
#             total.append(int(row['Quiz Score'].split(" out of ")[1]))
#             email.append(row['Email'])
#
#     list_cluster = {}
#     for i in range(len(email)):
#         if total[i] >0:
#             if ((score[i])*100)/total[i] >= 90.0:
#                 list_cluster[email[i]] = 0
#             elif ((score[i])*100)/total[i] < 90.0 and ((score[i])*100)/total[i] >= 50.0:
#                 list_cluster[email[i]] = 1
#             elif ((score[i])*100)/total[i] < 50.0 and ((score[i])*100)/total[i] >= 10:
#                 list_cluster[email[i]] = 2
#             elif ((score[i])*100)/total[i] < 10.0:
#                 list_cluster[email[i]] = 2
#         elif total[i] == 0:
#             list_cluster[email[i]] = 2
#
#     return list_cluster


def ground_truth():
    score = []
    total = []
    email = []

    with open(project_folder + "code/leaderboard_data/leaderboard.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            score.append(int(row['Quiz Score'].split(" out of ")[0]))
            total.append(int(row['Quiz Score'].split(" out of ")[1]))
            email.append(row['Email'])

    list_cluster = {}
    for i in range(len(email)):
        if total[i] > 0:
            list_cluster[email[i]] = float(score[i]*100)/float(total[i])
        elif total[i] == 0:
            list_cluster[email[i]] = 0.0

    return list_cluster


