from first_follow import first
from lexer import Token, Lexer


class ParseError(Exception):

    def __init__(self, message, line, col):
        super().__init__(message)
        self.line = line
        self.col = col
    
    def __str__(self):

        return f'ERROR: ({self.line}, {self.col}): ' + super().__str__()


class Parser:

    def __init__(self, filepath):
        
        self.lexer = Lexer(filepath)
    
    def consume_token(self, token):

        if self.current_token == token:
            self.current_token = self.lexer.get_token()
        else:
            raise ParseError(f'expected {token}, but got "{self.lexer.lexeme}".', 
                self.lexer.x, self.lexer.y)
    
    @property
    def function(self):
        self.type
        self.consume_token(Token.IDENT)
        self.consume_token(Token.ABREPAR)
        self.arg_list
        self.consume_token(Token.FECHAPAR)
        self.bloco
    
    @property
    def arg_list(self):
        if self.current_token in first['arg']:
            self.arg
            self.resto_arg_list
        else:
            pass
    
    @property
    def arg(self):
        self.type
        self.consume_token(Token.IDENT)
    
    @property
    def resto_arg_list(self):
        if self.current_token == Token.VIRGULA:
            self.consume_token(Token.VIRGULA)
            self.arg_list
        else:
            pass

    @property
    def type(self):
        if self.current_token == Token.INT:
            self.consume_token(Token.INT)
        else:
            self.consume_token(Token.FLOAT)
    
    @property
    def bloco(self):
        self.consume_token(Token.ABRECHAVE)
        self.stmt_list
        self.consume_token(Token.FECHACHAVE)
    
    @property
    def stmt_list(self):
        if self.current_token in first['stmt']:
            self.stmt
            self.stmt_list
        else:
            pass
    
    @property
    def stmt(self):
        if self.current_token in first['for_stmt']:
            self.for_stmt
        elif self.current_token in first['io_stmt']:
            self.io_stmt
        elif self.current_token in first['while_stmt']:
            self.while_stmt
        elif self.current_token in first['expr']:
            self.expr
            self.consume_token(Token.PTOEVIRGULA)
        elif self.current_token in first['if_stmt']:
            self.if_stmt
        elif self.current_token in first['bloco']:
            self.bloco
        elif self.current_token in first['declaration']:
            self.declaration
        elif self.current_token == Token.BREAK:
            self.consume_token(Token.BREAK)
            self.consume_token(Token.PTOEVIRGULA)
        elif self.current_token == Token.CONTINUE:
            self.consume_token(Token.CONTINUE)
            self.consume_token(Token.PTOEVIRGULA)
        elif self.current_token == Token.RETURN:
            self.consume_token(Token.RETURN)
            self.fator
            self.consume_token(Token.PTOEVIRGULA)
        else:
            self.consume_token(Token.PTOEVIRGULA)
    
    @property
    def declaration(self):
        self.type
        self.ident_list
        self.consume_token(Token.PTOEVIRGULA)
    
    @property
    def ident_list(self):
        
        self.consume_token(Token.IDENT)
        self.resto_ident_list
    
    @property
    def resto_ident_list(self):
        if self.current_token == Token.VIRGULA:
            self.consume_token(Token.VIRGULA)
            self.consume_token(Token.IDENT)
            self.resto_ident_list
        else:
            pass
    
    @property
    def for_stmt(self):
        self.consume_token(Token.FOR)
        self.consume_token(Token.ABREPAR)
        self.opt_expr
        self.consume_token(Token.PTOEVIRGULA)
        self.opt_expr
        self.consume_token(Token.PTOEVIRGULA)
        self.opt_expr
        self.consume_token(Token.FECHAPAR)
        self.stmt
    
    @property
    def opt_expr(self):
        if self.current_token in first['expr']:
            self.expr
        else:
            pass
    
    @property
    def io_stmt(self):
        if self.current_token == Token.SCAN:
            self.consume_token(Token.SCAN)
            self.consume_token(Token.ABREPAR)
            self.consume_token(Token.STRING)
            self.consume_token(Token.VIRGULA)
            self.consume_token(Token.IDENT)
            self.consume_token(Token.FECHAPAR)
            self.consume_token(Token.PTOEVIRGULA)
        else:
            self.consume_token(Token.PRINT)
            self.consume_token(Token.ABREPAR)
            self.out_list
            self.consume_token(Token.FECHAPAR)
            self.consume_token(Token.PTOEVIRGULA)
    
    @property
    def out_list(self):
        self.out
        self.resto_out_list
    
    @property
    def out(self):
        if self.current_token == Token.STRING:
            self.consume_token(Token.STRING)
        elif self.current_token == Token.IDENT:
            self.consume_token(Token.IDENT)
        elif self.current_token == Token.NUMINT:
            self.consume_token(Token.NUMINT)
        else:
            self.consume_token(Token.NUMFLOAT)
    
    @property
    def resto_out_list(self):
        
        if self.current_token == Token.VIRGULA:
            self.consume_token(Token.VIRGULA)
            self.out
            self.resto_out_list
        else:
            pass
    
    @property
    def while_stmt(self):
        self.consume_token(Token.WHILE)
        self.consume_token(Token.ABREPAR)
        self.expr
        self.consume_token(Token.FECHAPAR)
        self.stmt
    
    @property
    def if_stmt(self):
        self.consume_token(Token.IF)
        self.consume_token(Token.ABREPAR)
        self.expr
        self.consume_token(Token.FECHAPAR)
        self.stmt
        self.else_part
    
    @property
    def else_part(self):
        if self.current_token == Token.ELSE:
            self.consume_token(Token.ELSE)
            self.stmt
        else:
            pass
    
    @property
    def expr(self):
        self.atrib
    
    @property
    def atrib(self):
        a = self.or_
        b = self.resto_atrib
        if not(a or b):
            raise ParseError(f'missing lvalue!', self.lexer.x, self.lexer.y)
    
    @property
    def resto_atrib(self):
        if self.current_token == Token.ATRIB:
            self.consume_token(Token.ATRIB)
            self.atrib
        else:
            return True
        return False
    
    @property
    def or_(self):
        a = self.and_
        b = self.resto_or
        return a and b

    @property
    def resto_or(self):
        if self.current_token == Token.OR:
            self.consume_token(Token.OR)
            self.and_
            self.resto_or
        else:
            return True
        return False
    
    @property
    def and_(self):
        a = self.not_
        b = self.resto_and
        return a and b
    
    @property
    def resto_and(self):
        if self.current_token == Token.AND:
            self.consume_token(Token.AND)
            self.not_
            self.resto_and
        else:
            return True
        return False
    
    @property
    def not_(self):
        if self.current_token == Token.NOT:
            self.consume_token(Token.NOT)
            self.not_
        else:
            return self.rel
        return False
    
    @property
    def rel(self):
        a = self.add
        b = self.resto_rel
        return a and b
    
    @property
    def resto_rel(self):
        if self.current_token == Token.EQUAL:
            self.consume_token(Token.EQUAL)
            self.add
        elif self.current_token == Token.DIFF:
            self.consume_token(Token.DIFF)
            self.add
        elif self.current_token == Token.GT:
            self.consume_token(Token.GT)
            self.add
        elif self.current_token == Token.GTEQ:
            self.consume_token(Token.GTEQ)
            self.add
        elif self.current_token == Token.LT:
            self.consume_token(Token.GT)
            self.add
        elif self.current_token == Token.LTEQ:
            self.consume_token(Token.GTEQ)
            self.add
        else:
            return True
        return False
    
    @property
    def add(self):
        a = self.mult
        b = self.resto_add
        return a and b
    
    @property
    def resto_add(self):

        if self.current_token == Token.SOMA:
            self.consume_token(Token.SOMA)
            self.mult
            self.resto_add
        elif self.current_token == Token.SUBT:
            self.consume_token(Token.SUBT)
            self.mult
            self.resto_add
        else:
            return True
        return False
    
    @property
    def mult(self):
        a = self.uno
        b = self.resto_mult
        return a and b
    
    @property
    def resto_mult(self):
        if self.current_token == Token.MULT:
            self.consume_token(Token.MULT)
            self.uno
            self.resto_mult
        elif self.current_token == Token.DIV:
            self.consume_token(Token.DIV)
            self.uno
            self.resto_mult
        elif self.current_token == Token.MODU:
            self.consume_token(Token.MODU)
            self.uno
            self.resto_mult
        else:
            return True
        return False
    
    @property
    def uno(self):
        if self.current_token == Token.SOMA:
            self.consume_token(Token.SOMA)
            self.uno
        elif self.current_token == Token.SUBT:
            self.consume_token(Token.SUBT)
            self.uno
        else:
            return self.fator
        return False
    
    @property
    def fator(self):
        if self.current_token == Token.NUMINT:
            self.consume_token(Token.NUMINT)
        elif self.current_token == Token.NUMFLOAT:
            self.consume_token(Token.NUMFLOAT)
        elif self.current_token == Token.IDENT:
            self.consume_token(Token.IDENT)
            return True
        else:
            self.consume_token(Token.ABREPAR)
            self.atrib
            self.consume_token(Token.FECHAPAR)
        return False
        

    def parse(self):
        
        try:
            self.current_token = self.lexer.get_token()
            self.function
            self.consume_token(Token.EOF)
        except ParseError as error:
            print(error)


if __name__ == '__main__':
    parser = Parser('prog-exemplo.miniC')
    parser.parse()