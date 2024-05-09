"""
In this file it is defined the functions to check the termination criteria.
    
Functions:
    max_num_generation_reached: Function that checks if the max number of generations is reached.
    goal_fitness_reached: Function that checks if the goal fitness is reached.
    check_termination_criteria: This function selects the termination criteria
"""


def max_num_generation_reached(generation_count, max_generations):
    """
    這個函數判斷是否達到了最大世代數。
    
    :param generation_count: (int) 當前的世代數。
    :param max_generations: (int) 最大世代數。
    :return:
        (bool) 如果達到最大世代數，則返回 True。
    """
    return generation_count >= max_generations  # 判斷當前世代數是否大於或等於最大世代數。


def goal_fitness_reached(generation_best_fitness, goal_fitness, minimize):
    """
    這個函數判斷是否達到了目標適應度。
    
    :param generation_best_fitness: (int) 當前世代最佳適應度。
    :param goal_fitness: (int) 目標適應度。
    :param minimize: (bool) 如果為1，則目標是最小化適應度函數；反之則是最大化。
    :return:
        (bool) 如果達到目標適應度，則返回 True。
    """
    if minimize:  # 如果目標是最小化適應度
        return generation_best_fitness <= goal_fitness  # 檢查是否達到或低於目標適應度
    else:  # 如果目標是最大化適應度
        return generation_best_fitness >= goal_fitness  # 檢查是否達到或超過目標適應度


def check_termination_criteria(termination_criteria_args):
    """
    這個函數檢查終止條件。
    
    :param termination_criteria_args: (dictionary) 這是一個包含檢查終止條件所需參數的字典。它可以包含以下值：
        * {'termination_criteria': 'goal_fitness_reached', 'goal_fitness': _ , 'generation_fitness': _ , 'minimize': _ }
        * {'termination_criteria': 'max_num_generation_reached', 'generation_goal': _ , 'generation_count': _ }
    :return:
        (bool) 如果滿足終止條件，則返回 True。否則返回 False。
    """
    termination_criteria = termination_criteria_args['termination_criteria']  # 獲取終止條件類型
    if termination_criteria == 'max_num_generation_reached':  # 如果終止條件為達到最大世代數
        generation_count = termination_criteria_args['generation_count']  # 獲取當前世代數
        max_generations = termination_criteria_args['generation_goal']  # 獲取最大世代數
        return max_num_generation_reached(generation_count, max_generations)  # 調用函數檢查是否達到最大世代數
    elif termination_criteria == 'goal_fitness_reached':  # 如果終止條件為達到目標適應度
        generation_best_fitness = termination_criteria_args['generation_fitness']  # 獲取當前世代最佳適應度
        goal_fitness = termination_criteria_args['goal_fitness']  # 獲取目標適應度
        minimize = termination_criteria_args['minimize']  # 獲取是否最小化
        return goal_fitness_reached(generation_best_fitness, goal_fitness, minimize)  # 調用函數檢查是否達到目標適應度
    else:
        raise ValueError("終止條件必須是 'max_num_generation_reached' 或 'goal_fitness_reached'。")  # 如果終止條件不合法，拋出異常
