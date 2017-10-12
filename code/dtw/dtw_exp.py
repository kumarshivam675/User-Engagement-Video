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


def DTWDistance(s1, s2, w):
    DTW={}

    w = max(w, abs(len(s1)-len(s2)))

    for i in range(-1,len(s1)):
        for j in range(-1,len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(max(0, i-w), min(len(s2), i+w)):
            dist= (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])

    return math.sqrt(DTW[len(s1)-1, len(s2)-1])


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
            min_dist = float('inf')
            closest_clust = None
            for c_ind,j in enumerate(centroids):
                if LB_Keogh(i, j, 5) < min_dist:
                    cur_dist = DTWDistance(i, j, w)
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        closest_clust = c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust] = []

        #recalculate centroids of clusters
        # print assignments
        for key in assignments:
            clust_sum = 0
            for k in assignments[key]:
                # print data[k]
                clust_sum = clust_sum+data[k]
            # print clust_sum
            centroids[key] = [m/len(assignments[key]) for m in clust_sum]

    print assignments
    for key in assignments:
        for i in assignments[key]:
            plt.plot(data[i])
        plt.savefig("cluster_" + str(key) + ".png")
        # plt.show()
        plt.clf()

    return centroids


# x = np.array([18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]).reshape(-1, 1)
#
# y1 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6200579929945306, 0.6438632501087107, 0.0, 0.0,
#                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]).reshape(1, 20)
#
# y2 = np.array([0.0, 0.0, 0.0, 0.0, 0.49130419087139987, 0.2515370286958988, 0.32048017049845784,
#      0.4208220476684349, 0.45271634796775506, 0.523880610864608, 0.3701577102264382,
#      0.4075776421848937, 9.372698899424437e-05, 0.0, 0.0, 0.0, 0.0, 0.0,
#               0.35688195163750286, 0.0]).reshape(1, 20)


# train = np.genfromtxt('train.csv', delimiter='\t')
# print train.shape
# test = np.genfromtxt('test.csv', delimiter='\t')
# data = np.vstack((train[:, :-1], test[:, :-1]))
# centroids=k_means_clust(data, 4, 4, 5)

# print data.shape
# data = np.vstack((y1, y2))
# print y1.shape
# print y2.shape
# print data.shape

data = np.genfromtxt('feature_vectors.csv', delimiter=',')
# print data
centroids = k_means_clust(data, 7, 20, 3)
print centroids

for i in centroids:
    plt.plot(i)
plt.savefig("cluster_centroid.png")
# plt.show()
plt.clf()
