import os

feature_dict = {
    '车号': {

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


def data_word2num(data_list):
    res = []

    for feature, map_key in zip(data_list, feature_dict):
        feature_map = feature_dict[map_key]
        if feature_map and (feature in feature_map):
            feature = feature_map[feature]
        else:
            feature = [eval(feature)]

        res += feature

    return res


def csv2list(csv_path):
    res = []

    print(csv_path)
    with open(csv_path) as f:
        feature_list = f.readline()
        for data_line in f:
            data_split = data_line.split(',')
            # 空数据
            if not data_split[2]:
                continue
            # data_split.pop(1)
            data_split[-1] = data_split[-1][:-1]

            res.append(data_split)

    return res


if __name__ == '__main__':
    train_labels_path = '../data/train_labels.csv'
    print(csv2list(train_labels_path))

    usage = 'train'

    dir_path = '../data/{}/'.format(usage)
    csv_list = os.listdir(dir_path)

    for csv_name in csv_list[:2]:
        data_list = csv2list(dir_path + csv_name)
        data_list = list(map(lambda x: x[:1] + x[2:], data_list))
        for d in data_list:
            data_word2num(d)
