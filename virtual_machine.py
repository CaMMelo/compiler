import os

# instruction is: (operation, A, B, C)

def operation(foo):

    def wrapper(vm, a, b, c):
        b = vm.avalia(b)
        c = vm.avalia(c)

        return foo(vm, a, b, c)

    return wrapper


class MiniCVM:

    def __init__(self):
        
        self.symbol_table = {}
        self.labels = {}

        self.instructions = {
        	'='    : self.atrib,
        	'label': self.label,
        	'if'   : self.if_,
        	'jump' : self.jump,
        	'call' : self.call,
            'stop' : self.stop,
        	'or'   : self.or_,
        	'and'  : self.and_,
        	'not'  : self.not_,
        	'=='   : self.equals,
        	'!='   : self.nequals,
        	'>='   : self.gteq,
        	'<='   : self.lteq,
        	'>'    : self.gt,
        	'<'    : self.lt,
        	'+'    : self.sum,
        	'-'    : self.subt,
        	'*'    : self.mult,
        	'%'    : self.mod,
        	'/'    : self.div,
        }

    def valor(self, name):
        return self.symbol_table[name][0]

    def tipo(self, name):
        return self.symbol_table[name][1]

    def avalia(self, var):
        if var in self.symbol_table:
            return self.valor(var)
        return var

    def atrib(self, a, b, c):
        b = self.avalia(b)
        self.symbol_table[a] = b, float

    def label(self, a, b, c):
        pass

    def if_(self, a, b, c):
        a = self.avalia(a)
        goto = b if a != 0 else c
        self.jump(goto, None, None)

    def jump(self, a, b, c):
        if a in self.labels:
            self.pc = self.labels[a]

    def stop(self, a, b, c):
        self.pc = -1

    def call(self, a, b, c):
        if a == 'scan':
            tipo = self.tipo(b)
            try:
                self.symbol_table[b] = tipo(input()), tipo
            except:
                self.symbol_table[b] = tipo(0), tipo
        elif a == 'print':
            b = self.avalia(b)
            print(b, end='')

    @operation
    def or_(self, a, b, c):
        self.symbol_table[a] = int(b or c), int

    @operation
    def and_(self, a, b, c):
        self.symbol_table[a] = int(b and c), int

    @operation
    def not_(self, a, b, c):
        self.symbol_table[a] = int(not b), int

    @operation
    def equals(self, a, b, c):
        self.symbol_table[a] = int(b == c), int

    @operation
    def nequals(self, a, b, c):
        self.symbol_table[a] = int(b != c), int

    @operation
    def gteq(self, a, b, c):
        self.symbol_table[a] = int(b >= c), int

    @operation
    def lteq(self, a, b, c):
        self.symbol_table[a] = int(b <= c), int

    @operation
    def gt(self, a, b, c):
        self.symbol_table[a] = int(b > c), int

    @operation
    def lt(self, a, b, c):
        self.symbol_table[a] = int(b < c), int

    @operation
    def sum(self, a, b, c):
        self.symbol_table[a] = b + c, float

    @operation
    def subt(self, a, b, c):
        self.symbol_table[a] = b - c, float

    @operation
    def mult(self, a, b, c):
        self.symbol_table[a] = b * c, float

    @operation
    def mod(self, a, b, c):
        self.symbol_table[a] = int(b % c), int

    @operation
    def div(self, a, b, c):
        self.symbol_table[a] = b / c, float

    def fetch(self):
        c = self.program[self.pc]
        self.pc += 1
        return c

    def exec(self, program):

        self.program = program
        self.pc = 0

        for i, command in enumerate(self.program):
            print(command)
            instr, a, _, _ = command
            if instr == 'label':
                self.labels[a] = i

        while self.pc >= 0:
            instr, a, b, c, = self.fetch()
            self.instructions[instr](a, b, c)
