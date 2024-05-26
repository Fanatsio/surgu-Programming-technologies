import heapq

# ---- Основные классы кодирования Хаффмана ----

# Кодирует символы и записывает в поток битов, закодированный по Хаффману.
class HuffmanEncoder:
	
	# Создает кодировщик Хаффмана на основе данного потока битового вывода.
	def __init__(self, bitout):
		# Исходный поток битового вывода
		self.output = bitout
		# Дерево кодов, которое будет использоваться в следующей операции записи. 
		# Должно быть задано подходящее значение перед вызовом write(). Дерево может быть изменено
		# после кодирования каждого символа, если кодировщик и декодировщик имеют
		# одно и то же дерево в той же точке потока кода.
		self.codetree = None
	
	
	# Кодирует данный символ и записывает в поток битового вывода, закодированный по Хаффману.
	def write(self, symbol):
		if not isinstance(self.codetree, CodeTree):
			raise ValueError("Неверное текущее дерево кода")
		bits = self.codetree.get_code(symbol)
		for b in bits:
			self.output.write(b)



# Читает из потока битов, закодированного по Хаффману, и декодирует символы.
class HuffmanDecoder:
	
	# Создает декодировщик Хаффмана на основе данного потока битового ввода.
	def __init__(self, bitin):
		# Исходный поток битового ввода
		self.input = bitin
		# Дерево кодов, которое будет использоваться в следующей операции чтения. 
		# Должно быть задано подходящее значение перед вызовом read(). Дерево может быть изменено
		# после декодирования каждого символа, если кодировщик и декодировщик имеют
		# одно и то же дерево в той же точке потока кода.
		self.codetree = None
	
	
	# Читает из входного потока для декодирования следующего символа, закодированного по Хаффману.
	def read(self):
		if not isinstance(self.codetree, CodeTree):
			raise ValueError("Неверное текущее дерево кода")
		currentnode = self.codetree.root
		while True:
			temp = self.input.read_no_eof()
			if   temp == 0: nextnode = currentnode.leftchild
			elif temp == 1: nextnode = currentnode.rightchild
			else: raise AssertionError("Неверное значение от read_no_eof()")
			
			if isinstance(nextnode, Leaf):
				return nextnode.symbol
			elif isinstance(nextnode, InternalNode):
				currentnode = nextnode
			else:
				raise AssertionError("Неверный тип узла")



