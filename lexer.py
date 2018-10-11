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

 	IDENT			= enum.auto()	#
	STRING 			= enum.auto()	# \"(\\.|[^\\"])*\"
	NUMINT 			= enum.auto()	# [0-9]+
	NUMFLOAT 		= enum.auto()	# [0-9]*'.'[0-9]+


# OBSERVAÇÕES:
#	O estado '0' representa um erro
#	Caracteres em loop no estado '1' serão ignorados
# 	preciso achar um jeito de ignorar os comentários
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

			next_state = dfa[current_state][lookahead]

			if lookahead == '\n':
				self.lin += 1
				self.col = 0

			else:
				self.col += 1

			if next_state != 0: # increment the lexeme

				if not (next_state == current_state == 1):

					lexeme += lookahead
					current_state = next_state

				lookahead = self.file.read(1).decode()

			else: # next state is an error

				self.file.seek(-1, 1)
				return state_token[current_state], lexeme, (self.lin, self.col)

		return (TokenTypeEnum.EOF, '', self.lin, self.col)
