import sys
import io

from temporary import temporary

def check_output(func_input: list[str],output: list[str]):
	original_stdin = sys.stdin

	sys_stdout = sys.stdout
	func_output=[]
	for i in func_input:
		print(i)
		buffer = io.StringIO()
		print(buffer.getvalue())
		sys.stdout = buffer
		sys.stdin = io.StringIO(i)
		temporary()
		print(buffer.getvalue())
		func_output.append(buffer.getvalue().strip())

	sys.stdout = sys_stdout
	sys.stdin = original_stdin
	print(func_output)

check_output(["Алиса","123","ВАЫВАВЫА"],["Алиса","123","ВАЫВАВЫА"])