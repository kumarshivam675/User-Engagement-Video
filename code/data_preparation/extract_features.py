import json
import csv
import savetocsv
import os
from config import project_folder

path = project_folder + "logdumps_organisationX/"

for file in os.listdir(path):
    with open(path + file, 'r') as data_file:
        for line in data_file.readlines():
            data = json.loads(line)
            print data
            break

