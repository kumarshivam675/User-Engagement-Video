import csv


def save(file, timestamp, pid, client_message, offset, timestamp_2):

    hello = [[file, timestamp, pid, client_message, offset, timestamp_2]]

    with open('user_fb62884cc3fa8a4bfb36535fa628acff22830025acb5ebe31e1ef5ef.csv', 'a') as testfile:     # append it data to the csv file
        csv_writer = csv.writer(testfile)
        csv_writer.writerow(hello[0])
