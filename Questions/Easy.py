from random import randint

from modules.randfuncs import randstr


def first(a):
	return str(a)

def second(a,b):
	return str(a + b)

def third(lst):
	return str([(i.capitalize(),i.lower(),i.upper()) for i in lst.split(" ")])

def fourth(lst):
	return str(dict(zip(("id","name","age"),lst.split(" "))))

def fifth(lst):
	lst=lst.split(" ")
	return str((min(lst),max(lst)))

def sixth(a, b):
	a = a.split(" ")
	b = b.split(" ")
	return str(list(set(a).intersection(set(b))).sort())

def seventh(lst):
	lst = lst.split(" ")
	return str((lst[0], lst[-1]))

def eighth(a, b):
	return str(a.count(b))

def ninth(a,b):
	return str(a**b)

def tenth(a,b):
	return a%b==0

easy_questions=[
	{   "text": 'Получите переменную через ввод в консоль и выведите ее',
		"func": first,
	    "args": {'a': randstr()}
	},
	{
		"text": 'Получите 2 переменные через консоль и выведите их сумму',
		"func": second,
		"args": {'a': randint(1, 10 ** 6), 'b': randint(1, 10 ** 6)}
	},
	{
		"text": 'Получите список строк и выведите список наборов (кортежей) вариантов строк:\n'
		        'Строка с большой буквы\n'
		        'строка маленькими буквами\n',
				'СТРОКА БОЛЬШИМИ БУКВАМИ'
		"func": third,
		"args": {'lst': " ".join([randstr() for i in range(randint(1, 20))])}
	},
	{
		"text": 'Получите список в котором на первом месте стоит id,на 2 - name, на 3 - age и'
		        ' запакуйте с соответствующими ключами в словарь и выведите его',
		"func": fourth,
		"args": {"lst": " ".join([str(randint(1,10**12))] + [randstr() for j in range(2)])}
	},
	{
		"text": 'Выведите кортеж из наименьшего и наибольшего значения списка',
		"func": fifth,
		"args": {'lst': " ".join([str(randint(-5*10**5,5*10**5)) for _ in range(randint(1,5))])}
	},
	{
		"text": 'Выведите список элементов, находящихся в двух списках, введенных через пробел',
		"func": sixth,
		"args": {'a': " ".join([str(randint(-5 * 10 ** 5, 5 * 10 ** 5)) for _ in range(randint(1, 5))]),
		         'b': " ".join([str(randint(-5 * 10 ** 5, 5 * 10 ** 5)) for _ in range(randint(1, 5))])}
	},
	{
		"text": 'Выведите первый и последний элемент списка',
		"func": seventh,
		"args": {'lst' : [randint(-5*10**5,5*10**5) for _ in range(randint(1,5))]}
	},
	{
		"text": 'Выведите сколько раз встречается 2 строка в первой',
		"func": eighth,
		"args": {'a' : randstr(),'b' : randstr()}
	},
	{
		"text": 'Выведите первое введенное число в степени 2',
		"func": ninth,
		"args": {'a': randint(1,9),'b': randint(4,10)}
	},
	{
		"text": 'Выведите делится ли первое число на второе',
		"func": tenth,
		"args": {'a': randint(1,999),'b': randint(1,100)}
	}]