"""
In this file it is defined the function to perform random pairing given a selection (like the one given by roulette wheel).
    
Functions: 
    pairing: Given a selection (list with IDs), it performs a pairing of individuals.
"""
import random


def pairing(list_selected_ind):
    """
    這個函數執行隨機配對。注意，這個函數接受重複，且元素可能與自己配對。
    這種情況雖然很少發生，但可以作為精英過程使用。

    :param list_selected_ind: 包含被選中個體ID的列表。這是函數 roulette_selection 的輸出。
    :return:
        * :paired_ind: 包含配對個體ID的元組列表。
    """
    list_sel = list_selected_ind.copy()  # 複製輸入列表以避免修改原始數據
    if len(list_sel) % 2 == 1:  # 檢查列表長度是否為奇數
        list_sel.pop()  # 如果是奇數，移除列表中的最後一個元素
    random.shuffle(list_sel)  # 對列表進行隨機排序
    paired_ind = []  # 初始化配對列表
    while len(list_sel) > 0:  # 當列表中還有元素時，繼續配對過程
        # 從列表中移除最後兩個元素並將它們作為一對添加到配對列表中
        paired_ind.append((list_sel.pop(), list_sel.pop()))
    return paired_ind  # 返回配對列表
