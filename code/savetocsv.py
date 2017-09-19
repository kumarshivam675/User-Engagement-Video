import csv


def save(file, timestamp, pid, client_message, offset, timestamp_2):

    hello = [[file, timestamp, pid, client_message, offset, timestamp_2]]

    with open('user_all_logdump_400000.csv', 'a') as testfile:     # append it data to the csv file
        csv_writer = csv.writer(testfile)
        csv_writer.writerow(hello[0])
