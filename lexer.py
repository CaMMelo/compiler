import enum


class TokenTypeEnum(enum.Enum):

	ERROR			= enum.auto()
	EOF				= enum.auto()
	# palavras chave
	BREAK 			= enum.auto()	# 'break'
	CONTINUE 		= enum.auto()	# 'continue'
	ELSE 			= enum.auto()	# 'else'
	FLOAT 			= enum.auto()	# 'float'
	FOR 			= enum.auto()	# 'for'
	IF 				= enum.auto()	# 'if'
	INT 			= enum.auto()	# 'int'
	PRINT 			= enum.auto()	# 'print'
	SCAN 			= enum.auto()	# 'scan'
	WHILE 			= enum.auto()	# 'while'
	# operadores lógicos
	OR 				= enum.auto()	# '||'
	AND 			= enum.auto()	# '&&'
	NOT 			= enum.auto()	# '!'
	EQUAL 			= enum.auto()	# '=='
	DIFF 			= enum.auto()	# '!='
	LT				= enum.auto()	# '<'
	LTEQ 			= enum.auto()	# '<='
	GT 				= enum.auto()	# '>'
	GTEQ 			= enum.auto()	# '>='
	#operadores aritmeticos
	SOMA		 	= enum.auto()	# '+'
	SUBT 			= enum.auto()	# '-'
	MULT 			= enum.auto()	# '*'
	DIV 			= enum.auto()	# '/'
	MODU			= enum.auto()	# '%'
	ATRIB 			= enum.auto()	# '='
	# marcadores
	ABREPAR 		= enum.auto()	# '('
	FEHAPAR 		= enum.auto()	# ')'
	ABRECHAVE 		= enum.auto()	# '{'
	FECHACHAVE 		= enum.auto()	# '}'
	VIRGULA 		= enum.auto()	# ','
	PTOEVIRGULA		= enum.auto()	# ';'

 	IDENT			= enum.auto()	# [a-zA-Z_][a-zA-Z0-9_]*
	STRING 			= enum.auto()	# \"(\\.|[^\\"])*\"
	NUMINT 			= enum.auto()	# [0-9]+
	NUMFLOAT 		= enum.auto()	# [0-9]*'.'[0-9]+



dfa = [[0,] * 256 for i in range(0, 44)]


def set_transition(source, clist, target):

	for c in clist:
		dfa[source][ord(clist)] = target

dfa[1][ord(' ')]  = 1
dfa[1][ord('\n')] = 1
dfa[1][ord('\t')] = 1
dfa[1][ord('b')] = 2
dfa[1][ord('c')] = 3
dfa[1][ord('e')] = 4
dfa[1][ord('f')] = 5
dfa[1][ord('i')] = 6
dfa[1][ord('p')] = 7
dfa[1][ord('s')] = 8
dfa[1][ord('w')] = 9
dfa[2][ord('r')] = 10
dfa[3][ord('o')] = 11
dfa[4][ord('l')] = 12
dfa[5][ord('l')] = 13
dfa[5][ord('o')] = 14
dfa[6][ord('f')] = 15
dfa[6][ord('n')] = 16
dfa[7][ord('r')] = 17
dfa[8][ord('c')] = 18
dfa[9][ord('n')] = 19
dfa[10][ord('e')] = 20
dfa[11][ord('n')] = 21
dfa[12][ord('s')] = 22
dfa[13][ord('o')] = 23
dfa[14][ord('r')] = 24
dfa[16][ord('t')] = 25
dfa[17][ord('i')] = 26
dfa[18][ord('a')] = 27
dfa[19][ord('i')] = 28
dfa[20][ord('a')] = 29
dfa[21][ord('t')] = 30
dfa[22][ord('e')] = 31
dfa[23][ord('a')] = 32
dfa[26][ord('n')] = 33
dfa[27][ord('n')] = 34
dfa[28][ord('l')] = 35
dfa[29][ord('k')] = 36
dfa[30][ord('i')] = 37
dfa[32][ord('t')] = 38
dfa[33][ord('t')] = 39
dfa[35][ord('e')] = 40
dfa[37][ord('n')] = 41
dfa[41][ord('u')] = 42
dfa[42][ord('e')] = 43



# OBSERVAÇÕES:
#	O estado '0' representa um erro
#	Caracteres em loop no estado '1' serão ignorados
class Lexer:

	def __init__(self, filepath, dfa, state_token):

		self.file = open(filepath, 'rb')	# the file to tokenize
		self.lin, self.col = 0, 0			# position in file

	def get_token(self):
		""" return the next token in self.file """

		lexeme = ''
		lookahead = self.file.read(1).decode()
		current_state = 1

		while lookahead != '': # not eof

			if lookahead == '\n':
				self.lin += 1
				self.col = 0
			else:
				self.col += 1

			# block comment
			if lexeme == '/*':
				lexeme = ''
				current_state = 1

				while (lookahead != ''):

					if lookahead == '\n':
						self.lin += 1
						self.col = 0
					else:
						self.col += 1

					lookahead = self.file.read(1).decode()

					if (lookahead == '*') and (self.file.read(1).decode() == '/'):
						lookahead = self.file.read(1).decode()
						break

			# line comment
			if lexeme == '//':
				lexeme = ''
				current_state = 1

				while (lookahead != '') and (lookahead != '\n'):
					lookahead = self.file.read(1).decode()
					self.col += 1

				lookahead = self.file.read(1).decode()


			# walk through the DFA
			next_state = dfa[current_state][lookahead]

			if next_state != 0: # increment the lexeme

				if not (next_state == current_state == 1):

					lexeme += lookahead
					current_state = next_state

				lookahead = self.file.read(1).decode()

			else: # next state is an error

				self.file.seek(-1, 1)
				return state_token[current_state], lexeme, (self.lin, self.col)

		return (TokenTypeEnum.EOF, '', self.lin, self.col)
