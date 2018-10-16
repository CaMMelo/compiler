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
	RETURN 			= enum.auto()	# 'return'
	SCAN 			= enum.auto()	# 'scan'
	WHILE 			= enum.auto()	# 'while'
	# operadores lógicos
	NOT 			= enum.auto()	# '!'
	LT				= enum.auto()	# '<'
	GT 				= enum.auto()	# '>'
	LTEQ 			= enum.auto()	# '<='
	GTEQ 			= enum.auto()	# '>='
	OR 				= enum.auto()	# '||'
	AND 			= enum.auto()	# '&&'
	EQUAL 			= enum.auto()	# '=='
	DIFF 			= enum.auto()	# '!='
	#operadores aritmeticos
	SOMA		 	= enum.auto()	# '+'
	SUBT 			= enum.auto()	# '-'
	MULT 			= enum.auto()	# '*'
	DIV 			= enum.auto()	# '/'
	MODU			= enum.auto()	# '%'
	ATRIB 			= enum.auto()	# '='
	# marcadores
	ABREPAR 		= enum.auto()	# '('
	FECHAPAR 		= enum.auto()	# ')'
	ABRECHAVE 		= enum.auto()	# '{'
	FECHACHAVE 		= enum.auto()	# '}'
	VIRGULA 		= enum.auto()	# ','
	PTOEVIRGULA		= enum.auto()	# ';'

	IDENT 			= enum.auto()	# [a-zA-Z_][a-zA-Z0-9_]*
	STRING 			= enum.auto()	# \"(\\.|[^\\"])*\"
	NUMINT 			= enum.auto()	# [0-9]+
	NUMFLOAT 		= enum.auto()	# [0-9]*'.'[0-9]+



dfa = [[0 for k in range(0, 256)] for i in range(0, 200)]
state_token = [TokenTypeEnum.ERROR, ] * 200

state_token[2]  = TokenTypeEnum.IDENT
state_token[3]  = TokenTypeEnum.IDENT
state_token[4]  = TokenTypeEnum.IDENT
state_token[5]  = TokenTypeEnum.IDENT
state_token[6]  = TokenTypeEnum.IDENT
state_token[7]  = TokenTypeEnum.IDENT
state_token[8]  = TokenTypeEnum.IDENT
state_token[9]  = TokenTypeEnum.IDENT
state_token[10] = TokenTypeEnum.IDENT
state_token[11] = TokenTypeEnum.IDENT
state_token[12] = TokenTypeEnum.IDENT
state_token[13] = TokenTypeEnum.IDENT
state_token[14] = TokenTypeEnum.IDENT
state_token[15] = TokenTypeEnum.IF
state_token[16] = TokenTypeEnum.IDENT
state_token[17] = TokenTypeEnum.IDENT
state_token[18] = TokenTypeEnum.IDENT
state_token[19] = TokenTypeEnum.IDENT
state_token[20] = TokenTypeEnum.IDENT
state_token[21] = TokenTypeEnum.IDENT
state_token[22] = TokenTypeEnum.IDENT
state_token[23] = TokenTypeEnum.IDENT
state_token[24] = TokenTypeEnum.FOR
state_token[25] = TokenTypeEnum.INT
state_token[26] = TokenTypeEnum.IDENT
state_token[27] = TokenTypeEnum.IDENT
state_token[28] = TokenTypeEnum.IDENT
state_token[29] = TokenTypeEnum.IDENT
state_token[30] = TokenTypeEnum.IDENT
state_token[31] = TokenTypeEnum.ELSE
state_token[32] = TokenTypeEnum.IDENT
state_token[33] = TokenTypeEnum.IDENT
state_token[34] = TokenTypeEnum.SCAN
state_token[35] = TokenTypeEnum.IDENT
state_token[36] = TokenTypeEnum.BREAK
state_token[37] = TokenTypeEnum.IDENT
state_token[38] = TokenTypeEnum.FLOAT
state_token[39] = TokenTypeEnum.PRINT
state_token[40] = TokenTypeEnum.WHILE
state_token[41] = TokenTypeEnum.IDENT
state_token[42] = TokenTypeEnum.IDENT
state_token[43] = TokenTypeEnum.CONTINUE
state_token[44] = TokenTypeEnum.SOMA
state_token[45] = TokenTypeEnum.SUBT
state_token[46] = TokenTypeEnum.MULT
state_token[47] = TokenTypeEnum.DIV
state_token[48] = TokenTypeEnum.MODU
state_token[49] = TokenTypeEnum.ATRIB
state_token[50] = TokenTypeEnum.ABREPAR
state_token[51] = TokenTypeEnum.FECHAPAR
state_token[52] = TokenTypeEnum.ABRECHAVE
state_token[53] = TokenTypeEnum.FECHACHAVE
state_token[54] = TokenTypeEnum.VIRGULA
state_token[55] = TokenTypeEnum.PTOEVIRGULA
state_token[56] = TokenTypeEnum.NOT
state_token[57] = TokenTypeEnum.LT
state_token[58] = TokenTypeEnum.GT
state_token[61] = TokenTypeEnum.LTEQ
state_token[62] = TokenTypeEnum.GTEQ
state_token[63] = TokenTypeEnum.EQUAL
state_token[64] = TokenTypeEnum.AND
state_token[65] = TokenTypeEnum.OR
state_token[66] = TokenTypeEnum.NUMINT
state_token[67] = TokenTypeEnum.NUMFLOAT
state_token[69] = TokenTypeEnum.IDENT
state_token[73] = TokenTypeEnum.STRING
state_token[74] = TokenTypeEnum.DIFF
state_token[80] = TokenTypeEnum.RETURN

