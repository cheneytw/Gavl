"""
In this file it is defined the class to hold the population.

Classes:
    :Population: Main class.
"""
from .individual import Individual
from abc import ABC, abstractmethod


class Population(ABC):
    """ 人口類別。 """

    def __init__(self):
        """ 建構子。 """
        self.population = []  # 算法開始時將填充此列表，包含所有個體。

    def __set_population(self, population):
        """ 設置整個傳入的人口。警告：此方法會刪除人口中的所有先前個體。如果想保留舊個體，請使用 add_individual 方法。
        :param population: 個體或人口類的物件列表。
        :return: 無
        """
        try:
            if isinstance(population, list) and all(isinstance(ind, list) for ind in population):  # 如果傳入的對象是染色體列表
                self.population = []  # 重設人口
                for individual in population:
                    self.add_individual(individual)
            elif isinstance(population, list) and all(isinstance(ind, Individual) for ind in population):  # 如果傳入的對象是個體列表
                self.population = population
            elif isinstance(population, Population) and all(isinstance(ind, Individual) for ind in population.population):  # 如果傳入的是人口類的對象
                self.population = population.population
            else:
                raise ValueError()
        except ValueError:
            raise ValueError('人口必須是個體類的個體列表或染色體列表。')
        except Exception as e:
            raise Exception(str(e) + '\n' + '人口必須是個體類的個體列表或人口對象。')

    def __kill_and_reset_whole_population(self, new_population):
        """ 這是一個稍微複雜的方法。如果要創建一個新一代的人口，直接使用現有個體的對象重設其值會更快。
        :param new_population: 個體或人口類的物件列表。
        :return: 無
        """
        if not hasattr(new_population, '__len__'):
            raise ValueError('傳入的參數必須是染色體列表、個體（Individual類）或完整的人口。')
        elif len(self.population) != len(new_population):
            raise ValueError('新人口必須與現有人口有相同的個體數量。當前人口中有 {} 個個體。'.format(len(self.population)))
        else:
            try:
                if isinstance(new_population, list) and all(isinstance(ind, list) for ind in new_population):  # 如果傳入的是染色體列表
                    for i in range(len(self.population)):
                        self.population[i].kill_and_reset(new_population[i])
                elif isinstance(new_population, list) and all(isinstance(ind, Individual) for ind in new_population):  # 如果傳入的是個體列表
                    for i in range(len(self.population)):
                        self.population[i].kill_and_reset(new_population[i].chromosome)
                elif isinstance(new_population, Population) and all(isinstance(ind, Individual) for ind in new_population.population):  # 如果傳入的是人口類對象
                    for i in range(len(self.population)):
                        self.population[i].kill_and_reset(new_population[i].chromosome)
                else:
                    raise ValueError()
            except ValueError:
                raise ValueError('人口必須是個體類的個體列表或染色體列表。')
            except Exception as e:
                raise Exception(str(e) + '\n' + '人口必須是個體類的個體列表或人口對象。')

    def add_individual(self, individual):
        """ 向人口中添加新個體。注意：如果添加新個體，人口可能會超過指定大小。
        :param individual: 個體類的個體或表示染色體的列表。
        :return: 無
        """
        if isinstance(individual, list):
            new_ind = Individual(individual)  # 創建新個體
            self.population.append(new_ind)  # 添加到人口
        elif isinstance(individual, Individual):
            self.population.append(individual)  # 直接添加到人口
        else:
            raise ValueError('參數必須是個體類的個體或代表染色體的列表。')

    def get_individual_by_id(self, id_individual):
        """ 通過ID返回個體。如果沒有這個ID的個體，返回None。
        :param id_individual: 個體的ID。
        :return: 找到的個體或None
        """
        if not isinstance(id_individual, str):
            raise ValueError('此方法必須接收個體的ID，該ID是字符串。')
        else:
            for individual in self.population:
                if individual._id == id_individual:
                    return individual
            return None  # 沒有找到該ID的個體

    def __calculate_normalized_fitness(self):
        """ 計算整個人口的標準化適應度（並將參數添加到每個個體的屬性normalized_fitness）。同樣的操作也適用於反向標準化適應度。
        """
        if any(ind.fitness_value is None for ind in self):
            self.__calculate_fitness_population()  # 計算個體的適應度
        max_v = max(ind.fitness_value for ind in self)
        min_v = min(ind.fitness_value for ind in self)
        if max_v != min_v:  # 避免除零錯誤
            for ind in self.population:
                normalized_fitness_value = (ind.fitness_value - min_v) / (max_v - min_v)  # 計算標準化適應度
                ind.set_inverse_normalized_fitness_value(1 - normalized_fitness_value)  # 設置反向標準化適應度
                ind.set_normalized_fitness_value(normalized_fitness_value)  # 設置標準化適應度
        else:  # 如果所有個體的適應度相同
            for ind in self.population:
                ind.set_inverse_normalized_fitness_value(1)  # 設置反向標準化適應度為1
                ind.set_normalized_fitness_value(1)  # 設置標準化適應度為1

    @abstractmethod
    def __calculate_fitness_population(self):
        """ 計算人口中所有個體的適應度並設置這個屬性給每個個體。 """
        pass

    @abstractmethod
    def __generate_population(self):
        """ 生成一個新的人口並將其添加到屬性人口中。 """
        pass

    @abstractmethod
    def __sort_population(self):
        """ 按其適應度對人口進行排序。 """
        pass

    def __calculate_fitness_and_sort(self):
        """ 計算整個人口的適應度，然後計算標準化適應度，然後根據這個適應度對人口進行排序。 """
        self.__calculate_fitness_population()  # 計算適應度
        self.__calculate_normalized_fitness()  # 計算標準化適應度
        self.__sort_population()  # 排序人口

    @abstractmethod
    def __get_next_generation(self):
        """ 用於計算下一代。 """
        pass

    @abstractmethod
    def best_individual(self):
        """ 返回最佳個體。 """
        pass

    def get_population(self):
        """ 獲取人口的方法。 """
        self.__calculate_fitness_population()  # 計算適應度
        self.__calculate_normalized_fitness()  # 計算標準化適應度
        self.__sort_population()  # 排序人口
        return self.population

    def __len__(self):
        return len(self.population)

    def __iter__(self):
        return iter(self.population)

    def __getitem__(self, pos):
        return self.population[pos]
