

# instruction is: (operation, A, B, C)

class MiniCVM:

    def __init__(self):
        
        self.vars = {}
        self.instructions = {}
    
    def exec(self, loi):

        for command in loi:
            instr, a, b, c = command
            self.instructions[instr](a, b, c)