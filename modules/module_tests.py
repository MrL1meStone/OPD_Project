import sys
import io

from contextlib import redirect_stdout

from modules.temporary import temporary

def check_output(input_func, output_func: function):
	original_stdin = sys.stdin
	sys_stdout = sys.stdout
	is_right_output=[]
	for i in range(5):
		input_data=input_func()
		f = io.StringIO()
		with redirect_stdout(f):
			sys.stdin = io.StringIO(input_data)
			temporary()
		out = f.getvalue()
		is_right_output.append(out.strip() == output_func(input_data))

	sys.stdout = sys_stdout
	sys.stdin = original_stdin
	return False not in is_right_output
