"""
In this file it is defined the function to perform a roulette wheel selection.
    
Functions: 
    roulette_selection: Given a list with the tuples (id_individual, normalized_fitness), this function calculates the a roulette wheel selection based in the normalized fitness.
"""
import random


def roulette_selection(population, minimize, num_selected_ind):
    """
    此函數返回由輪盤賭選擇法選出的個體的ID列表。注意，在調用此函數之前必須計算人口的標準化適應度（調用方法 Gavl._Population__calculate_normalized_fitness）。

    :param population: (list of Individuals) 這是個體列表（見個體類）。
    :param minimize: (int) 整數，表示目標是最小化適應度（minimize = 1）還是最大化適應度（minimize = 0）。
    :param num_selected_ind: (int) 要選擇的個體數量。
    :return:
        * :list_selected_individuals: (list of str) 包含選中個體ID的列表。注意，可能會有重複的個體。
    """
    if minimize:
        # 如果是最小化適應度，使用個體的反向標準化適應度
        list_ids_normalizedfitness = [(ind._id, ind.inverse_normalized_fitness_value) for ind in population]
    else:
        # 如果是最大化適應度，使用個體的標準化適應度
        list_ids_normalizedfitness = [(ind._id, ind.normalized_fitness_value) for ind in population]

    list_selected_individuals = []  # 將包含選中個體ID的列表。
    sum_fit = sum(map(lambda x: x[1], list_ids_normalizedfitness))  # 所有個體的（反向）標準化適應度之和

    for _ in range(num_selected_ind):
        population_cumulative_fitness = 0  # 人口累積適應度
        selected_cumulative_fitness = random.random() * sum_fit  # 隨機選擇的個體的累積適應度閾值
        for ind in list_ids_normalizedfitness:
            population_cumulative_fitness += ind[1]  # 累加適應度
            if selected_cumulative_fitness <= population_cumulative_fitness:
                list_selected_individuals.append(ind[0])  # 添加個體的ID到列表中
                break
    return list_selected_individuals  # 返回選中的個體ID列表