# Таблица частот символов. Изменяемая. Значения символов нумеруются
# от 0 до symbolLimit-1. Таблица частот в основном используется так:
# 0. Собираются частоты символов в потоке, который мы хотим сжать.
# 1. Построение дерева кодов, которое является статически оптимальным для текущих частот.
class FrequencyTable:
	
	# Создает таблицу частот из данной последовательности частот.
	# Длина последовательности должна быть не менее 2, и каждое значение должно быть неотрицательным.
	def __init__(self, freqs):
		self.frequencies = list(freqs)  # Создает копию
		if len(self.frequencies) < 2:
			raise ValueError("Необходимо не менее 2 символов")
		if any(x < 0 for x in self.frequencies):
			raise ValueError("Отрицательная частота")
	
	
	# Возвращает количество символов в этой таблице частот. Результат всегда не менее 2.
	def get_symbol_limit(self):
		return len(self.frequencies)
	
	
	# Возвращает частоту данного символа в этой таблице частот. Результат всегда неотрицателен.
	def get(self, symbol):
		self._check_symbol(symbol)
		return self.frequencies[symbol]
	
	
	# Задает частоту данного символа в этой таблице частот данному значению.
	def set(self, symbol, freq):
		self._check_symbol(symbol)
		if freq < 0:
			raise ValueError("Отрицательная частота")
		self.frequencies[symbol] = freq
	
	
	# Увеличивает частоту данного символа в этой таблице частот.
	def increment(self, symbol):
		self._check_symbol(symbol)
		self.frequencies[symbol] += 1
	
	
	# Тихо возвращается, если 0 <= symbol < len(frequencies), в противном случае вызывает исключение.
	def _check_symbol(self, symbol):
		if 0 <= symbol < len(self.frequencies):
			return
		else:
			raise ValueError("Символ вне диапазона")
	
	
	# Возвращает строковое представление этой таблицы частот,
	# полезно только для отладки, и формат может измениться.
	def __str__(self):
		result = ""
		for (i, freq) in enumerate(self.frequencies):
			result += "{}\t{}\n".format(i, freq)
		return result
	
	
	# Возвращает дерево кодов, которое является оптимальным для частот символов в этой таблице.
	# Дерево всегда содержит не менее 2 листьев (даже если они исходят от символов с
	# 0 частотой), чтобы избежать вырожденных деревьев. Обратите внимание, что оптимальные деревья не уникальны.
	def build_code_tree(self):
		# Обратите внимание, что если два узла имеют одинаковую частоту, то
		# разрыв производится по тому, какое дерево содержит самый низкий символ. Таким образом,
		# алгоритм имеет детерминированный вывод и не полагается на очередь, чтобы
		# разрешить разрыв.
		# Каждый элемент в очереди с приоритетом представляет собой кортеж типа (int частота,
		# int наименьшийСимвол, Node узел). Согласно правилам Python, кортежи упорядочиваются по возрастанию
		# по наименьшему отличающемуся индексу, например, (0, 0) < (0, 1) < (0, 2) < (1, 0) < (1, 1).
		pqueue = []
		
		# Добавить листья для символов с ненулевой частотой
		for (i, freq) in enumerate(self.frequencies):
			if freq > 0:
				heapq.heappush(pqueue, (freq, i, Leaf(i)))
		
		# Добавьте символы с нулевой частотой, пока в очереди не окажется не менее 2 элементов
		for (i, freq) in enumerate(self.frequencies):
			if len(pqueue) >= 2:
				break
			if freq == 0:
				heapq.heappush(pqueue, (freq, i, Leaf(i)))
		assert len(pqueue) >= 2
		
		# Повторяйте объединение двух узлов с наименьшей частотой
		while len(pqueue) > 1:
			x = heapq.heappop(pqueue)  # Кортеж типа (частота, наименьший символ, объект узла)
			y = heapq.heappop(pqueue)  # Кортеж типа (частота, наименьший символ, объект узла)
			z = (x[0] + y[0], min(x[1], y[1]), InternalNode(x[2], y[2]))  # Создать новый кортеж
			heapq.heappush(pqueue, z)
		
		# Вернуть оставшийся узел
		return CodeTree(pqueue[0][2], len(self.frequencies))



