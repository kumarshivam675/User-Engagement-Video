import sys
import csv
from config import project_folder

sys.path.insert(0, project_folder + 'code/extract_duration')
sys.path.insert(0, project_folder + 'code/extract_phrasecloud')
sys.path.insert(0, project_folder + 'code/extract_mmtoc')

import duration_ver3
import phrasecloud
import mmtoc


def sort_values_on_keys(dictionary):
    keys = dictionary.keys()
    values = dictionary.values()

    a1 = sorted(keys)
    a2 = [x for _, x in sorted(zip(keys, values))]
    return a2


# def extract_vectors(dict1, dict2, dict3):
#     f1 = sort_values_on_keys(dict1)
#     f2 = sort_values_on_keys(dict2)
#     f3 = sort_values_on_keys(dict3)
#     return f1, f2, f3


def extract_vectors(dict):
    f1 = sort_values_on_keys(dict)
    return f1


def multiply_scalar_vector(wt, vec):
    return [i * wt for i in vec]


def add_lists(l1, l2, l3):
    return map(sum, zip(l1, l2, l3))


def save(email, data, filename):
    data.insert(0, email) #insert email id in the beginning
    details = [data]
    with open(filename, 'a') as testfile:  # append it data to the csv file
        csv_writer = csv.writer(testfile)
        csv_writer.writerow(details[0])


def combine_vectors(mmtoc_wt, phrase_wt, duration_wt):
    mmtoc_dict = mmtoc.extract_mmtoc_clicks()
    phrasecloud_dict = phrasecloud.extract_phrasecloud_clicks()
    duration_dict = duration_ver3.create_video_log()
    count = 0

    for user in phrasecloud_dict:
        count += 1
        print count
        mmtoc_vector = extract_vectors(mmtoc_dict[user])
        phrasecloud_vector = extract_vectors(phrasecloud_dict[user])
        duration_vector = extract_vectors(duration_dict[user])

        # print "vector extraction done"

        weighted_f1 = multiply_scalar_vector(mmtoc_wt, mmtoc_vector)
        weighted_f2 = multiply_scalar_vector(phrase_wt, phrasecloud_vector)
        weighted_f3 = multiply_scalar_vector(duration_wt, duration_vector)

        # print "vector multiplication done"

        feature_vector = add_lists(weighted_f1, weighted_f2, weighted_f3)

        # print "beginning to save in the csv"
        save(user, feature_vector, "feature_vectors.csv")

        save(user, multiply_scalar_vector(1, mmtoc_vector), "mmtoc_vectors.csv")
        save(user, multiply_scalar_vector(1, duration_vector), "duration_vectors.csv")
        save(user, multiply_scalar_vector(1, phrasecloud_vector), "phrasecloud_vectors.csv")


combine_vectors(0.3, 0.3, 0.4)

