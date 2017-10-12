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


def extract_vectors(dict1, dict2, dict3):
    f1 = sort_values_on_keys(dict1)
    f2 = sort_values_on_keys(dict2)
    f3 = sort_values_on_keys(dict3)
    return f1, f2, f3


def multiply_scalar_vector(wt, vec):
    return [i * wt for i in vec]


def add_lists(l1, l2, l3):
    return map(sum, zip(l1, l2, l3))


def save(data):
    details = [data]
    with open('feature_vectors.csv', 'a') as testfile:  # append it data to the csv file
        csv_writer = csv.writer(testfile)
        csv_writer.writerow(details[0])


def combine_vectors(mmtoc_wt, phrase_wt, duration_wt):
    mmtoc_dict = mmtoc.extract_mmtoc_clicks()
    phrasecloud_dict = phrasecloud.extract_phrasecloud_clicks()
    duration = duration_ver3.create_video_log()
    for i in mmtoc_dict:
        try:
            f1, f2, f3 = extract_vectors(mmtoc_dict[i], phrasecloud_dict[i], duration[i])
            weighted_f1 = multiply_scalar_vector(mmtoc_wt, f1)
            weighted_f2 = multiply_scalar_vector(phrase_wt, f2)
            weighted_f3 = multiply_scalar_vector(duration_wt, f3)
            feature_vector = add_lists(weighted_f1, weighted_f2, weighted_f3)
            save(feature_vector)
        except:
            print "error"


combine_vectors(0.2, 0.4, 0.4)

