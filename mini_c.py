from lexer import Lexer


if __name__ == '__main__':
	lexer = Lexer('input.file')
	print(lexer.get_token())
	print(lexer.get_token())
