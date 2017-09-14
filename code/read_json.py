import json

path = '/home/shivam/coursework/user engagement/User-Engagement-Video/logdumps_organisationX/'

count = 0
with open(path + 'logdump_2000000.json') as json_data:
    d = json.load(json_data)

# count = 1
# for feature in d:
#     count += 1
#     if count > 1000:
#         break
#     with open('data2.txt', 'a') as outfile:
#         json.dump(feature, outfile)

count = 1
for feature in d:
    count += 1
    if count > 3:
        break
    with open('test.json', 'a') as outfile:
        if feature['email_id'] == 'fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef':
            json.dump(feature, outfile)




