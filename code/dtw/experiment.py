from dtw import dtw
import matplotlib.pyplot as plt
import numpy as np

x = np.array([18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]).reshape(-1, 1)

y1 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6200579929945306, 0.6438632501087107, 0.0, 0.0,
               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]).reshape(-1, 1)

y2 = np.array([0.0, 0.0, 0.0, 0.0, 0.49130419087139987, 0.2515370286958988, 0.32048017049845784,
     0.4208220476684349, 0.45271634796775506, 0.523880610864608, 0.3701577102264382,
     0.4075776421848937, 9.372698899424437e-05, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.35688195163750286, 0.0]).reshape(-1, 1)

# plt.plot(x, y1)
# plt.plot(x, y2)
# plt.show()


dist, cost, acc, path = dtw(y1, y2, dist=lambda x, y: np.linalg.norm(x - y))

plt.imshow(cost.T, origin='lower', cmap=plt.cm.gray, interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.xlim((-0.5, cost.shape[0]-0.5))
plt.ylim((-0.5, cost.shape[1]-0.5))
# print dist
plt.savefig('test.png')
# # print cost
# # print acc
# print path



