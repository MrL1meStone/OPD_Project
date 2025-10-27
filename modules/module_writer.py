from os.path import exists

def make_module(text: str):
	if exists('modules/temporary.py'):
		mode = "w"
	else:
		mode = "a"
	with open('modules/temporary.py', mode) as module:
		module.write('def temporary():\n')
		text=text.split("\n")
		for line in text:
			module.write(f'	{line}\n')