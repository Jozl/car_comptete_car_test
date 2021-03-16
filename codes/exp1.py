import os
import glob
import pandas as pd
import numpy as np
import torch
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier
from torch import nn, optim, Tensor
from torch.autograd import Variable

from codes.data import data_word2num
from codes.utils.data import slice_data

train_labels = '../data/train_labels.csv'
train_labels_df = pd.read_csv(train_labels)

train_files = glob.glob('../data/train/*.csv')
train_files.sort(key=lambda x: int(x.split('/')[-1].split('.')[0]))

test_files = glob.glob('../data/test/*.csv')
train_files.sort(key=lambda x: int(x.split('/')[-1].split('.')[0]))

collect_time_list = []
train_data_list = []
test_data_list = []
label_list = []

test_no_collect_time_list = []

ch_map = {}
ch_count = 0

slice_len = 1000

training_files = train_files[:]
print('training set:\n')
for train_file in training_files:
    print(train_file)
    train_df = pd.read_csv(train_file).dropna()

    collect_time = train_labels_df[
        train_labels_df['车号'] == train_df['车号'].values[0]
        ]['CollectTime'].values[0]

    label = train_labels_df[
        train_labels_df['车号'] == train_df['车号'].values[0]
        ]['Label'].values[0]

    if label == 0:
        positive_index = 0
    else:
        positive_index = train_df[
            train_df['采集时间'] == collect_time
            ].index
        positive_index = positive_index.values[0]

        index_list = train_df.index.tolist()
        # print(index_list)
        positive_index = index_list.index(positive_index)

    train_list = train_df.values.tolist()
    train_list = list(map(lambda x: data_word2num(x), train_list))
    train_list = list(map(lambda x: x[2:], train_list))

    data_list, label_i = slice_data(train_list, slice_len, positive_index)
    # labels = [0] * len(data_list) * len(data_list[0])
    labels = [0] * len(data_list)
    if label == 1:
        labels[label_i] = 1
        # labels[positive_index] = 1

    for data in data_list:
        train_data_list.append(np.array(data).var(axis=0))

    label_list += labels
    # ch_map[ch_count] = len(data_list)
    # ch_count += 1

# test_files = train_files[-10:]
print('testing set:\n')
for test_file in test_files:
    print(test_file)
    test_df = pd.read_csv(test_file).dropna()

    test_list = test_df.values.tolist()
    test_list = list(map(lambda x: data_word2num(x), test_list))
    # test_list = list(map(lambda x: x[2:], test_list))

    data_list, _ = slice_data(test_list, slice_len, 0)

    for data in data_list:
        test_no_collect_time_list.append(list(map(lambda x: x[:2], data))[0])

        data = list(map(lambda x: x[2:], data))
        test_data_list.append(np.array(data).var(axis=0))

    ch_map[ch_count] = len(data_list)
    ch_count += 1

clf = svm.SVC(kernel='linear')
# clf = svm.SVC()
clf = AdaBoostClassifier()

clf.fit(train_data_list, label_list)

print('fit完了')

# predict = clf.predict(train_data_list)
predict = clf.predict(test_data_list)

print(label_list.count(1))
print(predict.tolist().count(1))

print('acc', np.sum([1 if o == p == 1 else 0 for o, p in zip(label_list, predict)]) / label_list.count(1))

# print(test_no_collect_time_list)

for i, p in enumerate(predict):
    if p == 1:
        # print(train_no_collect_time_list[i])
        print('time:', test_no_collect_time_list[i])
        for k, v in ch_map.items():
            if i <= v:
                break
            i -= v
        file_no = k
        print(test_files[file_no])

# print('实际上')
#
# for i, p in enumerate(label_list):
#     if p == 1:
#         for k, v in ch_map.items():
#             if i < v:
#                 line_no = i
#                 break
#             i -= v
#         file_no = k
#         print(train_files[file_no])
