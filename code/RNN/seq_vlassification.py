# Working example for my blog post at:
# http://danijar.com/variable-sequence-lengths-in-tensorflow/
import functools
import sets
import tensorflow as tf
import numpy as np
import random
import os

batch_size = 1
num_classes = 3
input_size = 3


def lazy_property(function):
    attribute = '_' + function.__name__
    @property
    @functools.wraps(function)
    def wrapper(self):
        if not hasattr(self, attribute):
            setattr(self, attribute, function(self))
        return getattr(self, attribute)
    return wrapper

def get_on_hot(number):
    on_hot = [0] * 3
    on_hot[number] = 1
    return on_hot

def data_train_prep():
    train = np.load('/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/combine_features/train.npz')
    feature = train['arr_0'].tolist()
    label = train['arr_1'].tolist()
    labels = map(get_on_hot, label)
    seq_len = train['arr_2'].tolist()
    c = list(zip(feature, labels, seq_len))
    random.shuffle(c)
    feature, labels, seq_len = zip(*c)
    print len(feature), len(labels), len(seq_len)
    return feature, labels, seq_len


def data_test_prep():
    test = np.load('/home/trisha/Desktop/Acad/Semester9/PE/User-Engagement-Video/code/combine_features/test.npz')
    tfeature = test['arr_0'].tolist()
    tlabel = test['arr_1'].tolist()
    tlabels = map(get_on_hot, tlabel)
    tseq_len = test['arr_2'].tolist()
    c = list(zip(tfeature, tlabels, tseq_len))
    random.shuffle(c)
    tfeature, tlabels, tseq_len = zip(*c)
    return tfeature, tlabels, tseq_len


class VariableSequenceLabelling:
    def __init__(self, data, target, length, num_hidden=500, num_layers=1):
        print data.get_shape()
        self.data = data
        self.target = target
        self.seqlen = length
        self._num_hidden = num_hidden
        self._num_layers = num_layers
        self.prediction
        self.error
        self.optimize

    @lazy_property
    def prediction(self):
        # Recurrent network.
        output, _ = tf.nn.dynamic_rnn(
            tf.contrib.rnn.BasicLSTMCell(self._num_hidden),
            self.data,
            dtype=tf.float32,
            sequence_length=self.seqlen,
        )
        # Softmax layer.
        max_length = self.seqlen
        weight, bias = self._weight_and_bias(self._num_hidden, num_classes)
        # Flatten to apply same weights to all time steps.
        output = tf.reshape(output, [-1, self._num_hidden])
        prediction = tf.nn.softmax(tf.matmul(output, weight) + bias)
        prediction = tf.reshape(prediction, [-1, max_length, num_classes], name='prediction')
        return prediction

    @lazy_property
    def cost(self):
        # Compute cross entropy for each frame.
        cross_entropy = self.target * tf.log(self.prediction)
        cross_entropy = -tf.reduce_sum(cross_entropy, reduction_indices=2, name='aaa')
        # Average over actual sequence lengths.
        cross_entropy = tf.reduce_sum(cross_entropy, reduction_indices=1)
        cross_entropy /= tf.cast(self.seqlen, tf.float32)
        return tf.reduce_mean(cross_entropy)

    @lazy_property
    def optimize(self):
        learning_rate = 0.01
        optimizer = tf.train.AdamOptimizer(learning_rate)
        return optimizer.minimize(self.cost)

    @lazy_property
    def error(self):
        mistakes = tf.not_equal(
            tf.argmax(self.target[:, -1], 1), tf.argmax(self.prediction[:, -1], 1), name='mistakes1')
        return tf.reduce_mean(tf.cast(mistakes, tf.float32), name='mistakes1')

    @staticmethod
    def _weight_and_bias(in_size, out_size):
        weight = tf.truncated_normal([in_size, out_size], stddev=0.01)
        bias = tf.constant(0.1, shape=[out_size])
        return tf.Variable(weight), tf.Variable(bias)


feature, labels, seq_len = data_train_prep()
tfeature, tlabels, tseq_len = data_test_prep()
print "Data Preparation Over :)"

data = tf.placeholder(tf.float32, shape=[None, None, input_size], name='inputs')
target = tf.placeholder(tf.float32, shape=[None, None, num_classes], name='outputs')
seqlen = tf.placeholder(tf.int32)
model = VariableSequenceLabelling(data, target, seqlen)
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
print "Model Initialisation Successful :)"

for epoch in range(100):
    start = 0
    end = 1
    start1 = 0
    end1 = 1
    error = 0

    print "Epoch: ", epoch
    for i in range(len(feature)):
        X = feature[start:end]
        Y = labels[start:end]
        L = len(X[0])
        temp = []
        for i in range(len(Y)):
            temp.append(np.array([Y[i]] * L))
        start = end
        end = start + 1
        sess.run(model.optimize, {data: X, target: temp, seqlen: L})
    for i in range(len(tfeature)):
        X = tfeature[start1:end1]
        Y = tlabels[start1:end1]
        L = len(X[0])
        temp = []
        for i in range(len(Y)):
            temp.append(np.array([Y[i]] * L))
        start1 = end1
        end1 = start1 + 1
        error += sess.run(model.error, {data: X, target: temp, seqlen: L})
    print("Error: ", error)
    print('Epoch {:2d} error {:3.1f}%'.format(epoch, ((error) *100) / 194))



