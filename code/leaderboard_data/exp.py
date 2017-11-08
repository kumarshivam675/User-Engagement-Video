import csv


score = []
total = []

with open("leaderboard.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        score.append(int(row['Quiz Score'].split(" out of ")[0]))
        total.append(int(row['Quiz Score'].split(" out of ")[1]))


count = 0
for sc in score:
    if sc < 1000:
        count += 1

print count
