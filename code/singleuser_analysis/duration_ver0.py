import csv

f = open('video_duration.csv', 'r')

videos = []
with f:
    reader = csv.DictReader(f)
    for row in reader:
            videos.append(row['video_id'])

