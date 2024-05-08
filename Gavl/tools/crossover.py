import random
from .aux_functions.combinations import combinations  # 引入組合計算功能


def cross_individuals(chromosome_a, chromosome_b, min_length_chromosome, max_length_chromosome, repeated_genes_allowed, check_valid_individual):
    """
    這個函數計算兩個不同個體之間的交叉。它選擇隨機數量的基因從 a 和 b 個體交換，並檢查是否存在可能的交叉大小（使用函數 check_valid_individual 檢查）。
    如果存在，則隨機選擇一種可能的交叉進行，並返回結果新染色體。如果沒有可能的交叉大小，則測試另一個不同的組合大小。
    注意，使用函數 check_valid_individual 來測試創建的個體，如果進行了 2000 次不成功的交叉，則認為是無法配對的個體對，並返回它們的原始染色體。
    
    :param chromosome_a: (list) 個體 A 的染色體。
    :param chromosome_b: (list) 個體 B 的染色體。
    :param min_length_chromosome: (int) 染色體的最小基因數。
    :param max_length_chromosome: (int) 染色體的最大基因數。
    :param repeated_genes_allowed: (int) 表示個體是否可以有重複基因的布爾值，1 表示允許重複基因，0 表示不允許。
    :param check_valid_individual: (function) 函數接收一個染色體並返回一個布爾值，指出這個染色體是否構成一個有效的個體（True）或不（False）。
    :return:
        * :crossed_a: (list) 交叉後的個體 A。
        * :crossed_b: (list) 交叉後的個體 B。
    """
    if repeated_genes_allowed:  # 如果允許重複基因
        genes_a = chromosome_a  # A 的基因列表可以交叉
        genes_b = chromosome_b  # B 的基因列表可以交叉
    else:  # 不允許重複基因
        genes_a = [gen for gen in chromosome_a if gen not in chromosome_b]  # 從 A 中選擇不在 B 中的基因
        genes_b = [gen for gen in chromosome_b if gen not in chromosome_a]  # 從 B 中選擇不在 A 中的基因
    random.shuffle(genes_a)  # 隨機打亂 A 的基因順序
    random.shuffle(genes_b)  # 隨機打亂 B 的基因順序
    number_of_genes_to_change_a = list(range(1, len(genes_a) + 1))  # A 的可交換基因數量列表
    random.shuffle(number_of_genes_to_change_a)  # 隨機打亂 A 的交換基因數量
    count_crossover_tried = 0  # 試圖交叉的次數計數器
    for num_a in number_of_genes_to_change_a:  # 從 A 中隨機選擇基因數進行交換
        number_of_genes_to_change_b = list(range(1, len(genes_b) + 1))  # B 的可交換基因數量列表
        random.shuffle(number_of_genes_to_change_b)  # 隨機打亂 B 的交換基因數量
        for num_b in number_of_genes_to_change_b:  # 從 B 中隨機選擇基因數進行交換
            if min_length_chromosome <= len(chromosome_a) - num_a + num_b <= max_length_chromosome and min_length_chromosome <= len(chromosome_b) - num_b + num_a <= max_length_chromosome:  # 確保交叉後的個體在染色體長度限制內
                genes_a_combinations = combinations(genes_a, num_a)  # 從 A 中選擇的基因組合
                for genes_change_a in genes_a_combinations:
                    genes_b_combinations = combinations(genes_b, num_b)  # 從 B 中選擇的基因組合
                    for genes_change_b in genes_b_combinations:
                        count_crossover_tried += 1
                        crossed_a = chromosome_a.copy()
                        crossed_b = chromosome_b.copy()
                        for gen in genes_change_a:
                            crossed_a.remove(gen)
                            crossed_b.append(gen)
                        for gen in genes_change_b:
                            crossed_b.remove(gen)
                            crossed_a.append(gen)
                        if not check_valid_individual(crossed_b):
                            break  # 如果 B 的任何基因組合都不能構成有效個體，則跳出，嘗試 A 的其他基因組合
                        if check_valid_individual(crossed_a):  # 如果 A 的某個組合有效
                            return crossed_a, crossed_b
                        if count_crossover_tried >= 2000:
                            return chromosome_a, chromosome_b  # 如果試圖交叉 2000 次均失敗，則返回原始染色體
            else:
                break  # 如果結果個體不在染色體長度限制內，則嘗試其他組合
    return chromosome_a, chromosome_b  # 如果沒有可能的交叉，則返回兩個原始個體


def mating(list_of_paired_ind, min_length_chromosome, max_length_chromosome, repeated_genes_allowed, check_valid_individual):
    """
    這個函數返回當可能進行配對時的配對個體。如果所有組合都導致無效的個體（例如，如果 repeated_genes_allowed = 0 且兩個個體完全相同），則返回原本打算配對的兩個個體。
    
    :param list_of_paired_ind: (list of tuples of lists) 配對個體的列表，每個元組代表兩個配對的個體。形式為 [(Individual_a, Individual_b), (Individual_c, Individual_d), ...]；在這個例子中，個體 a 與個體 b 配對，個體 c 與個體 d 配對。注意，元組中包含的是個體類的對象。
    :param min_length_chromosome: (int) 染色體的最小基因數。
    :param max_length_chromosome: (int) 染色體的最大基因數。
    :param repeated_genes_allowed: (int) 表示個體是否可以有重複基因的布爾值，1 表示允許重複基因，0 表示不允許。
    :param check_valid_individual: (function) 函數接收一個染色體並返回一個布爾值，指出這個染色體是否構成一個有效的個體（True）或不（False）。
    :return:
        * :crossed_individuals: (list of lists) 交叉後個體的染色體列表。
    """
    crossed_individuals = []  # 輸出 ---> 交叉後個體的列表。
    for (chromosome_a, chromosome_b) in list_of_paired_ind:
        crossed_a, crossed_b = cross_individuals(chromosome_a=chromosome_a, chromosome_b=chromosome_b, min_length_chromosome=min_length_chromosome, max_length_chromosome=max_length_chromosome, repeated_genes_allowed=repeated_genes_allowed, check_valid_individual=check_valid_individual)
        crossed_individuals.append(crossed_a)
        crossed_individuals.append(crossed_b)
    return crossed_individuals  # 返回交叉後的個體列表
