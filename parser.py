import lexer


class Parser:

	def __init__(self, filepath):

		self.lexer = lexer.Lexer(filepath)

	def consume_token(self, token):

		if self.current_token[0] == token:
			self.current_token = self.lexer.get_token()
		else:
			print('ERROR!') # consertar essa mensagem

	def __function(self):
		self.__type()
		self.consume_token(self, lexer.TokenTypeEnum.IDENT)
		self.consume_token(self, lexer.TokenTypeEnum.ABREPAR)
		self.__arglist()
		self.consume_token(self, lexer.TokenTypeEnum.FECHAPAR)
		self.__bloco()

	def __arg_list(self):

		pass

	def __type(self):

		if self.current_token[0] == lexer.TokenTypeEnum.INT:
			self.consume_token(self, lexer.TokenTypeEnum.INT)

		else:
			self.consume_token(self, lexer.TokenTypeEnum.FLOAT)

	def parse(self):
		self.current_token = self.lexer.get_token()
		self.__function()
