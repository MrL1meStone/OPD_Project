from random import randint

from Testing.randfuncs import randstr

easy_questions=[
	{   "text": 'Получите переменную через ввод в консоль и выведите ее',
		"func": lambda x: str(x),
	    "args": lambda: {'a': randstr()}
	},
	{
		"text": 'Получите 2 переменные через консоль и выведите их сумму',
		"func": lambda x,y: str(x+y),
		"args": lambda: {'a': randint(1, 10 ** 6), 'b': randint(1, 10 ** 6)}
	},
	{
		"text": 'Получите список строк и выведите список наборов (кортежей) вариантов строк:\n'
		        'Строка с большой буквы, '
		        'строка маленькими буквами, ',
				'СТРОКА БОЛЬШИМИ БУКВАМИ'
		"func": lambda lst: str([(i.capitalize(),i.lower(),i.upper()) for i in lst.split(" ")]),
		"args": lambda: {'lst': " ".join([randstr() for _ in range(randint(1, 20))])}
	},
	{
		"text": 'Получите список в котором на первом месте стоит id,на 2 - name, на 3 - age и'
		        ' запакуйте с соответствующими ключами в словарь и выведите его',
		"func": lambda lst: str(dict(zip(("id","name","age"),lst.split(" ")))),
		"args": lambda: {"lst": " ".join([str(randint(1,10**12))] + [randstr(),randstr()])}
	},
	{
		"text": 'Выведите кортеж из наименьшего и наибольшего значения списка',
		"func": lambda lst: str((min(lst.split(" ")),max(lst.split(" ")))),
		"args": lambda: {'lst': " ".join([str(randint(-5*10**5,5*10**5)) for _ in range(randint(1,5))])}
	},
	{
		"text": 'Выведите список элементов, находящихся в двух списках, введенных через пробел',
		"func": lambda a,b: str(list(set(a.split(" ")).intersection(set(b.split(" ")))).sort()),
		"args": lambda: {'a': " ".join([str(randint(-5 * 10 ** 5, 5 * 10 ** 5)) for _ in range(randint(1, 5))]),
		         'b': " ".join([str(randint(-5 * 10 ** 5, 5 * 10 ** 5)) for _ in range(randint(1, 5))])}
	},
	{
		"text": 'Выведите первый и последний элемент списка',
		"func": lambda lst: str((lst.split(" ")[0], lst.split(" ")[-1])),
		"args": lambda: {'lst' : [randint(-5*10**5,5*10**5) for _ in range(randint(1,5))]}
	},
	{
		"text": 'Выведите сколько раз встречается 2 строка в первой',
		"func": lambda a,b: str(a.count(b)),
		"args": lambda: {'a' : randstr(),'b' : randstr()}
	},
	{
		"text": 'Выведите первое введенное число в степени второго',
		"func": lambda a,b: str(a**b),
		"args": lambda: {'a': randint(1,9),'b': randint(4,10)}
	},
	{
		"text": 'Выведите делится ли первое число на второе',
		"func": lambda a,b: str(a%b==0),
		"args": lambda: {'a': randint(1,999),'b': randint(1,100)}
	}]