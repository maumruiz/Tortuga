class maquinaVirtual:

    options = {0 : op_multiplication,
                1: op_division,
                2: op_sum,
                3: op_substraction,
                4: op_greater,
                5: op_lesser,
                6: op_equal,
                7: op_not_equal,
                8: op_and,
                9: op_or,
                10: op_assignment,
                11: op_mayor_igual,
                12: op_menor_igual,
                13: op_goto,
                14: op_gotof,
                15: op_gotot,
    }

    def __init__(self):
        self.code = []
        self.global_memory = []
        self.current = 0

        self.dirBaseConstInt = 0
        self.dirBaseConstFloat = 1000
        self.dirBaseConstString = 2000
        self.dirBaseConstBool = 3000
        self.dirBaseConstExtra = 4000
        self.dirBaseGlobalInt = 10000
        self.dirBaseGlobalFloat = 11000
        self.dirBaseGlobalString = 12000
        self.dirBaseGlobalBool = 13000
        self.dirBaseGlobalExtra = 14000
        self.dirBaseLocalInt = 20000
        self.dirBaseLocalFloat = 21000
        self.dirBaseLocalString = 22000
        self.dirBaseLocalBool = 23000
        self.dirBaseLocalExtra = 24000
        self.dirBaseTempInt = 30000
        self.dirBaseTempFloat = 31000
        self.dirBaseTempString = 32000
        self.dirBaseTempBool = 33000
        self.dirBaseTempExtra = 34000

    def set_code(self, quadruple_list):
        self.code = quadruple_list

    def set_global_memory(self):
        return

    def execute_code(self):
        options[0]()
        return

    def op_goto(self):
        result = self.global_memory[self.code[current]['result']]
        options[self.result]()

    def op_gotof(self):
        if self.code[self.current]['operand_1'] >= self.dirBaseConstBool and self.code[self.current]['operand_1'] < self.dirBaseConstExtra:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseConstBool]
        elif self.code[self.current]['operand_1'] >= self.dirBaseGlobalBool and self.code[self.current]['operand_1'] < self.dirBaseGlobalExtra:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseGlobalBool]
        elif self.code[self.current]['operand_1'] >= self.dirBaseLocalBool and self.code[self.current]['operand_1'] < self.dirBaseLocalExtra:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseLocalBool]
        elif self.code[self.current]['operand_1'] >= self.dirBaseTempBool and self.code[self.current]['operand_1'] < self.dirBaseTempExtra:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseTempBool]

    def op_multiplication():
        if self.code[self.current]['operand_1'] >= self.dirBaseConstInt and self.code[self.current]['operand_1'] < self.dirBaseConstFloat:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseConstInt]
        elif self.code[self.current]['operand_1']  >= self.dirBaseConstFloat and self.code[self.current]['operand_1'] < self.dirBaseConstString:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseConstFloat]
        elif self.code[self.current]['operand_1'] >= self.dirBaseGlobalInt and self.code[self.current]['operand_1'] < self.dirBaseGlobalFloat:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseGlobalInt]
        elif self.code[self.current]['operand_1']  >= self.dirBaseGlobalFloat and self.code[self.current]['operand_1'] < self.dirBaseGlobalString:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseGlobalFloat]
        elif self.code[self.current]['operand_1'] >= self.dirBaseLocalInt and self.code[self.current]['operand_1'] < self.dirBaseLocalFloat:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseLocalInt]
        elif self.code[self.current]['operand_1']  >= self.dirBaseLocalFloat and self.code[self.current]['operand_1'] < self.dirBaseLocalString:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseLocalFloat]
        elif self.code[self.current]['operand_1'] >= self.dirBaseTempInt and self.code[self.current]['operand_1'] < self.dirBaseTempFloat:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseTempInt]
        elif self.code[self.current]['operand_1']  >= self.dirBaseTempFloat and self.code[self.current]['operand_1'] < self.dirBaseTempString:
            operand1 = self.global_memory[self.code[self.current]['operand_1'] - self.dirBaseTempFloat]

        if self.code[self.current]['operand_2'] >= self.dirBaseConstInt and self.code[self.current]['operand_2'] < self.dirBaseConstFloat:
            operand2 = self.global_memory[self.code[self.current]['operand_2'] - self.dirBaseConstInt]
        elif self.code[self.current]['operand_2']  >= self.dirBaseConstFloat and self.code[self.current]['operand_2'] < self.dirBaseConstString:
            operand2 = self.global_memory[self.code[self.current]['operand_2'] - self.dirBaseConstFloat]
        elif self.code[self.current]['operand_2'] >= self.dirBaseGlobalInt and self.code[self.current]['operand_2'] < self.dirBaseGlobalFloat:
            operand_2 = self.global_memory[self.code[self.current]['operand_2'] - self.dirBaseGlobalInt]
        elif self.code[self.current]['operand_2']  >= self.dirBaseGlobalFloat and self.code[self.current]['operand_2'] < self.dirBaseGlobalString:
            operand_2 = self.global_memory[self.code[self.current]['operand_2'] - self.dirBaseGlobalFloat]
        elif self.code[self.current]['operand_2'] >= self.dirBaseLocalInt and self.code[self.current]['operand_2'] < self.dirBaseLocalFloat:
            operand_2 = self.global_memory[self.code[self.current]['operand_2'] - self.dirBaseLocalInt]
        elif self.code[self.current]['operand_2']  >= self.dirBaseLocalFloat and self.code[self.current]['operand_2'] < self.dirBaseLocalString:
            operand_2 = self.global_memory[self.code[self.current]['operand_2'] - self.dirBaseLocalFloat]
        elif self.code[self.current]['operand_2'] >= self.dirBaseTempInt and self.code[self.current]['operand_2'] < self.dirBaseTempFloat:
            operand_2 = self.global_memory[self.code[self.current]['operand_2'] - self.dirBaseTempInt]
        elif self.code[self.current]['operand_2']  >= self.dirBaseTempFloat and self.code[self.current]['operand_2'] < self.dirBaseTempString:
            operand_2 = self.global_memory[self.code[self.current]['operand_2'] - self.dirBaseTempFloat]

        result = operand1 * operand2
        self.global_memory[self.code[self.current]['result']] = result
