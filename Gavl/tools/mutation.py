"""
In this file it is defined the function to perform mutation.

Function: 
    mutation: Function that performs mutation.
    mutate_genes_manner: Auxiliary function to make the mutation by changing the genes.
    mutate_length_manner: Auxiliary function to make the mutation in length.
"""
import random
from .aux_functions.combinations import combinations


def mutation(chromosomes_to_mutate, mutation_type, max_num_gen_changed_mutation, min_length_chromosome, max_length_chromosome, repeated_genes_allowed, check_valid_individual, possible_genes):
    """ 這個函數接收染色體並對其元素進行隨機突變。它會迭代所有可能的突變，直到找到一個為止，此時執行停止。如果沒有找到突變，則返回輸入的染色體。請注意，使用函數 check_valid_individual 來測試創建的個體，如果對同一個體進行了1000次不成功的突變，則將其視為無法突變的個體，並返回其原始染色體。 """
    if mutation_type not in ['mut_gene', 'addsub_gene', 'both']:  # 檢查突變類型是否在指定範圍內
        raise ValueError("The parameter 'mutation_type' can only take the values 'mut_gene', 'addsub_gene' or 'both'.")
    list_new_mutated_chromosomes = []  # 初始化一個列表來存儲突變後的染色體
    for chromosome in chromosomes_to_mutate:  # 遍歷每一條需要突變的染色體
        if repeated_genes_allowed:  # 如果允許重複基因
            mutation_genes = possible_genes  # 使用所有可能的基因作為突變基因
        else:  # 如果不允許重複基因
            mutation_genes = [e for e in possible_genes if e not in chromosome]  # 選擇未在當前染色體中的基因作為突變基因
        both_mutations_selection = int(random.random() > 0.5)  # 如果突變類型為'both'，隨機選擇突變類型
        # 開始突變演算法
        if (mutation_type == 'mut_gene') or ((mutation_type == 'both') and (both_mutations_selection == 0)):  # 如果是單基因突變或隨機選擇了單基因突變
            new_mutated_chromosome = mutate_genes_manner(chromosome, max_num_gen_changed_mutation, mutation_genes, check_valid_individual)  # 進行基因突變
            list_new_mutated_chromosomes.append(new_mutated_chromosome)  # 將突變後的染色體添加到列表中
        elif (mutation_type == 'addsub_gene') or ((mutation_type == 'both') and (both_mutations_selection == 1)):  # 如果是基因數目增減突變或隨機選擇了基因數目增減突變
            new_mutated_chromosome = mutate_length_manner(chromosome, max_num_gen_changed_mutation, min_length_chromosome, max_length_chromosome, mutation_genes, check_valid_individual)  # 進行基因長度的調整突變
            list_new_mutated_chromosomes.append(new_mutated_chromosome)  # 將突變後的染色體添加到列表中
    return list_new_mutated_chromosomes  # 返回所有突變後的染色體列表


