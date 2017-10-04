import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
from config import project_folder

path = project_folder + "code/extract_uniquevideo/user_data_test/"


def extract_week_number(raw_date):
    year = raw_date[:4]
    month = raw_date[5:7]
    day = raw_date[8:]
    dt = datetime.date(int(year), int(month), int(day))
    wk = dt.isocalendar()[1]
    return wk


def create_unique_video_dictionary(min_week, max_week):
    temp_dict = {}
    for i in range(min_week, max_week + 1):
        temp_dict[i] = []
    return temp_dict


def save(data):
        details = [data]
        with open('unique_video_user.csv', 'a') as testfile:     # append it data to the csv file
                csv_writer = csv.writer(testfile)
                csv_writer.writerow(details[0])
store_week_number = []
main_db_unique_video = []
week_unique_video = create_unique_video_dictionary(18, 37)

for file in os.listdir(path):
    if file != '.gitignore':
        with open(path + file, 'r') as data_file:
            for line in data_file.readlines():
                data = json.loads(line)
                raw_Video_Id = data['Video_Id']
                raw_date = data['date']
                week_number = extract_week_number(raw_date)
                if raw_Video_Id != 'null':

                    if week_number in week_unique_video:
                        week_unique_video[week_number].append(raw_Video_Id)
                    else:
                        week_unique_video[week_number] = [raw_Video_Id]
            temp_values = []
            for key in week_unique_video:
                temp_values.append(len(list(set(week_unique_video[key]))))
            main_db_unique_video.append(temp_values)

# print main_db_unique_video
for i in main_db_unique_video:
    print len(i)
keys = []
for key in week_unique_video:
    keys.append(key)

Z1 = sorted(keys)
copy = []
for i in main_db_unique_video:
    tmp = []
    tmp = [x for _, x in sorted(zip(keys, i))]
    copy.append(tmp)

# print copy
for i in copy:
    save(i)
    plt.plot(Z1, i)
plt.savefig('uniquevideo.png')
plt.show()