# Бинарное дерево, которое представляет собой отображение между символами
# и двоичными строками. Существует два основных варианта использования дерева кодов:
# - Прочитайте поле корня и пройдите по дереву, чтобы извлечь необходимую информацию.
# - Вызовите getCode(), чтобы получить двоичный код для конкретного кодируемого символа.
# Путь к листовому узлу определяет код символа этого листа. Начиная с корня, переходя
# к левому потомку, представляет 0, а к правому потомку - 1. Ограничения:
# - Корень должен быть внутренним узлом, и дерево конечно.
# - Ни одно значение символа не встречается в нескольких листьях.
# - Не каждое возможное значение символа должно быть в дереве.
# Проиллюстрированный пример:
#   Коды Хаффмана:
#     0: Символ A
#     10: Символ B
#     110: Символ C
#     111: Символ D
#   Дерево кодов:
#       .
#      / \
#     A   .
#        / \
#       B   .
#          / \
#         C   D
class CodeTree:
	
	# Создает дерево кодов из данного дерева узлов и заданного предела символов.
	# Каждый символ в дереве должен иметь значение строго меньше предела символов.
	def __init__(self, root, symbollimit):
		# Рекурсивная вспомогательная функция
		def build_code_list(node, prefix):
			if isinstance(node, InternalNode):
				build_code_list(node.leftchild , prefix + (0,))
				build_code_list(node.rightchild, prefix + (1,))
			elif isinstance(node, Leaf):
				if node.symbol >= symbollimit:
					raise ValueError("Символ превышает предел символов")
				if self.codes[node.symbol] is not None:
					raise ValueError("Символ имеет более одного кода")
				self.codes[node.symbol] = prefix
			else:
				raise AssertionError("Неверный тип узла")
		
		if symbollimit < 2:
			raise ValueError("Необходимо не менее 2 символов")
		# Корневой узел этого дерева кодов
		self.root = root
		# Хранит код для каждого символа или None, если у символа нет кода.
		# Например, если символ 5 имеет код 10011, то codes[5] - это кортеж (1,0,0,1,1).
		self.codes = [None] * symbollimit
		build_code_list(root, ())  # Заполнить 'codes' соответствующими данными
	
	
	# Возвращает код Хаффмана для данного символа, который является последовательностью 0 и 1.
	def get_code(self, symbol):
		if symbol < 0:
			raise ValueError("Недопустимый символ")
		elif self.codes[symbol] is None:
			raise ValueError("Нет кода для данного символа")
		else:
			return self.codes[symbol]
	
	
	# Возвращает строковое представление этого дерева кодов,
	# полезно только для отладки, и формат может измениться.
	def __str__(self):
		# Рекурсивная вспомогательная функция
		def to_str(prefix, node):
			if isinstance(node, InternalNode):
				return to_str(prefix + "0", node.leftchild) + to_str(prefix + "0", node.rightchild)
			elif isinstance(node, Leaf):
				return "Code {}: Symbol {}\n".format(prefix, node.symbol)
			else:
				raise AssertionError("Неверный тип узла")
		
		return to_str("", self.root)



# Узел в дереве кодов. Этот класс имеет ровно два подкласса: InternalNode, Leaf.
class Node:
	pass


# Внутренний узел в дереве кодов. Имеет два узла в качестве потомков.
class InternalNode(Node):
	def __init__(self, left, right):
		if not isinstance(left, Node) or not isinstance(right, Node):
			raise TypeError()
		self.leftchild = left
		self.rightchild = right


# Листовой узел в дереве кодов. Имеет значение символа.
class Leaf(Node):
	def __init__(self, sym):
		if sym < 0:
			raise ValueError("Значение символа должно быть неотрицательным")
		self.symbol = sym



