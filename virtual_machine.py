from memory_map import MemoryMap
from constant_table import ConstantTable


class VirtualMachine:

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

    POINTERS_BASE = 40000

    def __init__(self, quadruples, constants, functions):
        print("///////////////////////////// Virtual Machine init ///////////////////////")
        self.constant_table = ConstantTable()
        for constant in constants:
            self.constant_table.add_constant(constant['address'], constant['name'])

        self.quadruple_list = quadruples
        self.constant_memory = self.constant_table.table
        self.memory_map = MemoryMap(self.constant_table, functions)
        self.memory_stack = []
        self.current_quadruple = 0

    def execute_code(self):
        print('================Ejecutando maquina virtual==========================')
        while self.current_quadruple < len(self.quadruple_list):
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            self.options[action](self,quadruple)
            self.current_quadruple = self.current_quadruple + 1

        print(" ================ Termina ejecucion de cuadruplos ==================")

    def op_multiplication(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 * operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " * " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_division(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " / " + str(operand2))

        result = operand1 / operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " / " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_sum(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 + operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " + " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_substraction(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 - operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " - " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_greater(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 > operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " > " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_lesser(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 < operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " < " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_equal(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 == operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " == " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_not_equal(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 != operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " != " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_and(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 and operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " && " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_or(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 or operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " || " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_assignment(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(result_dir) + " = " + str(operand1))

        self.memory_map.set_value(result_dir, operand1)

    def op_mayor_igual(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 >= operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " >= " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_menor_igual(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = memory_map.get_value(operand1_dir)
        operand2 = memory_map.get_value(operand2_dir)
        result = operand1 <= operand2

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        print(" * " + str(operand1) + " <= " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_goto(self, quad):
        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")

        self.current_quadruple = int(quad['result'])

        print(" * GoTo: " + str(self.current_quadruple))

        quadruple = self.quadruple_list[self.current_quadruple];
        action = quadruple['operator']
        self.options[action](self, quadruple)

    def op_gotof(self, quad):
        operand1_dir = int(quad['operand_1'])
        result = int(quad['result'])

        condition = self.memory_map.get_value(operand1_dir)

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * GoToF: " + str(result) + "  condition: " + str(operand1_dir))

        if(not(condition)):
            self.current_quadruple = quad['result']
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            self.options[action](self, quadruple)

    def op_gotot(self, quad):
        operand1_dir = int(quad['operand_1'])
        result = int(quad['result'])

        condition = self.memory_map.get_value(operand1_dir)

        print(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        print(" * GoToT: " + str(result) + "  condition: " + str(operand1_dir))

        if(condition):
            self.current_quadruple = quad['result']
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            self.options[action](self, quadruple)


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
