import json
import csv
import os
import datetime
import matplotlib.pyplot as plt

path = '/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/user_data_test/'
# path = '/home/shivam/coursework/user engagement/User-Engagement-Video/code/'
file = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'


def extract_week_number(raw_date):
    year = raw_date[:4]
    month = raw_date[5:7]
    day = raw_date[8:]
    dt = datetime.date(int(year), int(month), int(day))
    wk = dt.isocalendar()[1]
    return wk


def create_phrasecloud_dictionary(min_week, max_week):
    phrase_cloud_clicks = {}
    for i in range(min_week, max_week+1):
        phrase_cloud_clicks[i] = []

    return phrase_cloud_clicks


def extract_phrasecloud_clicks():
	main_db = []
	phrase_cloud_clicks = create_phrasecloud_dictionary(18,45)
	for file in os.listdir(path):
		
    		with open(path + file, 'r') as data_file:
        		for line in data_file.readlines():
            			data = json.loads(line)
            			if "phrase" in data['user_action']:
                			week_number = extract_week_number(data['date'])
                			if week_number in phrase_cloud_clicks:
                    				phrase_cloud_clicks[week_number].append(data['Video_Id'])
                			else:
                    				phrase_cloud_clicks[week_number] = [data['Video_Id']]
			temp_values = []
			for key in phrase_cloud_clicks:
				temp_values.append(len(phrase_cloud_clicks[key]))
			main_db.append(temp_values)
    	return main_db



def plot_behaviour():
    phrase_cloud_clicks = extract_phrasecloud_clicks()
    print phrase_cloud_clicks    
    rowX = []
    
    for i in range(18,45):
	rowX.append(i)
    
    X = sorted(rowX)
    print '-------------------------------------------------------'
    print X
    copy = []
    for i in phrase_cloud_clicks:
	tmp = []
	tmp = [x for _,x in sorted(zip(rowX, i))]
	copy.append(tmp)

    print len(copy[0]), len(X)
    for i in copy:
	print 'yes'
    	plt.plot(X, i)
    plt.savefig('phrasecloud.png')
    plt.show()

plot_behaviour()


