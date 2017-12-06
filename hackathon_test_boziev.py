import re

def calculate(expr):
	ops = {
		"+": (lambda x,y: x+y),
		"-": (lambda x,y: re.sub('{0}$'.format(y), '', x)),
		"*": (lambda x,y: ''.join(map(lambda x,y: (x or '') + (y or ''), list(x), list(y)))),
		"/": (lambda x,y: ''.join(map(lambda x,y: x[0] if x[1] == y else ''.join(x), zip(list(x)[0:len(y)*2:2],list(x)[1:len(y)*2:2]),list(y))) + ''.join(list(x)[len(y)*2::]))
	}

	arr = [part.strip() for part in re.split("([-+*/])", expr) if part]

	operand_index = 1
	for index, el in enumerate(arr):
		if el in ['*', '/']:
			operand_index = index
			break

	if len(arr) == 1:
		return expr
	elif (len(arr) > 3):
		calculation = ops[arr[operand_index]](arr[operand_index-1],arr[operand_index+1])
		del arr[operand_index-1: operand_index+2]
		arr.insert(operand_index-1, calculation)
		expr = ''.join(arr)
		return calculate(expr)
	else:
		return ops[arr[1]](arr[0],arr[2])


def calculate_brackets(expr):
	regex = r"\((.*?)\)"
	matches = re.findall(regex, expr)

	if len(matches) > 0:
		match = re.sub(r'[()]', '', matches[0])
		result = calculate(match)
		expr = expr.replace(match, result)
		expr = expr.replace('({0})'.format(result), result)
		return calculate_brackets(expr)
	else:
		return calculate(expr)


def ingos(expr):
	result = calculate_brackets(expr)
	edge_row = str((len(result) + 6) * '*')
	interim_row = '*' + str((len(result) + 4) * ' ') + '*'
	result_row = '*  {0}  *'.format(result)
	return '\n{0}\n{1}\n{2}\n{1}\n{0}'.format(edge_row, interim_row , result_row)


# expr = '((index - ex) - d) + gst * osr + (an + k + oh) / (n + o)'
expr = raw_input('Please enter string to calculate:\n--> ')
print ingos(expr)
