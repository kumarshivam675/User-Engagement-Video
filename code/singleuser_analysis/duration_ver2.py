import json
import csv
import os
import datetime
import matplotlib.pyplot as plt
import pafy
from config import project_folder

path = project_folder + "/code/userdata/"
# path = '/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/'
file1 = 'result_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.json'

videos = []
def get_video():
	with open( path + file1, 'r') as data_file:
		for line in data_file.readlines():
			data = json.loads(line)
			if data['video_log'] == "true":
				if data['Video_Id'] not in videos:
					videos.append(data['Video_Id'])

	return videos

def get_video_duration(videos):
	url = "https://www.youtube.com/watch?v="
	for i in videos:
		if i!='null':
			
			v = url + i.encode('utf-8').strip()
			video = pafy.new(v)
			videos_duration[i] = video.duration
	return videos_duration

def get_logs(videos_access):
	a = []
        with open( path + file1, 'r') as data_file:
                for line in data_file.readlines():
                        data = json.loads(line)
                        if data['Video_Id'] == videos_access[3] and data['video_log'] == 'true':
				
				a.append([data['@timestamp'], data['user_action'], data['time_in_seconds']])
		

		a.sort(key=lambda x: x[0])
		for i in a:
			print i

videos_access = get_video()					
print videos_access
videos_duration = {}
# videos_duration = get_video_duration(videos_access)
print videos_duration
get_logs(videos_access)

