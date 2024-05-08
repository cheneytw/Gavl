import random
from inspect import signature
from .tools.population import Population
from .tools.individual import Individual
from .tools.generate_chromosome import generate_chromosome
from .tools.termination_criteria import check_termination_criteria
from .tools.keep_diversity import keep_diversity
from .tools.selection import roulette_selection
from .tools.pairing import pairing
from .tools.crossover import mating
from .tools.mutation import mutation


class Gavl(Population):
    """ 遺傳演算法主類，負責執行 GA 並應作為主要調用對象。"""

    def __init__(self):
        """ Gavl 類的構造函數。"""
        super().__init__()  # 呼叫父類的構造函數初始化
        self.size_population = None  # 族群大小
        self.min_length_chromosome = None  # 染色體最小長度
        self.max_length_chromosome = None  # 染色體最大長度
        self.fitness = None  # 個體適應度計算函數
        self.generate_new_chromosome = generate_chromosome  # 新個體生成函數
        self.selection = roulette_selection  # 選擇函數，用於交叉前選擇個體
        self.pairing = pairing  # 配對函數
        self.crossover = mating  # 交叉函數
        self.mutation = mutation  # 突變函數
        self.possible_genes = None  # 可能的基因值
        self.repeated_genes_allowed = 0  # 是否允許基因重複
        self.check_valid_individual = lambda chromosome: True  # 默認所有個體都有效
        self.minimize = 1  # 是否最小化目標函數
        self.elitism_rate = 0.05  # 精英比率
        self.mutation_rate = 0.3  # 突變率
        self.mutation_type = 'both'  # 突變類型
        self.max_num_gen_changed_mutation = None  # 突變時改變的最大基因數
        self.termination_criteria = {'max_num_generation_reached': 100}  # 終止條件
        self._termination_criteria_args = {'termination_criteria': 'max_num_generation_reached', 'generation_goal': 100, 'generation_count': 0}  # 終止條件參數
        self._check_termination_criteria_function = check_termination_criteria  # 檢查終止條件的函數
        self.keep_diversity = -1  # 保持多樣性的策略
        self._keep_diversity_function = keep_diversity  # 保持多樣性的函數
        self.best_fitness_per_generation = []  # 每一代的最佳適應度
        self.show_progress = 1  # 是否顯示進度
        self._generation_count = 0  # 當前已運行的代數

    def set_hyperparameter(self, id_hyperparameter, value):
        """ 設定超參數的方法。
        
        :param id_hyperparameter: 要設定的超參數名稱。
        :param value: 超參數的值。
        """
        # 定義超參數檢查條件和錯誤訊息
        hyperparameter_conditions = {'size_population': ([lambda x: type(x) == int, lambda x: x > 0, lambda x: getattr(self, 'elitism_rate', None) == 0 or getattr(self, 'elitism_rate', None) * x >= 1], "族群大小必須是大於 0 的整數。同時需要設定一個非零的精英比率，或者精英比率乘以族群大小大於等於 1。"), 'min_length_chromosome': ([lambda x: type(x) == int, lambda x: x >= 0, lambda x: True if getattr(self, 'max_length_chromosome', None) is None else x <= getattr(self, 'max_length_chromosome', None)], "染色體的最小長度必須是大於或等於 0 的整數，並且應小於或等於最大長度。"), 'max_length_chromosome': ([lambda x: type(x) == int, lambda x: x >= 1, lambda x: True if getattr(self, 'min_length_chromosome', None) is None else x >= getattr(self, 'min_length_chromosome', None), lambda x: True if getattr(self, 'max_num_gen_changed_mutation', None) is None else x > getattr(self, 'max_num_gen_changed_mutation', None), lambda x: True if getattr(self, 'possible_genes', None) is None or getattr(self, 'repeated_genes_allowed', None) == 1 else x < len(getattr(self, 'possible_genes', None))], "染色體的最大長度必須是大於或等於 1 的整數，並且應大於或等於最小長度。如果已設定突變的最大基因變化數，則最大長度應大於此值。如果不允許基因重複，則可能的基因數應大於最大長度。"), 'fitness': ([lambda x: callable(x), lambda x: len(signature(x).parameters) == 1], "適應度函數應該是一個函數，其唯一參數是個體的染色體，返回適應度值。"), 'generate_new_chromosome': ([lambda x: callable(x), lambda x: len(signature(x).parameters) == 4], "生成新染色體的函數應該是一個接受四個參數的函數：最小染色體長度、最大染色體長度、可能的基因列表和是否允許基因重複。"), 'selection': ([lambda x: callable(x), lambda x: len(signature(x).parameters) == 3], "選擇函數應該是一個接受三個參數的函數：族群列表、最小化標誌和選擇個體的數量，返回選擇的個體ID列表。"), 'pairing': ([lambda x: callable(x), lambda x: len(signature(x).parameters) == 1], "配對函數應該是一個接受一個參數的函數：選擇的個體ID列表，返回配對的個體ID對列表。"), 'crossover': ([lambda x: callable(x), lambda x: len(signature(x).parameters) == 5], "交叉函數應該是一個接受五個參數的函數：配對的個體列表、染色體的最小和最大長度、是否允許基因重複和檢查個體有效性的函數，返回新交叉個體的染色體列表。"), 'mutation': ([lambda x: callable(x), lambda x: len(signature(x).parameters) == 8], "突變函數應該是一個接受八個參數的函數：將要交叉的個體的染色體列表、突變類型、最大變化基因數、染色體的最小和最大長度、是否允許基因重複、檢查個體有效性的函數和可能的基因列表，返回新突變個體的染色體列表。"), 'possible_genes': ([lambda x: type(x) == list, lambda x: True if getattr(self, 'max_length_chromosome', None) is None or getattr(self, 'repeated_genes_allowed', None) == 1 else len(x) >= getattr(self, 'max_length_chromosome', None)], "可能的基因列表應該是一個列表，包含所有可能的基因值。如果不允許基因重複，則列表長度應大於最大染色體長度。"), 'repeated_genes_allowed': ([lambda x: type(x) == int or type(x) == bool, lambda x: x == 0 or x == 1 or type(x) == bool], "是否允許基因重複的屬性應該是 0 或 1，0 表示不允許重複，1 表示允許重複。"), 'check_valid_individual': ([lambda x: callable(x), lambda x: len(signature(x).parameters) == 1], "檢查個體有效性的函數應該是一個函數，其唯一參數是個體的染色體，返回一個布爾值表示個體是否有效。"), 'minimize': ([lambda x: type(x) == int or type(x) == bool, lambda x: x == 0 or x == 1 or type(x) == bool], "最小化目標的屬性應該是 0 或 1，0 表示最大化目標，1 表示最小化目標。"), 'elitism_rate': ([lambda x: type(x) == float or type(x) == int, lambda x: 0 <= x <= 1, lambda x: True if getattr(self, 'size_population', None) is None else x == 0 or getattr(self, 'size_population', None) * x >= 1], "精英比率應該是一個介於 0 和 1 之間的數字。同時需要設定一個非零的精英比率，或者精英比率乘以族群大小大於等於 1。"), 'mutation_rate': ([lambda x: type(x) == float or type(x) == int, lambda x: 0 <= x <= 1], "突變率應該是一個介於 0 和 1 之間的數字。"), 'mutation_type': ([lambda x: type(x) == str, lambda x: x in ['mut_gene', 'addsub_gene', 'both']], "突變類型應該是 'mut_gene', 'addsub_gene', 或 'both' 中的一個。"), 'max_num_gen_changed_mutation': ([lambda x: type(x) == int, lambda x: True if getattr(self, 'max_length_chromosome', None) is None else x < getattr(self, 'max_length_chromosome', None)], "每次突變最大變化的基因數應該是小於最大染色體長度的整數。"), 'termination_criteria': ([lambda x: type(x) == dict, lambda x: len(x) == 1, lambda x: list(x.keys())[0] in ['goal_fitness_reached', 'max_num_generation_reached'], lambda x: type(list(x.values())[0]) == int or type(list(x.values())[0]) == float], "終止條件應該是一個字典，包含 'max_num_generation_reached' 或 'goal_fitness_reached' 中的一個，其值應該是整數或浮點數。"), 'keep_diversity': ([lambda x: type(x) == int, lambda x: x != 0, lambda x: x >= -1], "保持多樣性的屬性應該是一個整數，可以取 -1（表示不使用多樣性保持技術）或大於等於 1 的值（表示每多少代應用一次多樣性保持技術）。"), 'show_progress': ([lambda x: type(x) == int or type(x) == bool, lambda x: x == 0 or x == 1 or type(x) == bool], "是否顯示進度的屬性應該是 0 或 1，0 表示不顯示，1 表示顯示進度。")}
        if id_hyperparameter not in list(hyperparameter_conditions.keys()):
            raise ValueError("設定超參數的方法 set_hyperparameter() 的參數 id_hyperparameter 必須是以下列表中的一個:\n* 'size_population': 代表族群大小的整數。\n* 'min_length_chromosome': 代表染色體最小長度的整數。\n* 'max_length_chromosome': 代表染色體最大長度的整數。\n* 'fitness': 評估適應度的函數。其唯一參數是個體的染色體（fitness(chromosome)）並返回適應度的值。\n* 'generate_new_chromosome': 創建新染色體的函數。它接受四個參數（按此順序）最小染色體長度、最大染色體長度、可能的基因列表和是否允許基因重複。這個函數必須返回一個基因列表。\n* 'selection': 執行選擇方法的函數。它必須是一個接受三個參數的函數並返回選中的個體的列表。它接收（按此順序）一個包含族群的列表（族群的個體類的對象列表）、屬性 self.minimize（1 -> 最小化；0 -> 最大化）和要選中的個體的數量。它必須返回一個包含選中個體ID的列表（individual._id）。默認的選擇方法是輪盤選擇。\n* 'pairing': 執行配對方法的函數。它必須是一個接受一個參數的函數並返回配對的個體的列表。它接收一個包含選中個體ID的列表（見選擇方法），並返回一個包含配對的個體ID對的列表。默認的配對方法是隨機配對。\n* 'crossover': 執行交叉方法的函數。它必須是一個接受五個參數的函數並返回新交叉個體的染色體的列表。它必須接收（按此順序）一個列表（[(Individual_a, Individual_b) , ...]）包含配對的個體（個體類的對象），染色體的最小允許長度、最大長度、一個布爾值指示是否允許基因重複（1 = 允許重複的基因）和一個函數 check_valid_individual(chromosome) 它接收一個個體的染色體並返回一個布爾值指示該個體是否有效（True）或無效（False）。它必須返回一個包含新創建個體的染色體的列表。\n* 'mutation': 執行突變方法的函數。它必須是一個接受八個參數的函數並返回新突變個體的染色體的列表。它必須接收（按此順序）一個列表包含將要交叉的個體的染色體（注意，這個函數接收的是染色體，即基因的列表，不是個體類的對象），一個字符串代表突變類型（如果突變方法改變，這是無用的），一個整數代表允許在一次突變中改變的最大基因數（它是屬性 .max_num_gen_changed_mutation），染色體的最小允許長度、最大長度、一個布爾值指示是否允許基因重複（1 = 允許重複的基因），一個函數 check_valid_individual(chromosome) 它接收一個個體的染色體並返回一個布爾值指示該個體是否有效（True）或無效（False）和一個列表包含所有允許的基因值（它是屬性 .possible_genes）。它必須返回一個包含新突變個體的染色體的列表。\n* 'possible_genes': 所有可能的基因值的列表。\n* 'repeated_genes_allowed': 一個整數表示一個個體是否可以有重複的基因（repeated_genes_allowed = 1）或不可以（repeated_genes_allowed = 0）。默認為 0。\n* 'check_valid_individual': 一個函數其唯一參數是個體的染色體（即 check_valid_individual(chromosome)）並返回一個布爾值（True 如果它是一個有效的解決方案，False 否則）。注意建議不改變這個方法，並在適應度函數中給無效的個體一個懲罰。注意染色體是一個基因的列表。\n* 'minimize': 一個整數表示是否將適應度最小化（minimize = 1）或最大化（minimize = 0）。默認 minimize = 1。\n* 'elitism_rate': 一個介於 0 和 1 之間的數字表示精英率。默認 elitism_rate = 0.05。\n* 'mutation_rate': 一個介於 0 和 1 之間的數字表示突變率。默認 mutation_rate = 0.3。\n* 'mutation_type': 一個字符串表示突變類型。它只能取 'mut_gene', 'addsub_gene' 或 'both' 的值。默認 mutation_type = 'both'。\n* 'max_num_gen_changed_mutation': 一個整數表示每次突變最大變化的基因數。默認它是 int(max_length_chromosome/3 + 1)。\n* 'termination_criteria': 屬性 'termination_criteria' 必須是一個字典表示終止條件，包含值 '{'max_num_generation_reached': 代數}' 或 '{'goal_fitness_reached': 目標適應度}'。\n* 'keep_diversity': 一個整數表示每多少代應用一次多樣性保持技術。它的默認值是 -1，這意味著不會應用多樣性保持技術。\n* 'show_progress': 一個整數表示是否願意顯示進度。它可以取 0（不顯示進度）或 1（顯示進度）。它的默認值是 1。"
                             "")
        else:
            try:
                conditions = hyperparameter_conditions[id_hyperparameter]
                if False in list(map(lambda x: x(value), conditions[0])):  # 檢查所有條件
                    raise ValueError(conditions[1])  # 發生錯誤
                else:
                    setattr(self, id_hyperparameter, value)  # 設定屬性
                    if id_hyperparameter == 'max_length_chromosome' and getattr(self, 'max_num_gen_changed_mutation', None) is None:  # 如果正在設定的超參數是 'max_length_chromosome' 並且沒有定義超參數 'max_num_gen_changed_mutation'，則將其設定為 'max_length_chromosome'
                        setattr(self, 'max_num_gen_changed_mutation', int(value / 3 + 1))  # 設定屬性
                    elif id_hyperparameter == 'termination_criteria':  # 更新檢查終止條件的函數的參數
                        if list(value.keys())[0] == 'goal_fitness_reached':
                            self._termination_criteria_args = {'termination_criteria': 'goal_fitness_reached', 'goal_fitness': list(value.values())[0], 'generation_fitness': 0, 'minimize': self.minimize}
                        elif list(value.keys())[0] == 'max_num_generation_reached':
                            self._termination_criteria_args = {'termination_criteria': 'max_num_generation_reached', 'generation_goal': list(value.values())[0], 'generation_count': 0}
                        else:  # 重新檢查
                            ValueError("終止條件參數只能包含 'goal_fitness_reached' 或 'max_num_generation_reached' 其中之一。")
                    elif id_hyperparameter == 'minimize' and self._termination_criteria_args['termination_criteria'] == 'goal_fitness_reached':
                        self._termination_criteria_args['minimize'] = value
            except ValueError:
                raise ValueError(conditions[1])  # 發生錯誤
            except Exception as e:
                print(str)
                raise (type(e))(str(e) + '\n' + conditions[1])  # 發生錯誤

    def optimize(self):
        """ 開始最優化（啟動遺傳演算法）。在呼叫此方法之前，必須定義 Gavl.size_population, Gavl.min_length_chromosome, Gavl.max_length_chromosome, Gavl.fitness 和 Gavl.possible_genes。

        :return:
            (Individual) 最佳個體。
        """
        # 首先檢查所需屬性是否已定義。
        if self.fitness is None:
            raise AttributeError("在呼叫此方法之前，必須定義適應度方法。可以通過調用方法 Gavl.set_hyperparameter('fitness', value) 來定義，其中 value 是一個函數，其唯一參數是個體的染色體（fitness(chromosome)）並返回適應度值。")
        elif self.size_population is None:
            raise AttributeError("在呼叫此方法之前，必須定義屬性 'size_population'。它必須是一個大於 0 的整數，可以通過調用方法 Gavl.set_hyperparameter('size_population', value) 來設定。")
        elif self.min_length_chromosome is None:
            raise AttributeError("在呼叫此方法之前，必須定義屬性 'min_length_chromosome'。它必須是一個大於 0 的整數，可以通過調用方法 Gavl.set_hyperparameter('min_length_chromosome', value) 來設定。")
        elif self.max_length_chromosome is None:
            raise AttributeError("在呼叫此方法之前，必須定義屬性 'max_length_chromosome'。它必須是一個大於 0 的整數，可以通過調用方法 Gavl.set_hyperparameter('max_length_chromosome', value) 來設定。")
        elif self.possible_genes is None:
            raise AttributeError("在呼叫此方法之前，必須定義屬性 'possible_genes'。它必須是一個包含所有可能的基因值的列表。")
        else:
            # 開始演算法
            self._generation_count = 0  # 開始代數計數器
            self.best_fitness_per_generation = []  # 清空最佳適應度列表
            # 創建族群
            self._Population__generate_population()
            self._Population__calculate_fitness_and_sort()
            if self._check_termination_criteria_function(self._termination_criteria_args):
                return self.best_individual()
            while not self._check_termination_criteria_function(self._termination_criteria_args):
                self._generation_count += 1  # 代數計數器增加
                if self.show_progress:
                    print('Generation: {}'.format(self._generation_count))
                new_population = self._Population__get_next_generation()  # 計算下一代。
                self._Population__kill_and_reset_whole_population(new_population)  # 設定下一代。
                if self._generation_count % self.keep_diversity == 0 and self.keep_diversity > 0:
                    self._Population__calculate_fitness_and_sort()  # 計算適應度並排序
                    # 保持多樣性協議：
                    new_diverse_population = self._keep_diversity_function(self.population, self.generate_new_chromosome, self.min_length_chromosome, self.max_length_chromosome, self.possible_genes, self.repeated_genes_allowed, self.check_valid_individual)
                    self._Population__kill_and_reset_whole_population(new_diverse_population)  # 設定下一代。
                self.__update_termination_criteria_args()  # 更新終止條件參數
                self.best_fitness_per_generation.append(self.best_individual().fitness_value)  # 獲取每一代的最佳適應度值
            self._Population__calculate_fitness_and_sort()  # 計算適應度並排序
            return self.best_individual()

    def _Population__get_next_generation(self):
        """ 用於計算下一代的方法。

        :return:
            * :new_generation: (染色體列表) 下一代的染色體列表。
        """
        # 首先，按適應度對族群進行排序：
        self._Population__calculate_fitness_and_sort()  # 計算適應度並排序
        # 下一代個體列表：
        new_generation = []
        # 獲取新族群的分組大小：
        size_elitism = int(len(self.population) * self.elitism_rate)  # 精英個體數
        size_crossover = int(len(self.population)) - size_elitism  # 交叉個體數
        if (size_crossover % 2) == 1:  # 如果交叉個體數是奇數
            size_elitism += 1  # 精英個體數增加一個
            size_crossover -= 1  # 交叉個體數減少一個
        # 精英：
        elite = [individual.chromosome for individual in self.population[:size_elitism]]
        new_generation.extend(elite)  # 添加精英個體 ---> 注意，在調用此函數之前，族群已按適應度排序。
        # 交叉：
        selected_individuals = self.selection(self.population, self.minimize, size_crossover)  # 1. 輪盤選擇
        paired_ids = self.pairing(selected_individuals)  # 2. 進行配對
        list_of_paired_ind = [(self.get_individual_by_id(id_a).chromosome, self.get_individual_by_id(id_b).chromosome) for id_a, id_b in paired_ids]  # 配對個體的染色體列表
        new_crossed_ind = self.crossover(list_of_paired_ind, self.min_length_chromosome, self.max_length_chromosome, self.repeated_genes_allowed, self.check_valid_individual)  # 3. 獲得已交叉的新染色體
        for new_individual in new_crossed_ind:  # 4. 添加已交叉的個體
            if type(new_individual) == Individual:
                new_generation.append(new_individual.chromosome)
            elif type(new_individual) == list:
                new_generation.append(new_individual)
            else:  # 如果交叉方法被錯誤地重新定義
                raise ValueError('交叉方法必須返回新交叉個體的染色體列表。')
        # 突變：
        size_mutation = int(len(self.population) * self.mutation_rate)  # 突變個體數
        if size_mutation >= len(new_generation) - size_elitism:
            size_mutation = int(len(new_generation) - size_elitism) - 1
        indices_mutation = random.sample(range(size_elitism, len(new_generation)), size_mutation)  # 獲取將要突變的個體的索引
        chromosomes_to_mutate = [new_generation[i] for i in indices_mutation]  # 獲取將要突變的染色體
        mutated_individuals = self.mutation(chromosomes_to_mutate, self.mutation_type, self.max_num_gen_changed_mutation, self.min_length_chromosome, self.max_length_chromosome, self.repeated_genes_allowed, self.check_valid_individual, self.possible_genes)
        for i in indices_mutation:  # 將新突變的個體添加到族群中
            m_ind = mutated_individuals.pop()
            if type(m_ind) == Individual:
                new_generation[i] = m_ind.chromosome
            elif type(m_ind) == list:
                new_generation[i] = m_ind
            else:  # 如果突變方法被錯誤地重新定義
                raise ValueError('突變方法必須返回新突變個體的染色體列表。')
        return new_generation

    def _Population__calculate_fitness_population(self):
        """ 計算族群中所有個體的適應度並設置這個屬性給每個個體。
        """
        # 首先檢查所需屬性是否已定義。
        if self.fitness is None:
            raise AttributeError("在調用此方法之前，必須定義適應度方法。可以通過調用方法 Gavl.set_hyperparameter('fitness', value) 來定義，其中 value 是一個函數，其唯一參數是個體的染色體（fitness(chromosome)）並返回適應度值。")
        elif not len(self.population):
            raise AttributeError('族群尚未生成。')
        else:
            for ind in self.population:
                ind.calculate_fitness(self.fitness)

    def _Population__generate_population(self):
        """ 生成新的族群並將其添加到 population 屬性中。
        """
        if self.fitness is None:
            raise AttributeError("在調用此方法之前，必須定義適應度方法。可以通過調用方法 Gavl.set_hyperparameter('fitness', value) 來定義，其中 value 是一個函數，其唯一參數是個體的染色體（fitness(chromosome)）並返回適應度值。")
        elif self.size_population is None:
            raise AttributeError("在調用此方法之前，必須定義屬性 'size_population'。它必須是一個大於 0 的整數，可以通過調用方法 Gavl.set_hyperparameter('size_population', value) 來設定。")
        elif self.min_length_chromosome is None:
            raise AttributeError("在調用此方法之前，必須定義屬性 'min_length_chromosome'。它必須是一個大於 0 的整數，可以通過調用方法 Gavl.set_hyperparameter('min_length_chromosome', value) 來設定。")
        elif self.max_length_chromosome is None:
            raise AttributeError("在調用此方法之前，必須定義屬性 'max_length_chromosome'。它必須是一個大於 0 的整數，可以通過調用方法 Gavl.set_hyperparameter('max_length_chromosome', value) 來設定。")
        elif self.possible_genes is None:
            raise AttributeError("在調用此方法之前，必須定義屬性 'possible_genes'。它必須是一個包含所有可能的基因值的列表。")
        else:
            while len(self.population) < self.size_population:
                # 創建新個體：
                new_ind = self.generate_new_chromosome(self.min_length_chromosome, self.max_length_chromosome, self.possible_genes, self.repeated_genes_allowed)
                if self.check_valid_individual(new_ind):  # 如果檢查個體有效性的函數過於嚴格，可能會導致這一步需要很長時間
                    self.add_individual(new_ind)

    def _Population__sort_population(self):
        """ 對族群按適應度進行排序。
        """
        if not len(self.population):
            raise AttributeError('族群尚未生成。')
        else:
            if any([ind.fitness_value is None for ind in self.population]):
                self._Population__calculate_fitness_population()  # 如果還沒有計算，先計算個體的適應度
            if self.minimize:  # 如果目標是最小化
                self.population.sort(key=lambda x: x.fitness_value, reverse=False)  # 從最佳適應度到最差適應度排序
            else:
                self.population.sort(key=lambda x: x.fitness_value, reverse=True)  # 從最差適應度到最佳適應度排序

    def __update_termination_criteria_args(self):
        """ 更新終止條件參數的方法。這個方法必須在遺傳演算法的每一新代中被調用。

        :return:
        """
        if list(self.termination_criteria.keys())[0] == 'max_num_generation_reached':
            self._termination_criteria_args['generation_count'] = self._generation_count
        elif list(self.termination_criteria.keys())[0] == 'goal_fitness_reached':
            self._termination_criteria_args['generation_fitness'] = self.best_individual().fitness_value

    def add_individual(self, individual):
        """ 將新個體添加到族群中的方法。這個方法覆蓋了具有相同名稱的類 Population 中的方法 ---> 這樣做是為了檢查是否添加的個體數超過了 self.size_population 許可的最大值。

        :param individual: (Individual 或列表) 個體類的對象或代表染色體的列表。
        :return:
        """
        if self.size_population is None:
            raise AttributeError('族群大小尚未生成。請通過調用 Gavl.set_hyperparameter("size_population", size) 定義它。')
        else:
            if type(individual) == list:
                ind = individual.copy()
            elif type(individual) == Individual:
                ind = individual.chromosome.copy()
            else:
                raise ValueError('提供的個體無效。它必須是一個基因列表或個體類的對象。')
            if self.check_valid_individual(ind):
                # 檢查族群中的個體數是否小於允許的最大值
                if len(self.population) < self.size_population:
                    super().add_individual(ind)
                else:
                    raise AttributeError('族群已滿（有 {} 個體，這是指定的最大族群大小）。如果想要更多個體，可以通過調用 Gavl.set_hyperparameter("size_population", size) 改變族群大小。'.format(self.size_population))
            else:
                raise ValueError('提供的個體無效。請檢查方法 check_valid_individual 或更改個體。')

    def best_individual(self):
        """ 返回最佳個體的方法。

        :return:
            * :individual: (Individual) 最佳個體。
        """
        if not len(self.population):
            raise AttributeError('族群尚未生成。')
        self._Population__sort_population()  # 從最佳個體到最差個體排序族群。
        return self.population[0]

    def historic_fitness(self):
        """ 返回每一代的最佳適應度值的方法。

        :return:
            * :bfv: (浮點數列表) 返回每一代的最佳適應度值列表。
        """
        if not self.best_fitness_per_generation:
            raise ValueError('在調用此方法之前，必須進行優化（調用方法 .optimize()）。')
        return self.best_fitness_per_generation

    def get_results(self):
        """ 獲取優化過程的結果的方法，一旦優化完成。

        :return:
            * :best_individual: (Individual) 最佳個體。
            * :population: (個體列表) 最後一代的所有個體列表。
            * :historic_fitness: (浮點數列表) 每一代的最佳適應度值列表。
        """
        # 首先檢查所需屬性是否已定義。
        if self.fitness is None:
            raise AttributeError("在調用此方法之前，必須定義適應度方法。可以通過調用方法 Gavl.set_hyperparameter('fitness', value) 來定義，其中 value 是一個函數，其唯一參數是個體的染色體（fitness(chromosome)）並返回適應度值。")
        elif self.size_population is None:
            raise AttributeError("在調用此方法之前，必須定義屬性 'size_population'。它必須是一個大於 0 的整數，可以通過調用方法 Gavl.set_hyperparameter('size_population', value) 來設定。")
        elif self.min_length_chromosome is None:
            raise AttributeError("在調用此方法之前，必須定義屬性 'min_length_chromosome'。它必須是一個大於 0 的整數，可以通過調用方法 Gavl.set_hyperparameter('min_length_chromosome', value) 來設定。")
        elif self.max_length_chromosome is None:
            raise AttributeError("在調用此方法之前，必須定義屬性 'max_length_chromosome'。它必須是一個大於 0 的整數，可以通過調用方法 Gavl.set_hyperparameter('max_length_chromosome', value) 來設定。")
        elif self.possible_genes is None:
            raise AttributeError("在調用此方法之前，必須定義屬性 'possible_genes'。它必須是一個包含所有可能的基因值的列表。")
        best_individual = self.best_individual()
        population = self.population
        historic_fitness = self.historic_fitness()
        return best_individual, population, historic_fitness
