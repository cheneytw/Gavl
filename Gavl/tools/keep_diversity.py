"""
In this file it is defined a function to keep the diversity.

Functions:
    keep_diversity: Function called to keep the diversity.
"""


def keep_diversity(population, generate_chromosome, min_length_chromosome, max_length_chromosome, possible_genes, repeated_genes_allowed, check_valid_chromosome):
    """
    此函數在希望強調族群多樣性時調用。當族群中出現重複的個體時，將其替換為全新隨機生成的個體。同時，最差的 25% 個體也被全新隨機個體所替代。
    注意在調用此函數前，必須先按適應度對族群進行排序。

    :param population: (list of Individuals) 按適應度排序的族群（從最好到最差）。
    :param generate_chromosome: (function) 生成新染色體的函數。
    :param min_length_chromosome: (int) 染色體的最小允許長度。
    :param max_length_chromosome: (int) 染色體的最大允許長度。
    :param possible_genes: (list of ...) 包含所有可能基因值的列表。
    :param repeated_genes_allowed: (bool) 指示染色體中的基因是否可以重複的布爾值。
    :param check_valid_chromosome: (function) 函數接收染色體，如果創建有效的個體則返回 True，否則返回 False。
    :return:
        (list of chromosomes) 將代表下一代的染色體列表。
    """
    new_population = [population[0].chromosome]  # 新族群列表，初始包括最優個體的染色體
    list_chromosomes = [ind.chromosome for ind in population]  # 所有個體的染色體列表
    copy_list_chromosomes = list_chromosomes.copy()  # 染色體列表的副本
    try:
        for i in range(len(list_chromosomes)):
            chrom = list_chromosomes[i]
            if type(chrom[0]) in [int, float, str, chr]:
                chrom.sort()  # 對基因進行排序，以正確移除重複個體
            elif type(chrom[0]) == dict:
                list_chromosomes[i] = sorted(chrom, key=lambda i: (list(i.keys())[0], list(i.values())[0]))  # 嘗試對字典類型的基因進行排序
    except:
        print('Sorting error in keep_diversity.')
        list_chromosomes = copy_list_chromosomes.copy()  # 排序出錯時，使用原始染色體列表
    for i in range(1, int(len(list_chromosomes) / 4)):  # 遍歷前 25% 的個體
        if population[i].chromosome in list_chromosomes[:i]:
            new_ind = generate_chromosome(min_length_chromosome, max_length_chromosome, possible_genes, repeated_genes_allowed)  # 生成新個體
            while not check_valid_chromosome(new_ind):
                new_ind = generate_chromosome(min_length_chromosome, max_length_chromosome, possible_genes, repeated_genes_allowed)  # 驗證新個體是否有效
            new_population.append(new_ind)
        else:
            new_population.append(population[i].chromosome)
    while len(new_population) < len(population):  # 為替換最差的 25% 增加新的隨機生成個體
        new_ind = generate_chromosome(min_length_chromosome, max_length_chromosome, possible_genes, repeated_genes_allowed)
        if check_valid_chromosome(new_ind):
            new_population.append(new_ind)
    return new_population
