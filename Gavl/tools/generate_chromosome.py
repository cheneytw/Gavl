import random  # 引入 random 模塊用於生成隨機數


def generate_chromosome(min_length_chromosome, max_length_chromosome, possible_genes, repeated_genes_allowed):
    """
    這個函數用來創建一個新的個體（它的染色體）。它隨機選擇染色體的長度（介於 min_length_chromosome 和 max_length_chromosome 之間），並在可能的基因列表 possible_genes 中隨機選擇基因。

    :param min_length_chromosome: (int) 染色體的最小允許長度。
    :param max_length_chromosome: (int) 染色體的最大允許長度。
    :param possible_genes: (list of ...) 包含所有可能基因值的列表。
    :param repeated_genes_allowed: (bool) 一個布爾值，指示染色體中的基因是否可以重複（repeated_genes_allowed = 1）或不可以重複（repeated_genes_allowed = 0）。
    :return:
        * (list of genes) 代表染色體的基因列表。
    """
    # 隨機選擇基因數量
    number_of_genes = random.randrange(min_length_chromosome, max_length_chromosome + 1)  # 從最小到最大長度範圍內隨機選擇染色體長度
    # 創建新的染色體：
    if repeated_genes_allowed:
        chromosome = random.choices(possible_genes, weights=None, k=number_of_genes)  # 允許基因重複，隨機選擇指定數量的基因
        return chromosome
    else:
        possible_genes_aux = possible_genes.copy()  # 創建可能基因的副本以防修改原列表
        random.shuffle(possible_genes_aux)  # 打亂可能基因列表以獲得隨機性
        return possible_genes_aux[:number_of_genes]  # 返回基因列表的切片，即不允許基因重複的染色體