def mutate_genes_manner(chromosome, max_num_gen_changed_mutation, mutation_genes, check_valid_individual):
    """ 這個函數執行基因的突變（不涉及長度的變化）。

    :param chromosome: (list of genes) 需要突變的染色體。
    :param max_num_gen_changed_mutation: (int) 單次突變中最大可改變的基因數量。
    :param mutation_genes: (list of genes) 可用於突變的基因列表（這些基因不在個體中）。
    :param check_valid_individual: (function) 函數，接收一個染色體並返回一個布林值，表示該染色體是否構成一個有效的個體。
    :return:
        * :new_chromosome: (list of genes) 突變後的新染色體。
    """
    random.shuffle(chromosome)  # 對染色體進行隨機排序
    random.shuffle(mutation_genes)  # 對可突變基因進行隨機排序
    # 隨機獲取變更基因的數量
    num_genes_to_mutate = list(range(1, min(max_num_gen_changed_mutation, len(mutation_genes), len(chromosome)) + 1))  # 從可變更的基因數量中生成範圍列表
    random.shuffle(num_genes_to_mutate)  # 對基因變更數量列表進行隨機排序
    count_mutations_tried = 0  # 計算嘗試的突變次數
    # 開始執行突變演算法
    for num_gen in num_genes_to_mutate:  # 選取一定數量的基因進行突變
        genes_in_combinations = combinations(mutation_genes, num_gen)  # 從突變基因中選取可能的組合
        for gen_in_comb in genes_in_combinations:
            genes_out_combinations = combinations(chromosome, num_gen)  # 從當前染色體中選取將被替換的基因組合
            for gen_out_comb in genes_out_combinations:
                count_mutations_tried += 1  # 突變嘗試次數加一
                new_chromosome = chromosome.copy()  # 複製當前染色體以進行突變
                for gen in gen_out_comb:
                    new_chromosome.remove(gen)  # 從染色體中移除舊的基因
                new_chromosome.extend(gen_in_comb)  # 向染色體中添加新的基因
                if check_valid_individual(new_chromosome):  # 檢查新染色體是否有效
                    return new_chromosome  # 如果有效則返回新染色體
                if count_mutations_tried >= 1000:  # 如果嘗試突變達到1000次仍未成功，則中斷
                    return chromosome  # 返回原始染色體
    return chromosome  # 如果未找到有效的突變，則返回原始染色體


def mutate_length_manner(chromosome, max_num_gen_changed_mutation, min_length_chromosome, max_length_chromosome, mutation_genes, check_valid_individual):
    """進行染色體長度的突變（添加或刪除基因）"""
    random.shuffle(chromosome)  # 對染色體隨機排序
    random.shuffle(mutation_genes)  # 對可能的突變基因隨機排序
    # 決定是添加還是刪除基因
    if len(chromosome) == min_length_chromosome:  # 如果達到最小長度，則添加基因
        add = 1
    elif len(chromosome) == max_length_chromosome:  # 如果達到最大長度，則刪除基因
        add = 0
    else:
        add = int(random.random() > 0.5)  # 隨機決定添加或刪除
    # 根據添加或刪除選擇改變的基因數目
    if add:
        num_genes_to_mutate = list(range(1, min(max_num_gen_changed_mutation, len(mutation_genes), max_length_chromosome - len(chromosome)) + 1))  # 建立添加基因的數目範圍
    else:
        num_genes_to_mutate = list(range(1, min(max_num_gen_changed_mutation, len(chromosome) - min_length_chromosome) + 1))  # 建立刪除基因的數目範圍
    random.shuffle(num_genes_to_mutate)  # 對數目列表進行隨機排序
    count_mutations_tried = 0  # 計數試圖突變的次數
    # 開始突變演算法
    if add:  # 添加基因的情況
        for num_gen in num_genes_to_mutate:
            genes_in_combinations = combinations(mutation_genes, num_gen)  # 從可能的突變基因中選出組合
            for gen_comb in genes_in_combinations:
                count_mutations_tried += 1
                new_chromosome = chromosome.copy()
                new_chromosome.extend(gen_comb)  # 將新基因添加到染色體中
                if check_valid_individual(new_chromosome):  # 檢查新的染色體是否有效
                    return new_chromosome
                if count_mutations_tried >= 1000:  # 如果嘗試了1000次仍未找到有效突變，則停止
                    return chromosome
    else:  # 刪除基因的情況
        for num_gen in num_genes_to_mutate:
            genes_in_combinations = combinations(chromosome, num_gen)  # 從染色體中選出將要刪除的基因組合
            for gen_comb in genes_in_combinations:
                count_mutations_tried += 1
                new_chromosome = chromosome.copy()
                for gen in gen_comb:
                    new_chromosome.remove(gen)  # 從染色體中移除選定的基因
                if check_valid_individual(new_chromosome):  # 檢查新的染色體是否有效
                    return new_chromosome
                if count_mutations_tried >= 1000:  # 如果嘗試了1000次仍未找到有效突變，則停止
                    return chromosome
    return chromosome  # 如果找不到有效的突變，返回原染色體