# Канонический код Хаффмана, который описывает только длину кода
# каждого символа. Длина кода 0 означает, что для символа нет кода.
# Двоичные коды для каждого символа могут быть восстановлены из информации о длине.
# В этой реализации лексикографически более низкие двоичные коды присваиваются символам
# с меньшей длиной кода, разрывая равенство по меньшим значениям символов. Например:
#   Длины кодов (канонический код):
#     Символ A: 1
#     Символ B: 3
#     Символ C: 0 (нет кода)
#     Символ D: 2
#     Символ E: 3
#   Отсортированные длины и символы:
#     Символ A: 1
#     Символ D: 2
#     Символ B: 3
#     Символ E: 3
#     Символ C: 0 (нет кода)
#   Сгенерированные коды Хаффмана:
#     Символ A: 0
#     Символ D: 10
#     Символ B: 110
#     Символ E: 111
#     Символ C: None
#   Коды Хаффмана, отсортированные по символу:
#     Символ A: 0
#     Символ B: 110
#     Символ C: None
#     Символ D: 10
#     Символ E: 111
class CanonicalCode:
	
	# Создает канонический код одним из двух способов:
	# - CanonicalCode(codelengths):
	#   Создает канонический код Хаффмана из данного массива длин кодов символов.
	#   Каждая длина кода должна быть неотрицательной. Длина кода 0 означает, что для символа нет кода.
	#   Набор длин кодов должен представлять собой правильное полное дерево кода Хаффмана.
	#   Примеры длин кодов, которые приводят к недостаточным деревьям кода Хаффмана:
	#   * [1]
	#   * [3, 0, 3]
	#   * [1, 2, 3]
	#   Примеры длин кодов, которые приводят к правильным полным деревьям кода Хаффмана:
	#   * [1, 1]
	#   * [2, 2, 1, 0, 0, 0]
	#   * [3, 3, 3, 3, 3, 3, 3, 3]
	#   Примеры длин кодов, которые приводят к избыточным деревьям кода Хаффмана:
	#   * [1, 1, 1]
	#   * [1, 1, 2, 2, 3, 3, 3, 3]
	# - CanonicalCode(tree, symbollimit):
	#   Создает канонический код из данного дерева кодов.
	def __init__(self, codelengths=None, tree=None, symbollimit=None):
		if codelengths is not None and tree is None and symbollimit is None:
			# Проверка базовой действительности
			if len(codelengths) < 2:
				raise ValueError("Необходимо не менее 2 символов")
			if any(cl < 0 for cl in codelengths):
				raise ValueError("Недопустимая длина кода")
			
			# Копировать один раз и проверить действительность дерева
			codelens = sorted(codelengths, reverse=True)
			currentlevel = codelens[0]
			numnodesatlevel = 0
			for cl in codelens:
				if cl == 0:
					break
				while cl < currentlevel:
					if numnodesatlevel % 2 != 0:
						raise ValueError("Недостаточное дерево кода Хаффмана")
					numnodesatlevel //= 2
					currentlevel -= 1
				numnodesatlevel += 1
			while currentlevel > 0:
				if numnodesatlevel % 2 != 0:
					raise ValueError("Недостаточное дерево кода Хаффмана")
				numnodesatlevel //= 2
				currentlevel -= 1
			if numnodesatlevel < 1:
				raise ValueError("Недостаточное дерево кода Хаффмана")
			if numnodesatlevel > 1:
				raise ValueError("Избыточное дерево кода Хаффмана")
			
			# Копировать еще раз
			self.codelengths = list(codelengths)
		
		elif tree is not None and symbollimit is not None and codelengths is None:
			# Рекурсивный вспомогательный метод
			def build_code_lengths(node, depth):
				if isinstance(node, InternalNode):
					build_code_lengths(node.leftchild , depth + 1)
					build_code_lengths(node.rightchild, depth + 1)
				elif isinstance(node, Leaf):
					if node.symbol >= len(self.codelengths):
						raise ValueError("Символ превышает предел символов")
					# Примечание. CodeTree уже имеет проверенное ограничение, которое не допускает символ в нескольких листьях
					if self.codelengths[node.symbol] != 0:
						raise AssertionError("Символ имеет более одного кода")
					self.codelengths[node.symbol] = depth
				else:
					raise AssertionError("Неверный тип узла")
			
			if symbollimit < 2:
				raise ValueError("Необходимо не менее 2 символов")
			self.codelengths = [0] * symbollimit
			build_code_lengths(tree.root, 0)
		
		else:
			raise ValueError("Неверные аргументы")
	
	
	# Возвращает предел символов для этого канонического кода Хаффмана.
	# Таким образом, этот код охватывает значения символов от 0 до symbolLimit-1.
	def get_symbol_limit(self):
		return len(self.codelengths)
	
	
	# Возвращает длину кода данного значения символа. Результат равен 0
	# если у символа нет кода; в противном случае результат - положительное число.
	def get_code_length(self, symbol):
		if 0 <= symbol < len(self.codelengths):
			return self.codelengths[symbol]
		else:
			raise ValueError("Символ вне диапазона")
	
	
	# Возвращает каноническое дерево кодов для этого канонического кода Хаффмана.
	def to_code_tree(self):
		nodes = []
		for i in range(max(self.codelengths), -1, -1):  # Спуститься по длинам кодов
			assert len(nodes) % 2 == 0
			newnodes = []
			
			# Добавить листья для символов с положительной длиной кода i
			if i > 0:
				for (j, codelen) in enumerate(self.codelengths):
					if codelen == i:
						newnodes.append(Leaf(j))
			
			# Объединить пары узлов с предыдущего более глубокого уровня
			for j in range(0, len(nodes), 2):
				newnodes.append(InternalNode(nodes[j], nodes[j + 1]))
			nodes = newnodes
		
		assert len(nodes) == 1
		return CodeTree(nodes[0], len(self.codelengths))



