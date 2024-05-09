"""
In this file it is defined the auxiliary function to get all the combinations of some length of the elements of a list. It is exactly like the tool itertools.combinations, but, as said below, itertools goes prrr (just wanted to define this function in a recurrent and dynamic programming manner).

Function:
    combinations: function that returns the combinations of some length of the elements in a list.
"""


def combinations(list_get_comb, length_combination):
    """
    生成器，用來獲取列表元素的所有特定長度的組合。

    :param list_get_comb: (list) 想要獲取元素組合的列表。
    :param length_combination: (int) 元素組合的長度。
    :return:
        * :generator: 此列表的組合的生成器。
    """
    # 檢查輸入參數是否正確
    if not isinstance(list_get_comb, list):
        raise TypeError("參數 'list_get_comb' 必須是列表。")
    if not isinstance(length_combination, int):
        raise TypeError("參數 'length_combination' 必須是一個正整數，且小於給定列表的長度。")
    if length_combination <= 0 or length_combination > len(list_get_comb):
        raise ValueError("參數 'length_combination' 必須是一個正整數，且小於給定列表的長度。")

    # 內部生成器，用來獲取列表索引的組合
    def get_indices_combinations(sub_list_indices, max_index):
        """
        生成器，返回索引的組合

        :param sub_list_indices: (list) 生成所有可能組合的子列表。
        :param max_index: (int) 最大索引。
        :return:
        """
        if len(sub_list_indices) == 1:  # 列表索引的最後一個元素
            for index in range(sub_list_indices[0], max_index + 1):
                yield [index]
        elif all([sub_list_indices[-i - 1] == max_index - i for i in range(len(sub_list_indices))]):  # 當前子列表已到達終點
            yield sub_list_indices
        else:
            # 獲取子列表 sub_list_indices[1:] 的所有可能組合
            for comb in get_indices_combinations(sub_list_indices[1:], max_index):
                yield [sub_list_indices[0]] + comb
            # 前進一個位置，檢查所有可能的組合
            new_sub_list = [sub_list_indices[0] + i + 1 for i in range(len(sub_list_indices))]
            for new_comb in get_indices_combinations(new_sub_list, max_index):
                yield new_comb  # 返回新列表的所有可能組合

    # 啟動演算法：
    ini_list_indices = list(range(length_combination))  # 初始化列表索引
    for list_indices in get_indices_combinations(ini_list_indices, len(list_get_comb) - 1):
        yield [list_get_comb[i] for i in list_indices]  # 根據索引返回列表中的元素組合
