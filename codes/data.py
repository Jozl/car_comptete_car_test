import os
import datetime

import pandas as pd

feature_dict = {
    '车号': {

    }, '采集时间': {
        '': [0]
    }, '加速踏板位置': {
        '': [0]
    }, '电池包主负继电器状态': {
        '断开': [0, 1],
        '连接': [1, 0],
    }, '电池包主正继电器状态': {
        '断开': [0, 1],
        '连接': [1, 0],
    }, '制动踏板状态': {
        '未踩': [0, 1],
        '踩下': [1, 0],
    }, '驾驶员离开提示': {
        'No Warning': [0, 1],
        'Warning(下车时请拔掉钥匙)': [1, 0],
    }, '主驾驶座占用状态': {
        '空置': [0, 0, 1],
        '有人': [0, 1, 0],
        '传感器故障': [1, 0, 0],
    }, '驾驶员安全带状态': {
        '未系': [0, 1],
        '已系': [1, 0],
    }, '驾驶员需求扭矩值': {
        '': [0]
    }, '手刹状态': {
        '手刹放下': [0, 0, 1],
        '手刹拉起': [0, 1, 0],
        '': [1, 0, 0]
    }, '整车钥匙状态': {
        'OFF': [0, 0, 0, 1],
        'ON': [0, 0, 1, 0],
        'ACC': [0, 1, 0, 0],
        '': [1, 0, 0, 0]
    }, '低压蓄电池电压': {
        '': [0]
    }, '整车当前档位状态': {
        '空档': [0, 0, 0, 0, 1],
        '前进': [0, 0, 0, 1, 0],
        '后退': [0, 0, 1, 0, 0],
        '驻车': [0, 1, 0, 0, 0],
        '': [1, 0, 0, 0, 0]
    }, '整车当前总电流': {
        '': [0]
    }, '整车当前总电压': {
        '': [0]
    }, '车辆行驶里程': {
        '': [0]
    }, '车速': {
        '': [0]
    }, '方向盘转角': {
        '': [0]
    }
}


# 字符串转时间戳
def str2ts(s):
    ts = (datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')).timestamp()
    return ts


# 时间戳转字符串
def ts2str(ts):
    t = datetime.datetime.fromtimestamp(ts)
    s = datetime.datetime.strftime(t, '%Y-%m-%d %H:%M:%S')
    return s


def data_word2num(data_list):
    res = []

    for feature, map_key in zip(data_list, feature_dict):
        feature_map = feature_dict[map_key]
        if feature_map and (feature in feature_map):
            feature = feature_map[feature]
        else:
            # feature = [eval(feature) if map_key != '采集时间' else feature]
            feature = [feature]
        res += feature

    return res


if __name__ == '__main__':

    r = data_word2num([1, '2020-08-28 06:33:14', 0.0, '断开', '断开', '未踩', 'No Warning', '空置', '未系', 0.0, '手刹拉起', 'OFF', 12.43, '空档', 0.0, 123.2, 7662.0, 0.0, 0.0])
    print(r)
    # train_labels_path = '../data/train_labels.csv'
    # df = pd.read_csv(train_labels_path)
    #
    #
    # train_path = '../data/train/'
    # train_csv_list = os.listdir(train_path)
    #
    # data_train = {}
    # for csv_name in train_csv_list[:1]:
    #     print(csv2list(train_path + csv_name)[0])
    #     train_list = list(map(
    #         lambda x: data_word2num(x),
    #         list(map(
    #             lambda x: x[:1] + [str2ts(x[1])] + x[2:],
    #             csv2list(train_path + csv_name)))))
    #
    #     data_train[train_list[0][0]] = train_list
    #
    # print(data_train.keys())
