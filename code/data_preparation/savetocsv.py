import csv


def save(file, timestamp, pid, client_message, offset, timestamp_2):

    hello = [[file, timestamp, pid, client_message, offset, timestamp_2]]

    with open('user_video_9db9c3e9d33364b57be6ad1f5707c011e76a26bfe15e653cf8d8d189.csv', 'a') as testfile:     # append it data to the csv file
        csv_writer = csv.writer(testfile)
        csv_writer.writerow(hello[0])
