import csv
import numpy as np

score = []
total = []
email = []



with open("leaderboard.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        score.append(int(row['Quiz Score'].split(" out of ")[0]))
        total.append(int(row['Quiz Score'].split(" out of ")[1]))
        email.append(row['Email'])

list_cluster = {}
for i in range(len(email)):
    if total[i] >0:
        if ((score[i])*100)/total[i] >= 90.0:
            list_cluster[email[i]] = 1
        elif ((score[i])*100)/total[i] < 90.0 and ((score[i])*100)/total[i] >= 50.0:
            list_cluster[email[i]] = 2
        elif ((score[i])*100)/total[i] < 50.0 and ((score[i])*100)/total[i] >= 10:
            list_cluster[email[i]] = 3
        elif ((score[i])*100)/total[i] < 10.0:
            list_cluster[email[i]] = 3
    elif total[i] == 0:
        list_cluster[email[i]] = 4


