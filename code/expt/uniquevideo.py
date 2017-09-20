import json
import csv
import os
import datetime

path = '/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/'
file = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'
# file ='result_logdump_400000.json'

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

store_week_number = []
with open(path + file, 'r') as data_file:
	for line in data_file.readlines():
        	data = json.loads(line)
		raw_Video_Id = data['Video_Id']
            	raw_date = data['date']
	    	week_number = extract_week_number(raw_date)
		store_week_number.append(week_number)
		print week_number, raw_Video_Id
	print min(store_week_number), len(store_week_number), max(store_week_number)
		

