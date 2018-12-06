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
        self.nivel = 0
    
    def consume_token(self, token):
        if self.current_token == token:
            self.current_token = self.lexer.get_token()
        else:
            raise ParseError(f'expected \'{token.value}\' but got \'{self.lexer.lexeme}\'.', 
                self.lexer.x, self.lexer.y)

    def busca_var(self, name):
        atual = self.nivel
        var = '_' + str(atual) + name

        while atual > 0:
            if var not in self.symbol_table:
                atual -= 1
                var = '_' + str(atual) + name
            else:
                return var

        raise ParseError(f'symbol \'{var}\' was not defined.', self.lexer.x, self.lexer.y)

    
    def function(self, inicio, fim):
        self.type()
        self.consume_token(Token.IDENT)
        self.consume_token(Token.ABREPAR)
        args = self.arg_list()
        self.consume_token(Token.FECHAPAR)
        cod = self.bloco(inicio, fim)

        return args + cod
    
    def arg_list(self):
        if self.current_token in first['arg']:
            a = self.arg()
            b = self.resto_arg_list()
            return a + b
        else:
            return []
    
    def arg(self):
        tipo = self.type()
        var = self.lexer.lexeme
        self.consume_token(Token.IDENT)

        if var not in self.symbol_table:
            self.symbol_table[var] = tipo
        else:
            raise ParseError(f'redefinition of symbol \'{v}\'', self.lexer.x, self.lexer.y)

        return [('=', var, tipo(0), None),]

    
    def resto_arg_list(self):
        if self.current_token == Token.VIRGULA:
            self.consume_token(Token.VIRGULA)
            return self.arg_list()
        else:
            return []

    def type(self):
        if self.current_token == Token.INT:
            self.consume_token(Token.INT)
            return int
        else:
            self.consume_token(Token.FLOAT)
            return float
    
    def bloco(self, inicio, fim):
        self.nivel += 1
        self.consume_token(Token.ABRECHAVE)
        cod = self.stmt_list(inicio, fim)
        self.consume_token(Token.FECHACHAVE)
        self.nivel -= 1
        return cod
    
    def stmt_list(self, inicio, fim):
        if self.current_token in first['stmt']:
            a = self.stmt(inicio, fim)
            b = self.stmt_list(inicio, fim)
            return a + b
        elif self.current_token in first['declaration']:
            a = self.declaration()
            b = self.stmt_list(inicio, fim)
            return a + b
        else:
            return []
    
    def stmt(self, inicio, fim):
        if self.current_token in first['for_stmt']:
            return self.for_stmt()
        elif self.current_token in first['io_stmt']:
            return self.io_stmt()
        elif self.current_token in first['while_stmt']:
            return self.while_stmt()
        elif self.current_token in first['expr']:
            cod, _ = self.expr()
            self.consume_token(Token.PTOEVIRGULA)
            return cod
        elif self.current_token in first['if_stmt']:
            return self.if_stmt(inicio, fim)
        elif self.current_token in first['bloco']:
            return self.bloco(inicio, fim)
        elif self.current_token == Token.BREAK:
            self.consume_token(Token.BREAK)
            self.consume_token(Token.PTOEVIRGULA)
            return [('jump', fim, None, None),]
        elif self.current_token == Token.CONTINUE:
            self.consume_token(Token.CONTINUE)
            self.consume_token(Token.PTOEVIRGULA)
            return [('jump', inicio, None, None),]
        elif self.current_token == Token.RETURN:
            self.consume_token(Token.RETURN)
            _, cod, res = self.fator()
            self.consume_token(Token.PTOEVIRGULA)
            return []
        else:
            self.consume_token(Token.PTOEVIRGULA)
            return []
    
    def declaration(self):
        tipo = self.type()
        vars = self.ident_list()
        self.consume_token(Token.PTOEVIRGULA)

        comandos = []

        for v in vars:
            if v not in self.symbol_table:
                v = '_' + str(self.nivel) + v
                self.symbol_table[v] = tipo
                comandos.append(('=', v, tipo(0), None))
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
        inicio = self.next_label()
        fim = self.next_label()
        code = []

        self.consume_token(Token.FOR)
        self.consume_token(Token.ABREPAR)
        expr_init, _ = self.opt_expr()
        self.consume_token(Token.PTOEVIRGULA)
        expr_cond, res_cond = self.opt_expr()
        self.consume_token(Token.PTOEVIRGULA)
        expr_inc, _ = self.opt_expr()
        self.consume_token(Token.FECHAPAR)
        bloco = self.stmt(inicio, fim)


        code += expr_init
        code.append(('label', inicio, None, None))
        code += expr_cond
        code.append(('if', res_cond, None, fim))
        code += bloco
        code += expr_inc
        code.append(('jump', inicio, None, None))
        code.append(('label', fim, None, None))

        return code
        
    
    def opt_expr(self):
        if self.current_token in first['expr']:
            return self.expr()
        else:
            return [], None
    
    def io_stmt(self):
        if self.current_token == Token.SCAN:
            self.consume_token(Token.SCAN)
            self.consume_token(Token.ABREPAR)
            string = self.lexer.lexeme
            self.consume_token(Token.STRING)
            self.consume_token(Token.VIRGULA)
            ident = self.lexer.lexeme
            self.consume_token(Token.IDENT)
            self.consume_token(Token.FECHAPAR)
            self.consume_token(Token.PTOEVIRGULA)

            ident = self.busca_var(ident)

            code = [
                ('call', 'print', string, None),
                ('call', 'scan', ident, None)
            ]

            return code

        else:
            self.consume_token(Token.PRINT)
            self.consume_token(Token.ABREPAR)
            cod = self.out_list()
            self.consume_token(Token.FECHAPAR)
            self.consume_token(Token.PTOEVIRGULA)

            return cod
    
    def out_list(self):
        cod = self.out()
        codr = self.resto_out_list()

        return cod + codr
    
    def out(self):
        ident = self.lexer.lexeme
        if self.current_token == Token.STRING:
            self.consume_token(Token.STRING)
        elif self.current_token == Token.IDENT:
            ident = self.busca_var(ident)
            self.consume_token(Token.IDENT)
        elif self.current_token == Token.NUMINT:
            self.consume_token(Token.NUMINT)
        else:
            self.consume_token(Token.NUMFLOAT)

        return [('call', 'print', ident, None), ]
    
    def resto_out_list(self):
        
        if self.current_token == Token.VIRGULA:
            self.consume_token(Token.VIRGULA)
            cod = self.out()
            codr = self.resto_out_list()
            return cod + codr
        else:
            return []
    
    def while_stmt(self):
        inicio = self.next_label()
        fim = self.next_label()
        code = []

        self.consume_token(Token.WHILE)
        self.consume_token(Token.ABREPAR)
        expr, res = self.expr()
        self.consume_token(Token.FECHAPAR)
        bloco = self.stmt(inicio, fim)

        code.append(('label', inicio, None, None))
        code = code + expr
        code.append( ('if', res, None, fim) )
        code = code + bloco
        code.append( ('jump', inicio, None, None) )
        code.append( ('label', fim, None, None) )

        return code
    
    def if_stmt(self, inicio, fim):
        true = self.next_label()
        false = self.next_label()
        code = []

        self.consume_token(Token.IF)
        self.consume_token(Token.ABREPAR)
        expr, res = self.expr()
        self.consume_token(Token.FECHAPAR)
        bloco_true = self.stmt(inicio, fim)
        bloco_false = self.else_part(inicio, fim)

        code = code + expr
        code.append(('if', res, None, false))
        code = code + bloco_true
        code.append(('jump', true, None, None))
        code.append(('label', false, None, None))
        code = code + bloco_false
        code.append(('label', true, None, None))

        return code
    
    def else_part(self, inicio, fim):
        if self.current_token == Token.ELSE:
            self.consume_token(Token.ELSE)
            return self.stmt(inicio, fim)
        else:
            return []
    
    def expr(self):
        return self.atrib()
    
    def atrib(self):
        is_llo, codo, tempo = self.or_()
        is_llr, codr, tempr = self.resto_atrib(tempo)
        
        if not(is_llo or is_llr):
            raise ParseError(f'missing lvalue.', self.lexer.x, self.lexer.y)
        
        return codo + codr, tempr

    def resto_atrib(self, valor):
        if self.current_token == Token.ATRIB:
            self.consume_token(Token.ATRIB)
            cod, res = self.atrib()
        else:
            return (True, [], valor)

        cod.append(('=', valor, res, None))
        return (False, cod, res)
    
    def or_(self):
        is_lla, coda, tempa = self.and_()
        is_llr, codr, tempr = self.resto_or(tempa)

        return (is_lla and is_llr, coda + codr, tempr)

    def resto_or(self, valor):
        temp = self.next_temp()
        if self.current_token == Token.OR:
            self.consume_token(Token.OR)
            _, coda, tempa = self.and_()
            _, codr, _ = self.resto_or(valor)
        else:
            return (True, [], valor)
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
            return (True, [], valor)
        comando = ('and', temp, valor, tempn)
        codn.append(comando)
        return (False, codn + codr, temp)
    
    def not_(self):
        temp = self.next_temp()
        if self.current_token == Token.NOT:
            self.consume_token(Token.NOT)
            is_left_value, cod, tempn = self.not_()
        else:
            res = self.rel()
            return res
        cod.append(('not', temp, tempn, None))
        return (False, cod, temp)
    
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
            self.consume_token(Token.LT)
            _, cod, tempa = self.add()
        elif self.current_token == Token.LTEQ:
            op = '<='
            self.consume_token(Token.LTEQ)
            _, cod, tempa = self.add()
        else:
            return True, [], valor
        
        cod.append((op, temp, valor, tempa))
        return (False, cod, temp)
    
    def add(self):
        is_llm, codm, tempm = self.mult()
        is_llr, codr, tempr = self.resto_add(tempm)
        
        return (is_llm and is_llr, codm + codr, tempr)
    
    def resto_add(self, valor):
        temp = self.next_temp()

        if self.current_token == Token.SOMA:
            self.consume_token(Token.SOMA)
            _, codu, tempu = self.mult()
            _, codr, _ = self.resto_add(valor)

            comando = ('+', temp, valor, tempu)
            codu.append(comando)
            return False, codu + codr, temp

        elif self.current_token == Token.SUBT:
            self.consume_token(Token.SUBT)
            _, codu, tempu = self.mult()
            _, codr, _ = self.resto_add(valor)

            comando = ('-', temp, valor, tempu)
            codu.append(comando)
            return False, codu + codr, temp

        else:
            return True, [], valor
    
    def mult(self):
        is_lvu, codu, tempu = self.uno()
        is_lvr, codr, tempr = self.resto_mult(tempu)

        return (is_lvu and is_lvr, codu + codr, tempr)
    
    def resto_mult(self, valor):
        temp = self.next_temp()

        if self.current_token == Token.MULT:
            self.consume_token(Token.MULT)
            _, codu, tempu = self.uno()
            _, codr, _ = self.resto_mult(valor)

            comando = ('*', temp, valor, tempu)
            codu.append(comando)
            return False, codu + codr, temp

        elif self.current_token == Token.DIV:
            self.consume_token(Token.DIV)
            _, codu, tempu = self.uno()
            _, codr, _ = self.resto_mult(valor)

            comando = ('/', temp, valor, tempu)
            codu.append(comando)
            return False, codu + codr, temp

        elif self.current_token == Token.MODU:
            self.consume_token(Token.MODU)
            _, codu, tempu = self.uno()
            _, codr, _ = self.resto_mult(valor)

            comando = ('%', temp, valor, tempu)
            codu.append(comando)
            return False, codu + codr, temp

        else:
            return (True, [], valor)
    
    def uno(self):
        temp = self.next_temp()

        if self.current_token == Token.SOMA:
            op = '+'
            self.consume_token(Token.SOMA)
        elif self.current_token == Token.SUBT:
            op = '-'
            self.consume_token(Token.SUBT)
        else:
            return self.fator()

        cod.append((op, temp, 0, ident))
        return False, cod, temp
    
    def fator(self):
        temp = self.next_temp()
        ident = self.lexer.lexeme
        
        if self.current_token == Token.NUMINT:
            self.consume_token(Token.NUMINT)
            return False, [('=', temp, int(ident), None)], temp
        elif self.current_token == Token.NUMFLOAT:
            self.consume_token(Token.NUMFLOAT)
            return False, [('=', temp, float(ident), None)], temp
        elif self.current_token == Token.IDENT:
            self.consume_token(Token.IDENT)
            
            ident = self.busca_var(ident)
            
            return True, [], ident
        else:
            self.consume_token(Token.ABREPAR)
            cod, res = self.atrib()
            self.consume_token(Token.FECHAPAR)

            cod.append(('=', temp, res, None))
            return False, cod, temp
        
    def parse(self):
        try:
            self.current_token = self.lexer.get_token()
            cod = self.function(None, None)
            self.consume_token(Token.EOF)
            cod.append(('stop', None, None, None))
            return cod
        except ParseError as error:
            print(error)
            self.symbol_table = {}
