class VirtualMachine:

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

    FALSE_CONSTANT = 0
    TRUE_CONSTANT = 1
    INT_CONSTANT_BASE = 1000
    FLOAT_CONSTANT_BASE = 2000
    STRING_CONSTANT_BASE = 3000

    INT_BASE = 10000
    FLOAT_BASE = 11000
    STRING_BASE = 12000
    BOOL_BASE = 13000

    LOCAL_INT_BASE = 20000
    LOCAL_FLOAT_BASE = 21000
    LOCAL_STRING_BASE = 22000
    LOCAL_BOOL_BASE = 23000

    TEMP_INT_BASE = 30000
    TEMP_FLOAT_BASE = 31000
    TEMP_STRING_BASE = 32000
    TEMP_BOOL_BASE = 33000

    def __init__(self, quadruples, memory):
        self.quadruple_list = quadruples
        self.memory_map = memory
        self.current_quadruple = 0

    def execute_code(self):
        print('Ejecutando maquina virtual')
        while self.current_quadruple < len(self.quadruple_list):
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            options[action](quadruple)
            self.current_quadruple = self.current_quadruple + 1

    def op_multiplication(self, quadruple):
        operand1_dir = quadruple['operand_1']
        operand2_dir = quadruple['operand_2']
        result_dir = quadruple['result']

        if operand1_dir < VirtualMachine.FLOAT_CONSTANT_BASE:
            operand1 = self.memory_map[operand1_dir - VirtualMachine.FLOAT_CONSTANT_BASE]
        elif operand1_dir < VirtualMachine.STRING_CONSTANT_BASE:
            operand1 = self.memory_map[operand1_dir - VirtualMachine.STRING_CONSTANT_BASE]
        elif operand1_dir < VirtualMachine.FLOAT_BASE:
            operand1 = self.memory_map[operand1_dir - VirtualMachine.FLOAT_BASE]
        elif operand1_dir < VirtualMachine.STRING_BASE:
            operand1 = self.memory_map[operand1_dir - VirtualMachine.STRING_BASE]
        elif operand1_dir < VirtualMachine.LOCAL_FLOAT_BASE:
            operand1 = self.memory_map[operand1_dir - VirtualMachine.LOCAL_FLOAT_BASE]
        elif operand1_dir < VirtualMachine.LOCAL_STRING_BASE:
            operand1 = self.memory_map[operand1_dir - VirtualMachine.LOCAL_STRING_BASE]
        elif operand1_dir < VirtualMachine.TEMP_FLOAT_BASE:
            operand1 = self.memory_map[operand1_dir - VirtualMachine.TEMP_FLOAT_BASE]
        elif operand1_dir < VirtualMachine.TEMP_STRING_BASE:
            operand1 = self.memory_map[operand1_dir - VirtualMachine.TEMP_STRING_BASE]

        if operand2_dir < VirtualMachine.FLOAT_CONSTANT_BASE:
            operand2 = self.memory_map[operand2_dir - VirtualMachine.FLOAT_CONSTANT_BASE]
        elif operand2_dir < VirtualMachine.STRING_CONSTANT_BASE:
            operand2 = self.memory_map[operand2_dir - VirtualMachine.STRING_CONSTANT_BASE]
        elif operand2_dir < VirtualMachine.FLOAT_BASE:
            operand2 = self.memory_map[operand2_dir - VirtualMachine.FLOAT_BASE]
        elif operand2_dir < VirtualMachine.STRING_BASE:
            operand2 = self.memory_map[operand2_dir - VirtualMachine.STRING_BASE]
        elif operand2_dir < VirtualMachine.LOCAL_FLOAT_BASE:
            operand2 = self.memory_map[operand2_dir - VirtualMachine.LOCAL_FLOAT_BASE]
        elif operand2_dir < VirtualMachine.LOCAL_STRING_BASE:
            operand2 = self.memory_map[operand2_dir - VirtualMachine.LOCAL_STRING_BASE]
        elif operand2_dir < VirtualMachine.TEMP_FLOAT_BASE:
            operand2 = self.memory_map[operand2_dir - VirtualMachine.TEMP_FLOAT_BASE]
        elif operand2_dir < VirtualMachine.TEMP_STRING_BASE:
            operand2 = self.memory_map[operand2_dir - VirtualMachine.TEMP_STRING_BASE]

        result = operand1 * operand2
        self.global_memory[result_dir] = result

    def op_goto(self, quad):
        self.current_quadruple = self.global_memory[quad['result']]

        quadruple = self.quadruple_list[self.current_quadruple];
        action = quadruple['operator']
        options[action](quadruple)

    def op_gotof(self, quad):
        if quad['operand_1'] == 0
            condition = False
        elif quad['operand_1'] == 1
            condition = True
        elif quad['operand_1'] < VirtualMachine.LOCAL_INT_BASE:
            condition = self.global_memory[quad['operand_1'] - VirtualMachine.INT_CONSTANT_BASE]
        elif quad['operand_1'] < VirtualMachine.TEMP_INT_BASE:
            condition = self.global_memory[quad['operand_1'] - VirtualMachine.LOCAL_INT_BASE]
        else:
            condition = self.global_memory[quad['operand_1'] - VirtualMachine.TEMP_INT_BASE]

        if(not(condition))
            self.current_quadruple = self.global_memory[quad['result']]

            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            options[action](quadruple)