# ---- Потоки ввода-вывода ориентированные на биты ----

# Поток битов, который можно читать. Поскольку они поступают из исходного байтового потока,
# общее количество битов всегда кратно 8. Биты читаются в порядке старших разрядов.
class BitInputStream:
	
	# Создает поток битового ввода на основе данного байтового входного потока.
	def __init__(self, inp):
		# Исходный байтовый поток для чтения
		self.input = inp
		# Либо в диапазоне [0x00, 0xFF], если биты доступны, либо -1, если достигнут конец потока
		self.currentbyte = 0
		# Количество оставшихся битов в текущем байте, всегда от 0 до 7 (включительно)
		self.numbitsremaining = 0
	
	
	# Читает бит из этого потока. Возвращает 0 или 1, если бит доступен, или -1, если
	# достигнут конец потока. Конец потока всегда происходит на границе байта.
	def read(self):
		if self.currentbyte == -1:
			return -1
		if self.numbitsremaining == 0:
			temp = self.input.read(1)
			if len(temp) == 0:
				self.currentbyte = -1
				return -1
			self.currentbyte = temp[0]
			self.numbitsremaining = 8
		assert self.numbitsremaining > 0
		self.numbitsremaining -= 1
		return (self.currentbyte >> self.numbitsremaining) & 1
	
	
	# Читает бит из этого потока. Возвращает 0 или 1, если бит доступен, или вызывает EOFError
	# если достигнут конец потока. Конец потока всегда происходит на границе байта.
	def read_no_eof(self):
		result = self.read()
		if result != -1:
			return result
		else:
			raise EOFError()
	
	
	# Закрывает этот поток и исходный входной поток.
	def close(self):
		self.input.close()
		self.currentbyte = -1
		self.numbitsremaining = 0



# Поток, в который можно записывать биты. Поскольку они записываются в исходный
# байтовый поток, конец потока дополняется 0 до кратного 8 бит.
# Биты записываются в порядке старших разрядов.
class BitOutputStream:
	
	# Создает поток битового вывода на основе данного байтового выходного потока.
	def __init__(self, out):
		self.output = out  # Исходный байтовый поток для записи
		self.currentbyte = 0  # Накопленные биты для текущего байта, всегда в диапазоне [0x00, 0xFF]
		self.numbitsfilled = 0  # Количество накопленных битов в текущем байте, всегда от 0 до 7 (включительно)
	
	
	# Записывает бит в поток. Данный бит должен быть 0 или 1.
	def write(self, b):
		if b not in (0, 1):
			raise ValueError("Аргумент должен быть 0 или 1")
		self.currentbyte = (self.currentbyte << 1) | b
		self.numbitsfilled += 1
		if self.numbitsfilled == 8:
			towrite = bytes((self.currentbyte,))
			self.output.write(towrite)
			self.currentbyte = 0
			self.numbitsfilled = 0
	
	
	# Закрывает этот поток и исходный выходной поток. Если вызывается, когда этот
	# поток битов не находится на границе байта, то минимальное количество "0" битов
	# (от 0 до 7) записываются в виде заполнения, чтобы достичь следующей границы байта.
	def close(self):
		while self.numbitsfilled != 0:
			self.write(0)
		self.output.close()