import enum
from dfa import next_state, get_action, symbol


class Token(enum.Enum):

    EOF             = enum.auto()
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
    IDENT 			= enum.auto()	# [a-zA-Z][a-zA-Z0-9]*
    STRING 			= enum.auto()	# \"(\\.|[^\\"])*\"
    NUMINT 			= enum.auto()	# [0-9]+
    NUMFLOAT 		= enum.auto()	# [0-9]*'.'[0-9]+

class Lexer:

    def __init__(self, filepath):
        
        self.file = open(filepath, 'rb')
        
        self._x, self._y = 1, 1
        self._oy = 1
        
        self.lexeme = ''
    
    def get_token(self):

        while True:
            
            # setup matching
            self.x, self.y = self._x, self._y
            self.current_state = 0
            self.current_char = self.__next_char
            self.lexeme = ''

            # match
            self.lexeme += self.current_char
            self.current_state = self.__next_state
            self.current_char = self.__next_char

            while(self.__next_state != -1):
                self.lexeme += self.current_char
                self.current_state = self.__next_state
                self.current_char = self.__next_char
            
            if self.current_char != '':

                self._y = self._oy
                if self.current_char == '\n':
                    self._x-=1
                self.file.seek(-1, 1)

            # act

            action = get_action(self.current_state)

            if action == 0: # the default action is to ignore
                continue
            if action == 1:
                return Token.BREAK
            if action == 2:
                return Token.CONTINUE
            if action == 3:
                return Token.ELSE
            if action == 4:
                return Token.FLOAT
            if action == 5:
                return Token.FOR
            if action == 6:
                return Token.IF
            if action == 7:
                return Token.INT
            if action == 8:
                return Token.PRINT
            if action == 9:
                return Token.RETURN
            if action == 10:
                return Token.SCAN
            if action == 11:
                return Token.WHILE
            if action == 12:
                return Token.NOT
            if action == 13:
                return Token.LT
            if action == 14:
                return Token.GT
            if action == 15:
                return Token.LTEQ
            if action == 16:
                return Token.GTEQ
            if action == 17:
                return Token.OR
            if action == 18:
                return Token.AND
            if action == 19:
                return Token.EQUAL
            if action == 20:
                return Token.DIFF
            if action == 21:
                return Token.SOMA
            if action == 22:
                return Token.SUBT
            if action == 23:
                return Token.MULT
            if action == 24:
                return Token.DIV
            if action == 25:
                return Token.MODU
            if action == 26:
                return Token.ATRIB
            if action == 27:
                return Token.ABREPAR
            if action == 28:
                return Token.FECHAPAR
            if action == 29:
                return Token.ABRECHAVE
            if action == 30:
                return Token.FECHACHAVE
            if action == 31:
                return Token.VIRGULA
            if action == 32:
                return Token.PTOEVIRGULA
            if action == 33:
                return Token.IDENT
            if action == 34:
                return Token.STRING
            if action == 35:
                return Token.NUMINT
            if action == 36:
                return Token.NUMFLOAT
            if action == 37:
                return Token.EOF
            if action == 38: # ignore line comment
                self.current_char = self.__next_char
                while self.current_char != '\n':
                    self.current_char = self.__next_char
                    

    @property
    def __next_state(self):
        return next_state(self.current_state, symbol(self.current_char))
    
    @property
    def __next_char(self):
        c = self.file.read(1).decode()
        self._oy = self._y
        self._y += 1
        if c == '\n':
            self._x+=1
            self._y =1
        return c


if __name__ == '__main__':

    lexer = Lexer('prog-exemplo.miniC')
    token = lexer.get_token()
    while token != Token.EOF:
        print(f'{token:20}, "{lexer.lexeme}"')
        token = lexer.get_token()