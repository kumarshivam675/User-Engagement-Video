import sys
import csv
from config import project_folder
import extract_ground_truth
import numpy as np

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


def save(email, user_cluster, data, filename):
    try:
        data.insert(0, user_cluster[email])
        data.insert(0, email) #insert email id in the beginning
        details = [data]
        with open(filename, 'a') as testfile:  # append it data to the csv file
            csv_writer = csv.writer(testfile)
            csv_writer.writerow(details[0])
    except:
        print "key error", email


def create_vectors():
    mmtoc_dict = mmtoc.extract_mmtoc_clicks()
    phrasecloud_dict = phrasecloud.extract_phrasecloud_clicks()
    duration_dict = duration_ver3.create_video_log()
    user_cluster = extract_ground_truth.ground_truth()
    count = 0

    # print len(mmtoc_dict), len(phrasecloud_dict), len(duration_dict), len(user_cluster)

    vector = []
    target = []
    for user in phrasecloud_dict:
        if user in user_cluster:
            count += 1
            print count
            mmtoc_vector = extract_vectors(mmtoc_dict[user])
            phrasecloud_vector = extract_vectors(phrasecloud_dict[user])
            duration_vector = extract_vectors(duration_dict[user])

            user_vector = []
            for i in range(0, len(mmtoc_vector)):
                feature = [mmtoc_vector[i], phrasecloud_vector[i], duration_vector[i]]
                user_vector.append(feature)

            # print "len of vector is ", len(user_vector)

            vector.append(user_vector)
            target.append(user_cluster[user])

    seq_len = [len(feature)]*len(target)
    np.savez("train.npz", np.array(vector[:500]), np.array(target[:500]), np.array(seq_len[:500]))
    np.savez("test.npz", np.array(vector[500:]), np.array(target[500:]), np.array(seq_len[500:]))
    return vector, target, seq_len

create_vectors()

