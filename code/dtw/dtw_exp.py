import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import math
import random


def euclid_dist(t1,t2):
    return math.sqrt(sum((t1-t2)**2))


def DTWDistance(s1, s2):
    DTW={}

    for i in range(len(s1)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(s2)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            dist= (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])

    return math.sqrt(DTW[len(s1)-1, len(s2)-1])


# def DTWDistance(s1, s2, w):
#     DTW={}
#
#     w = max(w, abs(len(s1)-len(s2)))
#
#     for i in range(-1,len(s1)):
#         for j in range(-1,len(s2)):
#             DTW[(i, j)] = float('inf')
#     DTW[(-1, -1)] = 0
#
#     for i in range(len(s1)):
#         for j in range(max(0, i-w), min(len(s2), i+w)):
#             dist= (s1[i]-s2[j])**2
#             DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])
#
#     return math.sqrt(DTW[len(s1)-1, len(s2)-1])


def LB_Keogh(s1,s2,r):
    LB_sum=0
    for ind,i in enumerate(s1):

        lower_bound=min(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        upper_bound=max(s2[(ind-r if ind-r>=0 else 0):(ind+r)])

        if i>upper_bound:
            LB_sum=LB_sum+(i-upper_bound)**2
        elif i<lower_bound:
            LB_sum=LB_sum+(i-lower_bound)**2

    return math.sqrt(LB_sum)


def k_means_clust(data, num_clust, num_iter, w=5):
    centroids=random.sample(data, num_clust)
    # print centroids
    counter=0
    for n in range(num_iter):
        counter += 1
        print counter
        assignments = {}
        #assign data points to clusters
        for ind,i in enumerate(data):
            # print ind, i
            min_dist = float('inf')
            closest_clust = None
            for c_ind,j in enumerate(centroids):
                if LB_Keogh(i, j, 5) < min_dist:
                    cur_dist = DTWDistance(i, j)
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        closest_clust = c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust] = [ind]

        #recalculate centroids of clusters
        # print assignments
        # for key in assignments:
        #     print key, assignments[key]
        # print "\n\n\n"

        for key in assignments:
            clust_sum = 0
            for k in assignments[key]:
                # print data[k]
                clust_sum = clust_sum+data[k]
            # print clust_sum
            centroids[key] = [m/len(assignments[key]) for m in clust_sum]

    # for key in assignments:
        # print key, assignments[key]

    return centroids, assignments


def cluster(num_clust, num_iter, w=5):
    feature, duration, mmtoc, phrasecloud = read_data()
    data = [item[2:] for item in feature]
    centroids, assignments = k_means_clust(data, num_clust, num_iter, w)

    distribution = {}

    for key in assignments:
        distribution[key] = {}
        # print key, assignments[key]
        for user in assignments[key]:
            if feature[user][1] in distribution[key]:
                distribution[key][int(feature[user][1])] += 1
            else:
                distribution[key][int(feature[user][1])] = 1

    for key in distribution:
        print "cluster id ", key
        for category in distribution[key]:
            print category, distribution[key][category]
        print "\n\n"

    for key in assignments:
        for i in assignments[key]:
            plt.title('No of user: %.2f' % (len(assignments[key])))
            plt.plot(feature[i][2:])
        plt.savefig("./cluster_visualization/feature_" + str(key) + ".png")
        plt.clf()

        for i in assignments[key]:
            plt.title('No of user: %.2f' % (len(assignments[key])))
            plt.plot(duration[i][2:])
        plt.savefig("./cluster_visualization/duration_" + str(key) + ".png")
        plt.clf()

        for i in assignments[key]:
            plt.title('No of user: %.2f' % (len(assignments[key])))
            plt.plot(mmtoc[i][2:])
        plt.savefig("./cluster_visualization/mmtoc_" + str(key) + ".png")
        plt.clf()

        for i in assignments[key]:
            plt.title('No of user: %.2f' % (len(assignments[key])))
            plt.plot(phrasecloud[i][2:])
        plt.savefig("./cluster_visualization/phrasecloud_" + str(key) + ".png")
        plt.clf()

    for i in centroids:
        plt.plot(i)

    plt.savefig("cluster_centroid.png")
    # plt.show()
    plt.clf()


def read_data():
    feature = []
    temp = np.genfromtxt('feature_vectors.csv', delimiter=',')
    for value in temp:
        feature.append(value)

    duration = []
    temp = np.genfromtxt('duration_vectors.csv', delimiter=',')
    for value in temp:
        duration.append(value)

    mmtoc = []
    temp = np.genfromtxt('mmtoc_vectors.csv', delimiter=',')
    for value in temp:
        mmtoc.append(value)

    phrasecloud = []
    temp = np.genfromtxt('phrasecloud_vectors.csv', delimiter=',')
    for value in temp:
        phrasecloud.append(value)

    return feature, duration, mmtoc, phrasecloud

    # cluster(feature, duration, mmtoc, phrasecloud, 3, 5, 3)

# read_data()
cluster(4, 500, 3)