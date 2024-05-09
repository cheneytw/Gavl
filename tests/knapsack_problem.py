# 匯入 Gavl 模組，這裡需要將 'import Gavl.Gavl as Gavl' 改為 'import Gavl'，假設適當的路徑已設定
import os, sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(parent_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import Gavl.Gavl as Gavl

ga = Gavl.Gavl()  # 初始化遺傳演算法

# 必要的超參數設定
ga.set_hyperparameter('size_population', 50)  # 設定族群大小為 50
ga.set_hyperparameter('min_length_chromosome', 1)  # 設定染色體最小長度為 1 個基因
ga.set_hyperparameter('max_length_chromosome', 9)  # 設定染色體最大長度為 9 個基因（有 9 個物品可選）

# 最大允許重量設定
MAX_WEIGTH = 15
# 超重每公斤的懲罰
PENALIZATION = 10

# 物品的價格與重量，用字典表示，格式為 {'物品名稱': (價格, 重量)}
prices_weights = {'pen': (5, 3), 'pencil': (4, 2), 'food': (7, 6), 'rubber': (3, 1), 'book': (10, 9), 'scissors': (6, 3), 'glasses': (7, 5), 'case': (7, 7), 'sharpener': (2, 1)}


def fun_fitness(chromosome):
    """ 定義適應度函數。
    
    :param chromosome: (基因列表) 正在分析的個體的染色體。
    """
    fitness = 0  # 累積的適應度
    sum_weights = 0  # 累積的重量
    for item in chromosome:
        fitness += prices_weights[item][0]  # 增加價格到適應度
        sum_weights += prices_weights[item][1]  # 累積重量
    if sum_weights > MAX_WEIGTH:  # 如果超過最大允許重量，則減去懲罰
        fitness -= PENALIZATION * (sum_weights - MAX_WEIGTH)
    return fitness


# 設定適應度函數
ga.set_hyperparameter('fitness', fun_fitness)

# 定義基因可能的值
possible_genes = ['pen', 'pencil', 'food', 'rubber', 'book', 'scissors', 'glasses', 'case', 'sharpener']
ga.set_hyperparameter('possible_genes', possible_genes)  # 設定基因可能的值為物品名稱

# 設定其他參數
ga.set_hyperparameter('termination_criteria', {'max_num_generation_reached': 30})  # 設定終止條件為達到 30 代
ga.set_hyperparameter('repeated_genes_allowed', 0)  # 不允許重複基因
ga.set_hyperparameter('minimize', 0)  # 設定目標是最大化適應度
ga.set_hyperparameter('elitism_rate', 0.1)  # 設定精英比率為 0.1
ga.set_hyperparameter('mutation_rate', 0.2)  # 設定突變率為 0.2
ga.set_hyperparameter('mutation_type', 'both')  # 設定突變類型
ga.set_hyperparameter('keep_diversity', 5)  # 每 5 代維持一次多樣性
ga.set_hyperparameter('show_progress', 1)  # 顯示演算法進展

best_individual = ga.optimize()  # 優化求解

# 獲取結果
best_individual, population, historic_fitness = ga.get_results()
