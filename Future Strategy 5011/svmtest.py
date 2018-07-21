# _*_ coding:utf-8 _*_
from sklearn import svm
from helperFunctions import generate_data_helper, compute_average, get_past_data
import  numpy as np
import os
from sklearn.externals import joblib

# 每隔多少分钟做一次检测
time_span = 45 # how long to perform an analysis and transaction

# 本金比例
cost_rate = 0.003
weight_index = [1.2, 1.0, 0.6]

#13个对象的标数
asset_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# 交易下限
my_cash_balance_lower_limit = 4000000. # Cutting-loss criterion

#  memory.counter - 1 = timer
def handle_bar(timer, data, info, init_cash, transaction, detail_last_min, memory):

    element_array = ["A.DCE", "AG.SHF", "AU.SHF", "I.DCE", "IC.CFE", "IF.CFE", "IH.CFE",
                     "J.DCE", "JM.DCE", "M.DCE", "RB.SHF", "Y.DCE", "ZC.CZC"]

    # Get position of last minute
    # Size 13x1
    position_new = detail_last_min[0]  # latest position matrix

    # Initialize
    if timer == 0:
       memory.totalCounter = 0
       memory.spanCounter = 0  

       memory.bufferLabel = list()
       memory.bufferLabel.append(0)

       memory.bar_counter = 0
       memory.data_list = list() # whole dataset from the start to the end
       memory.flagSVM = []

       memory.flagBuy = 0
       memory.flagSell = 0

    memory.data_list.append(data)
    memory.totalCounter += 1
    memory.spanCounter += 1
    
    # Do the analysis here
    if memory.spanCounter % time_span == 0 and memory.spanCounter != 0 and detail_last_min[1] > my_cash_balance_lower_limit:
        #path = 'svmmodel.pkl'
        #clf = joblib.load(path)   #把训练好的模型加载进来
        result = []
        for i in range(len(asset_index)):  #对每个对象做处理
            path = 'svmmodel' + str(i) + '.pkl'
            clf = joblib.load(path)
            data1 = generate_data_helper(memory.data_list, asset_index[i]) #列：开高低收
            current_close = data[asset_index[i], 3]
            current_open = data[asset_index[i], 0]
            current_average_sum = compute_average(data)
            current_average = current_average_sum[asset_index[i]]

            # 利用均价，开盘价，收盘价作为特征
            train_input = np.array([current_average, current_close, current_open]).reshape(1, 3)

            # 预测每只商品上涨的概率， 并且存入result里面
            prob = clf.predict_proba(train_input)
            prob = np.squeeze(prob)
            result.append(prob[1]) #prob[1]是预测结果取1的概率
            if i == 12:
                print(result)

        # 得到所有的预测概率结果
        result = np.asarray(result)

        # 得到上涨概率最高的3个商品，并且存入序号，从大到小
        #argsort：从小到大的索引值，-3是取最后三位，-1是倒序变成从大到小
        raise_target = result.argsort()[-3:][::-1]
        raise_target = raise_target.ravel()
        result.tolist()

        # 计算此分钟数据每个商品的均值
        current_average_sum = compute_average(data)

        count1 = 0

        for i in raise_target:
            print(i)
            if(result[i] >= 0.5): # 买入的概率阀值
                current_average_target = current_average_sum[i]
                lot_value = current_average_target * info.unit_per_lot[i] * info.margin_rate[i]
                num_lot = np.round(cost_rate * weight_index[count1] * init_cash / (lot_value * (1. + transaction)))
                #num_lot = np.round(cost_rate * result[i] * weight_index[count1] * init_cash / (lot_value * (1. + transaction)))
                position_new[i] += num_lot

                if count1 == 2:
                   break
                count1 += 1

        #最有可能下降的三个商品
        down_target = result.argsort()[:3]
        for j in down_target:
            if result[i] < 0.3: # 卖出的概率阀值
               current_average_target = current_average_sum[j]
               position_new[j] -= 5

    # Reset
    memory.flagBuy = 0
    memory.flagSell = 0

    return position_new, memory

if __name__ == '__main__':
    ''' This strategy simply check if there is any special technical pattern in data
        No training process required. Main function is passed.
    '''
    pass