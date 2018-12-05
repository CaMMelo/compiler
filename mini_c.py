from sys import argv
from parser import Parser
from virtual_machine import MiniCVM

if __name__ == '__main__':
	parser = Parser(argv[1])
	codigo = parser.parse()

	#for c in codigo:
	#	print(c)
	
	vm = MiniCVM()
	vm.exec(codigo)
