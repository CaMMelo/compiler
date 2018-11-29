from first_follow import first
from lexer import Token, Lexer


class ParseError(Exception):

    def __init__(self, message, line, col):
        super().__init__(message)
        self.line = line
        self.col = col
    
    def __str__(self):
        return f'ERROR: ({self.line}, {self.col}): ' + super().__str__()

def temp_generator():
    i = 0
    while True:
        name = 'temp' + str(i)
        i += 1
        yield name

def label_generator():
    i = 0
    while True:
        label = 'label' + str(i)
        i += 1
        yield label

class Parser:

    def __init__(self, filepath):
        
        a = temp_generator()
        b = label_generator()
        self.lexer = Lexer(filepath)
        self.symbol_table = {}
        self.next_temp = lambda : next(a)
        self.next_label = lambda : next(b)
    
    def consume_token(self, token):

        if self.current_token == token:
            self.current_token = self.lexer.get_token()
        else:
            raise ParseError(f'expected \'{token.value}\' but got \'{self.lexer.lexeme}\'.', 
                self.lexer.x, self.lexer.y)
    
    def function(self):
        self.type()
        self.consume_token(Token.IDENT)
        self.consume_token(Token.ABREPAR)
        self.arg_list()
        self.consume_token(Token.FECHAPAR)
        self.bloco()
    
    def arg_list(self):
        if self.current_token in first['arg']:
            self.arg()
            self.resto_arg_list()
        else:
            pass
    
    def arg(self):
        self.type()
        self.consume_token(Token.IDENT)
    
    def resto_arg_list(self):
        if self.current_token == Token.VIRGULA:
            self.consume_token(Token.VIRGULA)
            self.arg_list()
        else:
            pass

    def type(self):
        if self.current_token == Token.INT:
            self.consume_token(Token.INT)
            return 'int'
        else:
            self.consume_token(Token.FLOAT)
            return 'float'
    
    def bloco(self):
        self.consume_token(Token.ABRECHAVE)
        self.stmt_list()
        self.consume_token(Token.FECHACHAVE)
    
    def stmt_list(self):
        if self.current_token in first['stmt']:
            self.stmt()
            self.stmt_list()
        else:
            pass
    
    def stmt(self):
        if self.current_token in first['for_stmt']:
            self.for_stmt()
        elif self.current_token in first['io_stmt']:
            self.io_stmt()
        elif self.current_token in first['while_stmt']:
            self.while_stmt()
        elif self.current_token in first['expr']:
            self.expr()
            self.consume_token(Token.PTOEVIRGULA)
        elif self.current_token in first['if_stmt']:
            self.if_stmt()
        elif self.current_token in first['bloco']:
            self.bloco()
        elif self.current_token in first['declaration']:
            self.declaration()
        elif self.current_token == Token.BREAK:
            self.consume_token(Token.BREAK)
            self.consume_token(Token.PTOEVIRGULA)
        elif self.current_token == Token.CONTINUE:
            self.consume_token(Token.CONTINUE)
            self.consume_token(Token.PTOEVIRGULA)
        elif self.current_token == Token.RETURN:
            self.consume_token(Token.RETURN)
            self.fator()
            self.consume_token(Token.PTOEVIRGULA)
        else:
            self.consume_token(Token.PTOEVIRGULA)
    
    def declaration(self):
        tipo = self.type()
        vars = self.ident_list()
        self.consume_token(Token.PTOEVIRGULA)

        comandos = []

        for v in vars:
            if v not in self.symbol_table:
                self.symbol_table[v] = tipo
                comandos.append(('=', v, 0, None))
            else:
                raise ParseError(f'redefinition of symbol \'{v}\'', self.lexer.x, self.lexer.y)
        
        return comandos
    
    def ident_list(self):

        var = self.lexer.lexeme
        self.consume_token(Token.IDENT)
        vars = self.resto_ident_list()
        vars.append(var)
        return vars
    
    def resto_ident_list(self):
        vars = []
        if self.current_token == Token.VIRGULA:
            self.consume_token(Token.VIRGULA)
            var = self.lexer.lexeme
            self.consume_token(Token.IDENT)
            vars = self.resto_ident_list()
        else:
            return vars
        
        vars.append(var)
        return vars
    
    def for_stmt(self):
        self.consume_token(Token.FOR)
        self.consume_token(Token.ABREPAR)
        self.opt_expr()
        self.consume_token(Token.PTOEVIRGULA)
        self.opt_expr()
        self.consume_token(Token.PTOEVIRGULA)
        self.opt_expr()
        self.consume_token(Token.FECHAPAR)
        self.stmt()
    
    def opt_expr(self):
        if self.current_token in first['expr']:
            self.expr()
        else:
            pass
    
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
            self.out_list()
            self.consume_token(Token.FECHAPAR)
            self.consume_token(Token.PTOEVIRGULA)
    
    def out_list(self):
        self.out()
        self.resto_out_list()
    
    def out(self):
        if self.current_token == Token.STRING:
            self.consume_token(Token.STRING)
        elif self.current_token == Token.IDENT:
            self.consume_token(Token.IDENT)
        elif self.current_token == Token.NUMINT:
            self.consume_token(Token.NUMINT)
        else:
            self.consume_token(Token.NUMFLOAT)
    
    def resto_out_list(self):
        
        if self.current_token == Token.VIRGULA:
            self.consume_token(Token.VIRGULA)
            self.out()
            self.resto_out_list()
        else:
            pass
    
    def while_stmt(self):
        self.consume_token(Token.WHILE)
        self.consume_token(Token.ABREPAR)
        self.expr()
        self.consume_token(Token.FECHAPAR)
        self.stmt()
    
    def if_stmt(self):
        self.consume_token(Token.IF)
        self.consume_token(Token.ABREPAR)
        self.expr()
        self.consume_token(Token.FECHAPAR)
        self.stmt()
        self.else_part()
    
    def else_part(self):
        if self.current_token == Token.ELSE:
            self.consume_token(Token.ELSE)
            self.stmt()
        else:
            pass
    
    def expr(self):
        return self.atrib()
    
    def atrib(self):
        is_llo, codo, tempo = self.or_()
        is_llr, codr, _ =  = self.resto_atrib(tempo)
        
        if not(is_llo or is_llr):
            raise ParseError(f'missing lvalue.', self.lexer.x, self.lexer.y)
        
        return codo + codr

    
    def resto_atrib(self, valor):
        temp = self.next_temp()
        if self.current_token == Token.ATRIB:
            self.consume_token(Token.ATRIB)
            _, cod, _ = self.atrib()
        else:
            return (True, [], temp)
        comando = ('=', temp, valor, None)
        return (False, cod.append(comando), temp)
    
    def or_(self):
        is_lla, coda, tempa = self.and_()
        is_llr, codr, tempr =  = self.resto_or(tempa)
        return (is_lla and is_llr, coda + codr, tempr)

    def resto_or(self, valor):
        temp = self.next_temp()
        if self.current_token == Token.OR:
            self.consume_token(Token.OR)
            _, coda, tempa = self.and_()
            _, codr, _ = self.resto_or()
        else:
            return (True, [], temp)
        comando = ('or', temp, valor, tempa)
        coda.append(comando)
        return (False, coda + codr, temp)
    
    def and_(self):
        is_lln, codn, tempn = self.not_()
        is_llr, codr, tempr = self.resto_and(tempn)
        return (is_lln and is_llr, codn + codr, tempr)
    
    def resto_and(self, valor):
        temp = self.next_temp()
        if self.current_token == Token.AND:
            self.consume_token(Token.AND)
            _, codn, tempn = self.not_()
            _, codr, _ = self.resto_and(valor)
        else:
            return (True, [], temp)
        comando = ('and', temp, valor, tempn)
        codn.append(comando)
        return (False, codn + codr, temp)
    
    def not_(self):
        temp = self.next_temp()
        if self.current_token == Token.NOT:
            self.consume_token(Token.NOT)
            is_left_value, cod, tempn = self.not_()
        else:
            return self.rel()
        comando = ('!', temp, tempn, None)
        return (False, cod.append(comando), temp)
    
    def rel(self):
        is_lla, coda, tempa = self.add()
        is_llr, codr, tempr = self.resto_rel(tempa)
        return (is_lla and is_llr, coda + codr, tempr)
    
    def resto_rel(self, valor):
        temp = self.next_temp()

        if self.current_token == Token.EQUAL:
            op = '=='
            self.consume_token(Token.EQUAL)
            _, cod, tempa = self.add()
        elif self.current_token == Token.DIFF:
            op = '!='
            self.consume_token(Token.DIFF)
            _, cod, tempa = self.add()
        elif self.current_token == Token.GT:
            op = '>'
            self.consume_token(Token.GT)
            _, cod, tempa = self.add()
        elif self.current_token == Token.GTEQ:
            op = '>='
            self.consume_token(Token.GTEQ)
            _, cod, tempa = self.add()
        elif self.current_token == Token.LT:
            op = '<'
            self.consume_token(Token.GT)
            _, cod, tempa = self.add()
        elif self.current_token == Token.LTEQ:
            op = '<='
            self.consume_token(Token.GTEQ)
            _, cod, tempa = self.add()
        else:
            return (True, [], temp)
        
        comando = (op, temp, valor, tempa)
        return (False, cod.append(comando), temp)
    
    def add(self):
        is_llm, codm, tempm = self.mult()
        is_llr, codr, tempr = self.resto_add(tempm)
        
        return (is_llm and is_llr, codm + codr, tempr)
    
    def resto_add(self, valor):
        temp = self.next_temp()

        if self.current_token == Token.SOMA:
            op = '+'
            self.consume_token(Token.SOMA)
            _, codu, tempu = self.mult()
            _, codr, _ = self.resto_add(valor)
        elif self.current_token == Token.SUBT:
            op = '-'
            self.consume_token(Token.SUBT)
            _, codu, tempu = self.mult()
            _, codr, _ = self.resto_add(valor)
        else:
            return (True, [], temp)
        
        comando = (op, temp, valor, tempu)
        codu.append(comando)
        return (False, codu + codr, temp)
    
    def mult(self):
        is_lvu, codu, tempu = self.uno()
        is_lvr, codr, tempr = self.resto_mult(tempu)

        return (is_lvu and is_lvr, codu + codr, tempr)
    
    def resto_mult(self, valor):
        temp = self.next_temp()

        if self.current_token == Token.MULT:
            op = '*'
            self.consume_token(Token.MULT)
            _, codu, tempu = self.uno()
            _, codr, _ = self.resto_mult(valor)
        elif self.current_token == Token.DIV:
            op = '/'
            self.consume_token(Token.DIV)
            _, codu, tempu = self.uno()
            _, codr, _ = self.resto_mult(valor)
        elif self.current_token == Token.MODU:
            op = '%'
            self.consume_token(Token.MODU)
            _, codu, tempu = self.uno()
            _, codr, _ = self.resto_mult(valor)
        else:
            return (True, [], valor)
        
        comando = (op, temp, valor, tempu)
        codu.append(comando)
        return (False, codu + codr, temp)
    
    def uno(self):
        temp = self.next_temp()

        if self.current_token == Token.SOMA:
            op = '+'
            self.consume_token(Token.SOMA)
            is_left_value, cod, ident = self.uno()
        elif self.current_token == Token.SUBT:
            op = '-'
            self.consume_token(Token.SUBT)
            is_left_value, cod, ident = self.uno()
        else:
            return self.fator()
        
        cod.append((op, temp, ident, 0))
        return (False, cod, temp)
    
    def fator(self):
        is_left_value = False
        temp = self.next_temp()
        ident = self.lexer.lexeme
        
        if self.current_token == Token.NUMINT:
            self.consume_token(Token.NUMINT)
        elif self.current_token == Token.NUMFLOAT:
            self.consume_token(Token.NUMFLOAT)
        elif self.current_token == Token.IDENT:
            self.consume_token(Token.IDENT)
            if ident not in self.symbol_table:
                raise ParseError(f'symbol \'{ident}\' was not defined.', self.lexer.x, self.lexer.y)

            is_left_value = True
        else:
            self.consume_token(Token.ABREPAR)
            self.atrib()
            self.consume_token(Token.FECHAPAR)
        
        return (is_left_value, [('=', temp, ident, None), ], temp)
        
    def parse(self):
        try:
            self.current_token = self.lexer.get_token()
            self.function()
            self.consume_token(Token.EOF)
        except ParseError as error:
            print(error)
            self.symbol_table = {}
