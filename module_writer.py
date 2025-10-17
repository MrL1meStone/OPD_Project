import os

def make_module(text: list[str]):
	if os.path.exists('temporary.py'):
		mode = "w"
	else:
		mode = "a"
	with open('temporary.py',mode) as module:
		module.write('def temporary():\n')
		for line in text:
			module.write(f'    {line}\n')
