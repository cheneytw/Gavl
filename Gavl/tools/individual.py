import uuid  # 引入 uuid 模塊來生成唯一識別碼
import numpy as np  # 引入 numpy 用於進行數值計算


class Individual:
    """ 個體類，包含染色體、適應度和正規化適應度等屬性。
    """

    def __init__(self, chromosome):
        """ 構造函數。

        :param chromosome: (list of genes) 個體的染色體。
        """
        if type(chromosome) != list:
            raise AttributeError('染色體必須是基因的列表')
        else:
            self.chromosome = chromosome  # 存儲染色體
            self._id = str(uuid.uuid4())  # 為每個個體生成一個唯一的 ID
            self.fitness_value = None  # 適應度值將在評估時填充
            self.normalized_fitness_value = None  # 存儲相對於族群的正規化適應度
            self.inverse_normalized_fitness_value = None  # 存儲相對於族群的逆正規化適應度

    def set_new_chromosome(self, chromosome):
        """ 設置新染色體的方法。

        :param chromosome: (list of genes) 個體的染色體。
        """
        if type(chromosome) != list:
            raise AttributeError('染色體必須是基因的列表')
        else:
            self.chromosome = chromosome  # 更新染色體

    def set_fitness_value(self, fitness_value):
        """ 設置適應度值的方法。

        :param fitness_value: (float) 適應度值。
        """
        if type(fitness_value) in [int, float, np.float64]:
            self.fitness_value = fitness_value
        else:
            raise ValueError('適應度值必須是整數或浮點數。接收到的類型為 {}。'.format(type(fitness_value)))

    def set_normalized_fitness_value(self, normalized_fitness_value):
        """ 設置正規化適應度值的方法。

        :param normalized_fitness_value: (float) 正規化適應度值。
        """
        if type(normalized_fitness_value) in [int, float, np.float64]:
            self.normalized_fitness_value = normalized_fitness_value
        else:
            raise ValueError('正規化適應度值必須是整數或浮點數。接收到的類型為 {}。'.format(type(normalized_fitness_value)))

    def set_inverse_normalized_fitness_value(self, inverse_normalized_fitness_value):
        """ 設置逆正規化適應度值的方法。

        :param inverse_normalized_fitness_value: (float) 逆正規化適應度值。
        """
        if type(inverse_normalized_fitness_value) in [int, float, np.float64]:
            self.inverse_normalized_fitness_value = inverse_normalized_fitness_value
        else:
            raise ValueError('逆正規化適應度值必須是整數或浮點數。接收到的類型為 {}。'.format(type(inverse_normalized_fitness_value)))

    def calculate_fitness(self, fitness):
        """ 計算個體適應度的方法。

        :param fitness: (function) 評估適應度的函數。它的唯一參數是個體的染色體 (fitness(chromosome))，返回適應度值。
        """
        try:
            value = fitness(self.chromosome)  # 計算適應度值
            self.set_fitness_value(value)  # 設置適應度值
            return value
        except Exception as e:
            raise Exception(str(e) + '\n計算個體適應度時出錯')

    def kill_and_reset(self, chromosome):
        """ 重設個體的方法。如果要創建新一代的新個體，重設已有個體的值會比創建全新個體並取消引用舊個體更快。

        :param chromosome: (list of genes) 個體的染色體。
        """
        if type(chromosome) != list:
            raise AttributeError('染色體必須是基因的列表')
        else:
            self.chromosome = chromosome  # 更新染色體
            self.fitness_value = None  # 重設適應度值
            self.normalized_fitness_value = None  # 重設正規化適應度值
            self.inverse_normalized_fitness_value = None  # 重設逆正規化適應度值

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.chromosome == other.chromosome  # 比較是否相等

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.fitness < other.fitness  # 比較小於

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.fitness > other.fitness  # 比較大於

    def __repr__(self):
        return '{self.__class__.__name__}({self.chromosome})'.format(self=self)  # 定義對象的官方字串表示

    def __str__(self):
        return "Chromosome: {0} \nFitness: {1}".format(self.chromosome, self.fitness_value)  # 定義對象的字串表示，方便打印

    def __iter__(self):
        return iter(self.chromosome)  # 允許對染色體進行迭代

    def __len__(self):
        return len(self.chromosome)  # 返回染色體的長度

    def __getitem__(self, pos):
        return self.chromosome[pos]  # 允許索引訪問染色體
