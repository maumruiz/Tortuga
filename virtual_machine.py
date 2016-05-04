from memory_map import MemoryMap
from constant_table import ConstantTable
from semantic_cube import SemanticCube
from logger import Logger
import sys
import turtle


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

    POINTER_BASE = 40000

    def __init__(self, quadruples, constants, functions):
        self.log = Logger(False)
        self.log.write("///////////////////////////// Virtual Machine init ///////////////////////")
        self.constant_table = ConstantTable()
        for constant in constants:
            self.constant_table.add_constant(constant['address'], constant['name'])

        self.quadruple_list = quadruples
        self.constant_memory = self.constant_table.table
        self.memory_map = MemoryMap(self.constant_table, functions)
        self.current_quadruple = 0
        self.return_stack = []
        self.saved_position = (0, 0)

    def execute_code(self):
        self.log.write('================Ejecutando maquina virtual==========================')
        turtle.mode("logo")
        while self.current_quadruple < len(self.quadruple_list):
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            self.options[action](self,quadruple)
            self.current_quadruple = self.current_quadruple + 1

        self.log.write(" ================ Termina ejecucion de cuadruplos ==================")

    def op_multiplication(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 * operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " * " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_division(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)

        result = operand1 / operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " / " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_sum(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 + operand2

        if result_dir >= MemoryMap.POINTER_BASE:
            operand2 = operand2_dir
            result = operand1 + operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " + " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_substraction(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 - operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " - " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_greater(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 > operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " > " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_lesser(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 < operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " < " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_equal(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 == operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " == " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_not_equal(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 != operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " != " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_and(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 and operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " && " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_or(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 or operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " || " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_assignment(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)

        if result_dir >= MemoryMap.POINTER_BASE:
            result_dir = self.memory_map.get_pointer_address(result_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(result_dir) + " = " + str(operand1))

        self.memory_map.set_value(result_dir, operand1)

    def op_mayor_igual(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 >= operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " >= " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_menor_igual(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 <= operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " <= " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    def op_goto(self, quad):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")

        self.current_quadruple = int(quad['result'])

        self.log.write(" * GoTo: " + str(self.current_quadruple))

        quadruple = self.quadruple_list[self.current_quadruple];
        action = quadruple['operator']
        self.options[action](self, quadruple)

    def op_gotof(self, quad):
        operand1_dir = int(quad['operand_1'])
        result = int(quad['result'])

        condition = self.memory_map.get_value(operand1_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * GoToF: " + str(result) + "  condition: " + str(operand1_dir))

        if(not(condition)):
            self.current_quadruple = quad['result']
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            self.options[action](self, quadruple)

    def op_gotot(self, quad):
        operand1_dir = int(quad['operand_1'])
        result = int(quad['result'])

        condition = self.memory_map.get_value(operand1_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * GoToT: " + str(result) + "  condition: " + str(operand1_dir))

        if(condition):
            self.current_quadruple = quad['result']
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            self.options[action](self, quadruple)

    def op_era(self, quadruple):
        self.memory_map.nested_call_level += 1

        func_name = quadruple['operand_1']

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * era: " + str(func_name))

        self.memory_map.push_local(func_name)

    def op_gosub(self, quadruple):
        self.memory_map.nested_call_level -= 1

        func_dir = int(quadruple['operand_1'])

        self.return_stack.append(self.current_quadruple + 1)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * gosub: " + str(func_dir))
        self.log.write(" * Return stack: " + str(self.return_stack))

        self.current_quadruple = func_dir
        quadruple = self.quadruple_list[self.current_quadruple];
        action = quadruple['operator']
        self.options[action](self, quadruple)

    def op_ret_act(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * return to func call: ")
        self.log.write(" * return stack: " + str(self.return_stack))

        self.memory_map.pop_local()
        self.current_quadruple = self.return_stack.pop()
        quadruple = self.quadruple_list[self.current_quadruple];
        action = quadruple['operator']
        self.options[action](self, quadruple)

    def op_return(self, quadruple):
        pass

    def op_param(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        result_dir = int(quadruple['result'])

        param_value = self.memory_map.get_param_value(operand1_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * param: " + str(result_dir) + " = " + str(param_value))

        self.memory_map.set_value(result_dir, param_value)

    def op_verify(self, quadruple):
        operand1 = int(quadruple['operand_1'])
        operand2 = int(quadruple['operand_2'])
        subject_dir = int(quadruple['result'])

        value = self.memory_map.get_value(subject_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * verify: " + str(value) + " | " + str(operand1) + '-' + str(operand2))

        if value < operand1 or value >= operand2:
            self.log.write('Error: Indice fuera de los limites')
            exit(1)

    def read(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        value = self.memory_map.read_by_type(operand1_dir)
        self.log.write(" * read: " + str(value) + '->' + str(operand1_dir))

        self.memory_map.set_value(operand1_dir, value)

    def write(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * write: " + str(operand1_dir))
        print(str(operand1)) 

    def forward(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * forward: " + str(operand1))
        turtle.forward(operand1)

    def backward(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * backward: " + str(operand1))
        turtle.backward(operand1)

    def right(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * right: " + str(operand1))
        turtle.right(operand1)

    def left(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * left: " + str(operand1))
        turtle.left(operand1)

    def pos(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pos: " + str(operand1) + ' ' + str(operand1))
        turtle.setposition(operand1, operand2)

    def pos_x(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pos_x: " + str(operand1))
        turtle.setx(operand1)

    def pos_y(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pos_y: " + str(operand1))
        turtle.sety(operand1)

    def line_color(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        operand3_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        operand3 = self.memory_map.get_value(operand3_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * line_color: " + str(operand1) + ' ' + str(operand1) + ' ' + str(operand3))
        turtle.colormode(255)
        turtle.pencolor(operand1, operand2, operand3)

    def line_width(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * line_width: " + str(operand1))
        turtle.pensize(operand1)

    def pen_up(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pen_up: ")
        turtle.penup()

    def pen_down(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pen_down: ")
        turtle.pendown()

    def fill_true(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_true: ")
        turtle.begin_fill()

    def fill_false(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_false: ")
        turtle.end_fill()

    def fill_color(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        operand3_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        operand3 = self.memory_map.get_value(operand3_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_color: " + str(operand1) + ' ' + str(operand1) + ' ' + str(operand3))
        turtle.colormode(255)
        turtle.fillcolor(operand1, operand2, operand3)

    def background_color(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        operand3_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        operand3 = self.memory_map.get_value(operand3_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * background_color: " + str(operand1) + ' ' + str(operand1) + ' ' + str(operand3))
        turtle.colormode(255)
        turtle.bgcolor(operand1, operand2, operand3)

    def save_pos(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_true: ")
        self.saved_position = turtle.pos()

    def restore_pos(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_true: ")
        turtle.setposition(self.saved_position[0], self.saved_position[1])

    def random(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * random: " + str(operand1))
        # turtle.pensize(operand1)

    def circle(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * circle: " + str(operand1) + ' ' + str(operand1))
        turtle.circle(operand1, operand2)

    def op_end(self, quad):
        turtle.done()
        self.log.write(" end ")


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
                16: op_param,
                17: op_era,
                18: op_gosub,
                19: op_ret_act,
                20: op_return,
                21: op_verify,
                101: read,
                102: write,
                103: forward,
                104: backward,
                105: right,
                106: left,
                107: pos,
                108: pos_x,
                109: pos_y,
                110: line_color,
                111: line_width,
                112: pen_up,
                113: pen_down,
                114: fill_true,
                115: fill_false,
                116: fill_color,
                117: background_color,
                118: save_pos,
                119: restore_pos,
                120: random,
                121: circle,
                "end": op_end,
    }
