import json
import csv
import savetocsv
import os

path = '/home/shivam/coursework/user engagement/User-Engagement-Video/code/result/'
# file ='result_logdump_400000.json'

for file in os.listdir(path):
    with open(path + file, 'r') as data_file:
        for line in data_file.readlines():
            data = json.loads(line)
            print data
            break

