import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
from config import project_folder

path = project_folder + "code/"
file = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'


def extract_week_number(raw_date):
    year = raw_date[:4]
    month = raw_date[5:7]
    day = raw_date[8:]
    dt = datetime.date(int(year), int(month), int(day))
    wk = dt.isocalendar()[1]
    return wk


'''
with open(path + file, 'r') as data_file:
	for line in data_file.readlines():
        	data = json.loads(line)
		print data
		break	
'''


def create_unique_video_dictionary(min_week, max_week):
    temp_dict = {}
    for i in range(min_week, max_week + 1):
        temp_dict[i] = []
    return temp_dict


store_week_number = []
week_unique_video = create_unique_video_dictionary(23, 35)

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
        store_week_number.append(week_number)

    print min(store_week_number), len(store_week_number), max(store_week_number)

    keys = []
    values1 = []
    values2 = []
    for key in week_unique_video:
        keys.append(key)
        values1.append(len(list(set(week_unique_video[key]))))
        values2.append(len(week_unique_video[key]))

Z1 = sorted(keys)
Z2 = [x for _, x in sorted(zip(keys, values1))]
Z3 = [x for _, x in sorted(zip(keys, values2))]

print(Z1)
print(Z2)
print(Z3)

plt.plot(Z1, Z2)
plt.savefig('uniquevideo.png')
plt.show()
