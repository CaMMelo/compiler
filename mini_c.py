from lexer import Lexer, TokenTypeEnum


if __name__ == '__main__':
	lexer = Lexer('input.file')

	token = lexer.get_token()

	while token[0] != TokenTypeEnum.EOF:
		print(token)
		token = lexer.get_token()
	print(token)
