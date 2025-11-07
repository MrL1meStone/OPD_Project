from random import randint, choice
from Testing.randfuncs import randstr


def second(lst):
	return str(sum(list(map(int, lst.split(" ")))))


def third(a):
	return str(sum(ch.lower() in "aeiouаеёиоуыэюя" for ch in a))


def fourth(a):
	s = a.lower().replace(" ", "")
	return str(s == s[::-1])


def fifth(lst):
	lst = list(map(int, lst.split()))
	return str([i**2 for i in lst])


def sixth(a):
	return str("".join("*" if ch.isdigit() else ch for ch in a))


def seventh(a):
	return str([word for word in a.split() if len(word) > 3])


def eighth(a):
	result = {}
	for ch in a:
		result[ch] = result.get(ch, 0) + 1
	return str(result)


def nineth(lst):
	lst = lst.split()
	return str(list(dict.fromkeys(lst)))


def tenth(a, b):
	return str(a in range(0, b + 1))


normal_questions = [
	{
		"text": 'Введите число и выведите четное оно или нет',
		"func": lambda a: str("четное" if a % 2 == 0 else "нечетное"),
		"args": lambda: {'a': str(randint(1, 1000))}
	},
	{
		"text": "Введите несколько чисел через пробел и найдите их сумму.",
		"func": second,
		"args": lambda: {'lst': " ".join([str(randint(-50, 50)) for _ in range(randint(3, 10))])}
	},
	{
		"text": "Введите строку и узнайте, сколько в ней гласных букв.",
		"func": third,
		"args": lambda: {'a': randstr()}
	},
	{
		"text": "Введите строку и проверьте, является ли она палиндромом.",
		"func": fourth,
		"args": lambda: {'a': choice(["казак", "дом", "шалаш", "python", "madam"])}
	},
	{
		"text": "Введите несколько чисел через пробел и выведите их квадраты.",
		"func": fifth,
		"args": lambda: {'lst': " ".join([str(randint(1, 10)) for _ in range(randint(3, 8))])}
	},
	{
		"text": "Введите строку и замените все цифры символом *.",
		"func": sixth,
		"args": lambda: {'a': "".join(choice("abc123xyz") for _ in range(randint(5, 12)))}
	},
	{
		"text": "Введите несколько слов и выведите те, длина которых больше 3 символов.",
		"func": seventh,
		"args": lambda: {'a': " ".join([randstr(randint(2, 6)) for _ in range(randint(4, 8))])}
	},
	{
		"text": "Введите строку и выведите, сколько раз встречается каждый символ.",
		"func": eighth,
		"args": lambda: {'a': randstr()}
	},
	{
		"text": "Введите список слов и удалите из него дубликаты.",
		"func": nineth,
		"args": lambda: {'lst': " ".join([choice(["apple", "banana", "apple", "pear", "banana", "kiwi"]) for _ in range(randint(5, 8))])}
	},
	{
		"text": "Введите два числа: проверьте, входит ли первое в диапазон от 0 до второго.",
		"func": tenth,
		"args": lambda: {'a': randint(0, 10), 'b': randint(5, 15)}
	}
]