# dfa definition
def set_transition(source, clist, target):
	for c in clist:
		dfa[source][ord(c)] = target

dfa[1][ord(' ')]  = 1
dfa[1][ord('\n')] = 1
dfa[1][ord('\t')] = 1
dfa[1][ord('/')]   = 70
dfa[2][ord('/')]   = 70
dfa[3][ord('/')]   = 70
dfa[4][ord('/')]   = 70
dfa[5][ord('/')]   = 70
dfa[6][ord('/')]   = 70
dfa[7][ord('/')]   = 70
dfa[8][ord('/')]   = 70
dfa[9][ord('/')]   = 70
dfa[10][ord('/')]  = 70
dfa[11][ord('/')]  = 70
dfa[12][ord('/')]  = 70
dfa[13][ord('/')]  = 70
dfa[14][ord('/')]  = 70
dfa[15][ord('/')]  = 70
dfa[16][ord('/')]  = 70
dfa[17][ord('/')]  = 70
dfa[18][ord('/')]  = 70
dfa[19][ord('/')]  = 70
dfa[20][ord('/')]  = 70
dfa[21][ord('/')]  = 70
dfa[22][ord('/')]  = 70
dfa[23][ord('/')]  = 70
dfa[24][ord('/')]  = 70
dfa[25][ord('/')]  = 70
dfa[26][ord('/')]  = 70
dfa[27][ord('/')]  = 70
dfa[28][ord('/')]  = 70
dfa[29][ord('/')]  = 70
dfa[30][ord('/')]  = 70
dfa[31][ord('/')]  = 70
dfa[32][ord('/')]  = 70
dfa[33][ord('/')]  = 70
dfa[34][ord('/')]  = 70
dfa[35][ord('/')]  = 70
dfa[36][ord('/')]  = 70
dfa[37][ord('/')]  = 70
dfa[38][ord('/')]  = 70
dfa[39][ord('/')]  = 70
dfa[40][ord('/')]  = 70
dfa[41][ord('/')]  = 70
dfa[42][ord('/')]  = 70
dfa[43][ord('/')]  = 70
dfa[44][ord('/')]  = 70
dfa[45][ord('/')]  = 70
dfa[46][ord('/')]  = 70
dfa[48][ord('/')]  = 70
dfa[49][ord('/')]  = 70
dfa[50][ord('/')]  = 70
dfa[51][ord('/')]  = 70
dfa[52][ord('/')]  = 70
dfa[53][ord('/')]  = 70
dfa[54][ord('/')]  = 70
dfa[55][ord('/')]  = 70
dfa[56][ord('/')]  = 70
dfa[57][ord('/')]  = 70
dfa[58][ord('/')]  = 70
dfa[59][ord('/')]  = 70
dfa[60][ord('/')]  = 70
dfa[61][ord('/')]  = 70
dfa[62][ord('/')]  = 70
dfa[63][ord('/')]  = 70
dfa[64][ord('/')]  = 70
dfa[65][ord('/')]  = 70
dfa[66][ord('/')]  = 70
dfa[67][ord('/')]  = 70
dfa[68][ord('/')]  = 70
dfa[69][ord('/')]  = 70
dfa[70][ord('/')]  = 70
dfa[70][ord('*')]  = 70
dfa[47][ord('/')]  = 70
dfa[47][ord('*')]  = 70
set_transition(1, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_', 69)
set_transition(69, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(1, '1234567890', 66)
set_transition(66, '1234567890', 66)
dfa[66][ord('.')]  = 67
set_transition(67, '1234567890', 67)
dfa[1][ord('.')]  = 68
set_transition(68, '1234567890', 67)
set_transition(2,  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(3,  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(4,  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(5,  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(6,  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(7,  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(8,  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(9,  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(10, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(11, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(12, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(13, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(14, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(15, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(16, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(17, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(18, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(19, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(20, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(21, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(22, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(23, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(24, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(25, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(26, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(27, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(28, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(29, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(31, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(32, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(33, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(34, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(35, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(36, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(37, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(38, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(39, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(40, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(41, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(42, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(43, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)

set_transition(75, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(76, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(77, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(78, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(79, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)
set_transition(80, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_', 69)

dfa[1][ord('b')]  = 2
dfa[1][ord('c')]  = 3
dfa[1][ord('e')]  = 4
dfa[1][ord('f')]  = 5
dfa[1][ord('i')]  = 6
dfa[1][ord('p')]  = 7
dfa[1][ord('s')]  = 8
dfa[1][ord('w')]  = 9
dfa[1][ord('+')]  = 44
dfa[1][ord('-')]  = 45
dfa[1][ord('*')]  = 46
dfa[1][ord('/')]  = 47
dfa[1][ord('%')]  = 48
dfa[1][ord('=')]  = 49
dfa[1][ord('(')]  = 50
dfa[1][ord(')')]  = 51
dfa[1][ord('{')]  = 52
dfa[1][ord('}')]  = 53
dfa[1][ord(',')]  = 54
dfa[1][ord(';')]  = 55
dfa[1][ord('!')]  = 56
dfa[1][ord('<')]  = 57
dfa[1][ord('>')]  = 58
dfa[1][ord('&')]  = 59
dfa[1][ord('|')]  = 60
dfa[56][ord('!')]  = 74
dfa[57][ord('=')]  = 61
dfa[58][ord('=')]  = 62
dfa[49][ord('=')]  = 63
dfa[59][ord('&')]  = 64
dfa[60][ord('|')]  = 65
dfa[2][ord('r')]  = 10
dfa[3][ord('o')]  = 11
dfa[4][ord('l')]  = 12
dfa[5][ord('l')]  = 13
dfa[5][ord('o')]  = 14
dfa[6][ord('f')]  = 15
dfa[6][ord('n')]  = 16
dfa[7][ord('r')]  = 17
dfa[8][ord('c')]  = 18
dfa[9][ord('h')]  = 19
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
dfa[1][ord('"')] = 71
dfa[71] = [71 for i in range(0, 256)]
dfa[71][ord('"')] = 73
dfa[71][ord('\\')] = 72
dfa[72] = [71 for i in range(0, 256)]

dfa[1][ord('r')] = 75
dfa[75][ord('e')] = 76
dfa[76][ord('t')] = 77
dfa[77][ord('u')] = 78
dfa[78][ord('r')] = 79
dfa[79][ord('n')] = 80


# OBSERVAÇÕES:
#	O estado '0' representa um erro
#	Caracteres em loop no estado '1' serão ignorados
class Lexer:

	def __init__(self, filepath):

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

			# walk through the DFA
			next_state = dfa[current_state][ord(lookahead)]

			if next_state != 0: # increment the lexeme

				if not (next_state == current_state == 1):

					lexeme += lookahead
					current_state = next_state

				lookahead = self.file.read(1).decode()

			else: # next state is an error

				self.file.seek(-1, 1)
				return state_token[current_state], lexeme, (self.lin, self.col)

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

		return (TokenTypeEnum.EOF, '', self.lin, self.col)
