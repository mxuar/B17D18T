# -*- coding:UTF-8 -*-
from sklearn import svm
from sklearn.externals import joblib
from helperFunctions import read_h5, addLabel, compute_average
import talib as tb
import h5py
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing

#initialize the index parameters
kd_low = 10
kd_high = 90
fastk_period = 9
slowk_period = 3
slowd_period = 3

#data path & data information path
path_data= './Future Strategy 5011/Data/data_format1_20170717_20170915.h5'
path_info= './Future Strategy 5011/Data/information.csv'

#13 futures
indexes = ['A.DCE', 'AG.SHF', 'AU.SHF', 'I.DCE', 'IC.CFE', 'IF.CFE',
           'IH.CFE', 'J.DCE', 'JM.DCE', 'M.DCE', 'RB.SHF', 'Y.DCE', 'ZC.CZC']
target_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

dict = read_h5(path_data)

flagBuy = 0
flagSell = 0

for i in target_index:
    keyData = dict[indexes[i]].values[:, 0:4]

    train_label = list()
    train_label.append(0)

    # For the average
    average_label = list()
    average_label.append(0)
    average_target = compute_average(keyData).reshape(-1, 1)
    #reshape: 变成行数未知，列只有一列的状态
    average_label += addLabel(average_target)
    #addLabel: 当当前数比下一个数小则为1，反之为0

    # For the close
    close_label = list()
    close_label.append(0)
    close_target = keyData[:, 3].reshape(-1, 1)
    #将close里的值都跳出来，变成一列的状态
    close_label += addLabel(close_target)


    # For the open
    open_label = list()
    open_label.append(0)
    open_target = keyData[:, 0].reshape(-1, 1)
    open_label += addLabel(open_target)

    # Train label
    train_label = list()

    for j in range(len(average_label)):
        if average_label[j] == close_label[j] == open_label[j]:
           train_label.append(1)
        else:
           train_label.append(0)



# C1 -- average, C2 -- close
    train_input = np.concatenate((average_target, close_target, open_target), axis=1).reshape(len(average_target), 3)
#concatenate：将多个数组进行拼接
#axis=1表示对应行的数组进行拼接
    train_label = np.asarray(train_label)

# SVM/LR
    #clf = LogisticRegression(C = 1.0,penalty = 'l2')
    clf = svm.SVC(probability=True,kernel='linear')
    #‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ 
    train_input = preprocessing.scale(train_input)
    clf.fit(train_input, train_label)
    print("Model being stored....")

    joblib.dump(clf, 'svmmodel' + str(i) + '.pkl')
#在模型持久化过程中，使用scikit-learn提供的joblib.dump()
#joblib更适合大数据量的模型，且只能往硬盘存储，不能往字符串存储

