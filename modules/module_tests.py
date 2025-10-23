import sys
import io

from temporary import temporary

def check_output(func_input: list, output: list[str]):
	original_stdin = sys.stdin

	sys_stdout = sys.stdout
	right_output=[]
	for i in func_input:
		buffer = io.StringIO()
		sys.stdout = buffer
		sys.stdin = io.StringIO(i)
		temporary()
		right_output.append(buffer.getvalue().strip() == output[i])

	sys.stdout = sys_stdout
	sys.stdin = original_stdin
	return not(False in right_output)

check_output(["Алиса","123","ВАЫВАВЫА"],["Алиса","123","ВАЫВАВЫА"])