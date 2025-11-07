import sys
import io
import traceback
from contextlib import redirect_stdout

def check_output(input_func, output_func):
	from Testing.temporary import temporary
	original_stdin = sys.stdin
	sys_stdout = sys.stdout
	is_right_output=[]
	for _ in range(5):
		input_data=input_func()
		print(input_data)
		f = io.StringIO()
		with redirect_stdout(f):
			sys.stdin = io.StringIO("\n".join(input_data.values()))
			try:
				temporary()
				out = f.getvalue()
				is_right_output.append(out.strip() == output_func(**input_data))
			except BaseException:
				sys.stdout = sys_stdout
				sys.stdin = original_stdin
				error = traceback.format_exc()
				return False, error

	sys.stdout = sys_stdout
	sys.stdin = original_stdin
	return False not in is_right_output,None
