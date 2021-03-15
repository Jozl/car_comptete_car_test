def slice_data(data_list, l, i):
    """

    :param data_list: 数据列表，一行一条
    :param l:每个切片长度
    :param i:关键一点那一条的index
    :return:切片列表
    """
    res = []

    half_l = l // 2
    l = half_l * 2

    left = i
    right = len(data_list) - i

    s = 0
    if left > half_l and right > half_l:
        s = (i - half_l) % l

    data_list = data_list[s:]

    for i in range(0, len(data_list), l):
        res.append(data_list[i:i + l])

    if len(res[-1]) < l:
        res.pop(-1)

    return res, i//l - 1


if __name__ == '__main__':
    data_list = []
    for i in range(1000):
        data_list.append(i)
    print(data_list)

    data = slice_data(data_list, 100, 20)
    print(data)
