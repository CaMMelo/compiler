from sys import argv
from parser import Parser


if __name__ == '__main__':
	parser = Parser(argv[1])
	codigo = parser.parse()

	for c in codigo:
		print(c)
