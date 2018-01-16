import itertools

def printTriangle(triangle):
	max_cols = len(triangle[-1])
	output = ''.join(['{:15}'.format(str(x)) for x in range(max_cols+1)]) + '\n'
	for index, row in enumerate(triangle):
		output += '{:15}'.format(str(index + 1))
		for element in row:
			output += '{:15}'.format(str(element))
		output += '\n'
	print output

def parseProductions(productions):
	parsedProductions = {}
	for production in productions:
		rhs, lhs = production.split('->')
		splitted_lhs = lhs.split('|')
		for each_splitted_lhs in splitted_lhs:
			if each_splitted_lhs in parsedProductions:
				parsedProductions[each_splitted_lhs].append(rhs)
			else:
				parsedProductions[each_splitted_lhs] = [rhs]
	return parsedProductions

def getCartisianProduct(array1, array2):
	cartesianProduct = []
	for element in itertools.product(array1, array2):
		cartesianProduct.append(''.join(element))
	return cartesianProduct

def getValidProductions(language_productions, all_productions):
	validProductions = []
	for rhs in all_productions:
		if rhs in language_productions:
			validProductions += list(set(language_productions[rhs]) - set(validProductions))
	return validProductions

def populateTriangle(triangle, test_string, parsedProductions):
	size = len(test_string)

	for row in range(size-1, -1, -1):
		for col in range(row+1):

			if row == size - 1:
				character = test_string[col]
				if character in parsedProductions:
					triangle[row][col] = parsedProductions[character]
			else:
				vertical_row, vertical_col = size - 1, col
				diag_row, diag_col = row + 1, col + 1
				completeCartesianProduct = []

				while vertical_row > row and diag_col < size and diag_row < size:
					array1 = triangle[vertical_row][vertical_col]
					array2 = triangle[diag_row][diag_col]
					cartesianProduct = getCartisianProduct(array1, array2)
					completeCartesianProduct += cartesianProduct
					vertical_row -= 1
					diag_row += 1
					diag_col += 1

				validProductions = getValidProductions(parsedProductions, completeCartesianProduct)
				triangle[row][col] = validProductions

	printTriangle(triangle)
	return True if 'S' in triangle[0][0] else False

def isStringInLanguage(string, parsedProductions):
	size = len(string)
	triangle = [[[] for x in range(y+1)] for y in range(size)]
	return populateTriangle(triangle, string, parsedProductions)


def main():
	grammar = raw_input('Enter the grammar in CNF form productions separated by space : ').strip().split(' ')
	test_string = list(raw_input('Enter the test string : ').strip())
	parsedProductions = parseProductions(grammar)
	result = isStringInLanguage(test_string, parsedProductions)
	print "Result : ", result

if __name__ == '__main__':
	main()