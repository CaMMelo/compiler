import lexer
import sys


class Parser:

	def __init__(self, filepath):

		self.lexer = lexer.Lexer(filepath)

	def consume_token(self, token):

		if self.current_token[0] == token:
			self.current_token = self.lexer.get_token()
		else:
			print('ERROR. expected:', token, ', got:', self.current_token[0], 'in line:', self.current_token[2])
			sys.exit(0)

	def __function(self):
		self.__type()
		self.consume_token( lexer.TokenTypeEnum.IDENT)
		self.consume_token( lexer.TokenTypeEnum.ABREPAR)
		self.__arg_list()
		self.consume_token( lexer.TokenTypeEnum.FECHAPAR)
		self.__bloco()

	def __arg_list(self):
		if self.current_token[0] == lexer.TokenTypeEnum.INT or self.current_token[0] == lexer.TokenTypeEnum.FLOAT:
			self.__arg()
			self.__resto_arg_list()
		else:
			pass

	def __arg(self):
		self.__type()
		self.consume_token( lexer.TokenTypeEnum.IDENT)

	def __resto_arg_list(self):
		if self.current_token[0] == lexer.TokenTypeEnum.VIRGULA:
			self.consume_token( lexer.TokenTypeEnum.VIRGULA)
			self.__arg_list()
		else:
			pass

	def __type(self):
		if self.current_token[0] == lexer.TokenTypeEnum.INT:
			self.consume_token( lexer.TokenTypeEnum.INT)
		else:
			self.consume_token( lexer.TokenTypeEnum.FLOAT)

	def __bloco(self):
		self.consume_token( lexer.TokenTypeEnum.ABRECHAVE)
		self.__stmt_list()
		self.consume_token( lexer.TokenTypeEnum.FECHACHAVE)

	def __stmt_list(self):
		if self.current_token[0] == lexer.TokenTypeEnum.NOT or \
			self.current_token[0] == lexer.TokenTypeEnum.ABREPAR or \
			self.current_token[0] == lexer.TokenTypeEnum.SOMA or \
			self.current_token[0] == lexer.TokenTypeEnum.SUBT or \
			self.current_token[0] == lexer.TokenTypeEnum.PTOEVIRGULA or \
			self.current_token[0] == lexer.TokenTypeEnum.IDENT or \
			self.current_token[0] == lexer.TokenTypeEnum.NUMFLOAT or \
			self.current_token[0] == lexer.TokenTypeEnum.NUMINT or \
			self.current_token[0] == lexer.TokenTypeEnum.BREAK or \
			self.current_token[0] == lexer.TokenTypeEnum.CONTINUE or \
			self.current_token[0] == lexer.TokenTypeEnum.FLOAT or \
			self.current_token[0] == lexer.TokenTypeEnum.FOR or \
			self.current_token[0] == lexer.TokenTypeEnum.IF or \
			self.current_token[0] == lexer.TokenTypeEnum.INT or \
			self.current_token[0] == lexer.TokenTypeEnum.PRINT or \
			self.current_token[0] == lexer.TokenTypeEnum.SCAN or \
			self.current_token[0] == lexer.TokenTypeEnum.WHILE or \
			self.current_token[0] == lexer.TokenTypeEnum.ABRECHAVE or \
			self.current_token[0] == lexer.TokenTypeEnum.RETURN:
				self.__stmt()
				self.__stmt_list()
		else:
			pass

	def __stmt(self):
		if self.current_token[0] == lexer.TokenTypeEnum.FOR:
			self.__for_stmt()
		elif self.current_token[0] == lexer.TokenTypeEnum.PRINT or \
			self.current_token[0] == lexer.TokenTypeEnum.SCAN:
			self.__io_stmt()
		elif self.current_token[0] == lexer.TokenTypeEnum.WHILE:
			self.__while_stmt()
		elif self.current_token[0] == lexer.TokenTypeEnum.NOT or \
			self.current_token[0] == lexer.TokenTypeEnum.ABREPAR or \
			self.current_token[0] == lexer.TokenTypeEnum.SOMA or \
			self.current_token[0] == lexer.TokenTypeEnum.SUBT or \
			self.current_token[0] == lexer.TokenTypeEnum.IDENT or \
			self.current_token[0] == lexer.TokenTypeEnum.NUMFLOAT or \
			self.current_token[0] == lexer.TokenTypeEnum.NUMINT:
				self.__expr()
				self.consume_token( lexer.TokenTypeEnum.PTOEVIRGULA)
		elif self.current_token[0] == lexer.TokenTypeEnum.IF:
			self.__if_stmt()
		elif self.current_token[0] == lexer.TokenTypeEnum.ABRECHAVE:
			self.__bloco()
		elif self.current_token[0] == lexer.TokenTypeEnum.BREAK:
			self.consume_token( lexer.TokenTypeEnum.BREAK)
			self.consume_token( lexer.TokenTypeEnum.PTOEVIRGULA)
		elif self.current_token[0] == lexer.TokenTypeEnum.CONTINUE:
			self.consume_token( lexer.TokenTypeEnum.CONTINUE)
			self.consume_token( lexer.TokenTypeEnum.PTOEVIRGULA)
		elif self.current_token[0] == lexer.TokenTypeEnum.FLOAT or \
			self.current_token[0] == lexer.TokenTypeEnum.INT:
			self.__declaration()
		elif self.current_token[0] == lexer.TokenTypeEnum.PTOEVIRGULA:
			self.consume_token( lexer.TokenTypeEnum.PTOEVIRGULA)
		else:
			self.consume_token(lexer.TokenTypeEnum.RETURN)
			self.__fator()
			self.consume_token(lexer.TokenTypeEnum.PTOEVIRGULA)

	# ---- Declaracoes
	def __declaration(self):
		self.__type()
		self.__ident_list()
		self.consume_token( lexer.TokenTypeEnum.PTOEVIRGULA)

	def __ident_list(self):
		self.consume_token( lexer.TokenTypeEnum.IDENT)
		self.__resto_ident_list()

	def __resto_ident_list(self):
		if self.current_token[0] == lexer.TokenTypeEnum.VIRGULA:
			self.consume_token( lexer.TokenTypeEnum.VIRGULA)
			self.consume_token( lexer.TokenTypeEnum.IDENT)
			self.__resto_ident_list()
		else:
			pass

	# ---- For
	def __for_stmt(self):
		self.consume_token( lexer.TokenTypeEnum.FOR)
		self.consume_token( lexer.TokenTypeEnum.ABREPAR)
		self.__opt_expr()
		self.consume_token( lexer.TokenTypeEnum.PTOEVIRGULA)
		self.__opt_expr()
		self.consume_token( lexer.TokenTypeEnum.PTOEVIRGULA)
		self.__opt_expr()
		self.consume_token( lexer.TokenTypeEnum.FECHAPAR)
		self.__stmt()

	def __opt_expr(self):
		if self.current_token[0] == lexer.TokenTypeEnum.NOT or \
			self.current_token[0] == lexer.TokenTypeEnum.ABREPAR or \
			self.current_token[0] == lexer.TokenTypeEnum.SOMA or \
			self.current_token[0] == lexer.TokenTypeEnum.SUBT or \
			self.current_token[0] == lexer.TokenTypeEnum.IDENT or \
			self.current_token[0] == lexer.TokenTypeEnum.NUMFLOAT or \
			self.current_token[0] == lexer.TokenTypeEnum.NUMINT:
				self.__expr()
		else:
			pass

	# ---- io
	def __io_stmt(self):
		if self.current_token[0] == lexer.TokenTypeEnum.SCAN:
			self.consume_token( lexer.TokenTypeEnum.SCAN)
			self.consume_token( lexer.TokenTypeEnum.ABREPAR)
			self.consume_token( lexer.TokenTypeEnum.STRING)
			self.consume_token( lexer.TokenTypeEnum.VIRGULA)
			self.consume_token( lexer.TokenTypeEnum.IDENT)
			self.consume_token( lexer.TokenTypeEnum.FECHAPAR)
			self.consume_token( lexer.TokenTypeEnum.PTOEVIRGULA)
		else:
			self.consume_token( lexer.TokenTypeEnum.PRINT)
			self.consume_token( lexer.TokenTypeEnum.ABREPAR)
			self.__out_list()
			self.consume_token( lexer.TokenTypeEnum.FECHAPAR)
			self.consume_token( lexer.TokenTypeEnum.PTOEVIRGULA)

	def __out_list(self):
		self.__out()
		self.__resto_out_list()

	def __out(self):
		if self.current_token[0] == lexer.TokenTypeEnum.STRING:
			self.consume_token( lexer.TokenTypeEnum.STRING)
		elif self.current_token[0] == lexer.TokenTypeEnum.IDENT:
			self.consume_token( lexer.TokenTypeEnum.IDENT)
		elif self.current_token[0] == lexer.TokenTypeEnum.NUMINT:
			self.consume_token( lexer.TokenTypeEnum.NUMINT)
		else:
			self.consume_token( lexer.TokenTypeEnum.NUMFLOAT)

	def __resto_out_list(self):
		if self.current_token[0] == lexer.TokenTypeEnum.VIRGULA:
			self.consume_token( lexer.TokenTypeEnum.VIRGULA)
			self.__out()
			self.__resto_out_list()
		else:
			pass

	# ---- while
	def __while_stmt(self):
		self.consume_token( lexer.TokenTypeEnum.WHILE)
		self.consume_token( lexer.TokenTypeEnum.ABREPAR)
		self.__expr()
		self.consume_token( lexer.TokenTypeEnum.FECHAPAR)
		self.__stmt()

	# ---- if
	def __if_stmt(self):
		self.consume_token( lexer.TokenTypeEnum.IF)
		self.consume_token( lexer.TokenTypeEnum.ABREPAR)
		self.__expr()
		self.consume_token( lexer.TokenTypeEnum.FECHAPAR)
		self.__stmt()
		self.__else_part()

	def __else_part(self):
		if self.current_token[0] == lexer.TokenTypeEnum.ELSE:
			self.consume_token( lexer.TokenTypeEnum.ELSE)
			self.__stmt()
		else:
			pass

	# ---- expressoes
	def __expr(self):
		self.__atrib()

	def __atrib(self):
		self.__or()
		self.__resto_atrib()

	def __resto_atrib(self):
		if self.current_token[0] == lexer.TokenTypeEnum.ATRIB:
			self.consume_token( lexer.TokenTypeEnum.ATRIB)
			self.__atrib()
		else:
			pass

	def __or(self):
		self.__and()
		self.__resto_or()

	def __resto_or(self):
		if self.current_token[0] == lexer.TokenTypeEnum.OR:
			self.consume_token( lexer.TokenTypeEnum.OR)
			self.__and()
			self.__resto_or()
		else:
			pass

	def __and(self):
		self.__not()
		self.__resto_and()

	def __resto_and(self):
		if self.current_token[0] == lexer.TokenTypeEnum.AND:
			self.consume_token( lexer.TokenTypeEnum.AND)
			self.__not()
			self.__resto_and()
		else:
			pass

	def __not(self):
		if self.current_token[0] == lexer.TokenTypeEnum.NOT:
			self.consume_token( lexer.TokenTypeEnum.NOT)
			self.__not()
		else:
			self.__rel()

	def __rel(self):
		self.__add()
		self.__resto_rel()

	def __resto_rel(self):
		if self.current_token[0] == lexer.TokenTypeEnum.EQUAL:
			self.consume_token( lexer.TokenTypeEnum.EQUAL)
			self.__add()
		elif self.current_token[0] == lexer.TokenTypeEnum.DIFF:
			self.consume_token( lexer.TokenTypeEnum.DIFF)
			self.__add()
		elif self.current_token[0] == lexer.TokenTypeEnum.GT:
			self.consume_token( lexer.TokenTypeEnum.GT)
			self.__add()
		elif self.current_token[0] == lexer.TokenTypeEnum.GTEQ:
			self.consume_token( lexer.TokenTypeEnum.GTEQ)
			self.__add()
		elif self.current_token[0] == lexer.TokenTypeEnum.LT:
			self.consume_token( lexer.TokenTypeEnum.LT)
			self.__add()
		elif self.current_token[0] == lexer.TokenTypeEnum.LTEQ:
			self.consume_token( lexer.TokenTypeEnum.LTEQ)
			self.__add()
		else:
			pass

	def __add(self):
		self.__mult()
		self.__resto_add()

	def __resto_add(self):
		if self.current_token[0] == lexer.TokenTypeEnum.SOMA:
			self.consume_token( lexer.TokenTypeEnum.SOMA)
			self.__mult()
			self.__resto_add()
		elif self.current_token[0] == lexer.TokenTypeEnum.SUBT:
			self.consume_token( lexer.TokenTypeEnum.SUBT)
			self.__mult()
			self.__resto_add()
		else:
			pass

	def __mult(self):
		self.__uno()
		self.__resto_mult()

	def __resto_mult(self):
		if self.current_token[0] == lexer.TokenTypeEnum.MULT:
			self.consume_token( lexer.TokenTypeEnum.MULT)
			self.__uno()
			self.__resto_mult()
		elif self.current_token[0] == lexer.TokenTypeEnum.DIV:
			self.consume_token( lexer.TokenTypeEnum.DIV)
			self.__uno()
			self.__resto_mult()
		elif self.current_token[0] == lexer.TokenTypeEnum.MODU:
			self.consume_token( lexer.TokenTypeEnum.MODU)
			self.__uno()
			self.__resto_mult()
		else:
			pass

	def __uno(self):
		if self.current_token[0] == lexer.TokenTypeEnum.SOMA:
			self.consume_token( lexer.TokenTypeEnum.SOMA)
			self.__uno()
		elif self.current_token[0] == lexer.TokenTypeEnum.SUBT:
			self.consume_token( lexer.TokenTypeEnum.SUBT)
			self.__uno()
		else:
			self.__fator()

	def __fator(self):
		if self.current_token[0] == lexer.TokenTypeEnum.NUMINT:
			self.consume_token( lexer.TokenTypeEnum.NUMINT)
		elif self.current_token[0] == lexer.TokenTypeEnum.NUMFLOAT:
			self.consume_token( lexer.TokenTypeEnum.NUMFLOAT)
		elif self.current_token[0] == lexer.TokenTypeEnum.IDENT:
			self.consume_token( lexer.TokenTypeEnum.IDENT)
		else:
			self.consume_token( lexer.TokenTypeEnum.ABREPAR)
			self.__atrib()
			self.consume_token( lexer.TokenTypeEnum.FECHAPAR)

	def parse(self):
		self.current_token = self.lexer.get_token()
		self.__function()
