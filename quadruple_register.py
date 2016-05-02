from semantic_cube import SemanticCube
from virtual_address_handler import VirtualAddressHandler
from constant_handler import ConstantHandler
from op_codes import OpCodes
import sys

class QuadrupleRegister:
    FAKE_BOTTOM = -1
    MULTIPLICATION = 0
    DIVISION = 1
    SUM = 2
    SUBSTRACTION = 3
    GREATER = 4
    LESSER = 5
    EQUAL = 6
    NOT_EQUAL = 7
    AND = 8
    OR = 9
    ASSIGNMENT = 10
    MAYOR_IGUAL = 11
    MENOR_IGUAL = 12
    GOTO = 13
    GOTOF = 14
    GOTOT = 15
    PARAM = 16
    ERA = 17
    GOSUB = 18
    RET = 19
    RETURN = 20

    def __init__(self):
        self.semantic_cube = SemanticCube()
        self.temp_count = 1
        self.count = 0
        self.quadruple_list = []
        self.operand_stack = []
        self.operator_stack = []
        self.jump_stack = []
        self.repeat_stack = []
        self.constant_list = []
        self.address_handler = VirtualAddressHandler()
        self.constant_handler = ConstantHandler(self.address_handler)

    def push_operand(self, operand):
        if operand is None:
            print('Error: undefined variable')
            exit(0)
        self.operand_stack.append(operand)

    def push_operator(self, operator):
        operator = self.__to_opcode(operator)
        print('Pushing operator: ' +  str(operator))
        self.operator_stack.append(operator)
        print(self.operator_stack)

    def push_fake_bottom(self):
        self.operator_stack.append(QuadrupleRegister.FAKE_BOTTOM)

    def pop_fake_bottom(self):
        if self.operator_stack[-1] == QuadrupleRegister.FAKE_BOTTOM:
            self.operator_stack.pop()
        else:
            print('Error: parenthesis mismatch')
            exit(0)

    def push_int_literal(self, literal):
        constant = self.constant_handler.find_or_init_int_constant(literal)
        self.constant_list.append(constant)
        self.operand_stack.append(constant)

    def push_float_literal(self, literal):
        constant = self.constant_handler.find_or_init_float_constant(literal)
        self.constant_list.append(constant)
        self.operand_stack.append(constant)

    def push_string_literal(self, literal):
        string_lit = literal[1:-1]
        constant = self.constant_handler.find_or_init_string_constant(string_lit)
        self.constant_list.append(constant)
        self.operand_stack.append(constant)

    def push_bool_literal(self, literal):
        constant = self.constant_handler.assign_boolean_constant(literal)
        #self.constant_list.append(constant)
        self.operand_stack.append(constant)

    def push_function_return(self, return_type, function_variable):
        temp_var = self.__new_temp_var(return_type)
        self.generate(OpCodes.ASSIGNMENT, function_variable, None, temp_var)

    def term_check(self):
        operator = self.operator_stack[-1] if self.operator_stack else None
        if operator == QuadrupleRegister.MULTIPLICATION or operator == QuadrupleRegister.DIVISION:
            self.operator_stack.pop()
            self.__arithmetic_check(operator)

    def exp_check(self):
        operator = self.operator_stack[-1] if self.operator_stack else None
        if operator == QuadrupleRegister.SUM or operator == QuadrupleRegister.SUBSTRACTION:
            self.operator_stack.pop()
            self.__arithmetic_check(operator)

    def sexp_check(self):
        print(self.operator_stack)
        operator = self.operator_stack[-1] if self.operator_stack else None
        if (operator == QuadrupleRegister.GREATER or
            operator == QuadrupleRegister.LESSER or
            operator == QuadrupleRegister.EQUAL or
            operator == QuadrupleRegister.NOT_EQUAL or
            operator == QuadrupleRegister.MAYOR_IGUAL or
            operator == QuadrupleRegister.MENOR_IGUAL):
            self.operator_stack.pop()
            self.__arithmetic_check(operator)

    def ssexp_check(self):
        operator = self.operator_stack[-1] if self.operator_stack else None
        if operator == QuadrupleRegister.AND or operator == QuadrupleRegister.OR:
            self.operator_stack.pop()
            self.__arithmetic_check(operator)

    def assignment_check(self):
        operator = self.operator_stack[-1] if self.operator_stack else None
        if operator == QuadrupleRegister.ASSIGNMENT:
            self.operator_stack.pop()
            operand = self.operand_stack.pop()
            assigned = self.operand_stack.pop()
            print("Assigned type: " + str(assigned['type']) + "   Operand type: " + str(operand['type']))
            result_type = self.semantic_cube.get_result_type(assigned['type'], operand['type'], operator)
            print('Result Type in assignment ::::: ' + str(result_type))
            if result_type is not None:
                self.generate(operator, operand, None, assigned)
            else:
                print('Error: Assignment type mismatch with operands ' + assigned['name'] + ' and ' + operand['name'])
                exit(0)

    def begin_if_check(self):
        self.print_quadruples()
        operand = self.operand_stack.pop()
        if  operand['type'] != SemanticCube.BOOL:
            sys.exit('Error Semantico: El estatuto if requiere una expresión booleana')
        else:
            self.generate(QuadrupleRegister.GOTOF, operand, None, None)
            self.jump_stack.append(len(self.quadruple_list) - 1)

    def end_if_check(self):
        end = self.jump_stack.pop()
        self.fill_quadruple(end, len(self.quadruple_list))

    def else_check(self):
        self.generate(QuadrupleRegister.GOTO, None, None, None)
        false = self.jump_stack.pop()
        self.fill_quadruple(false, len(self.quadruple_list))
        self.jump_stack.append(len(self.quadruple_list) - 1)

    def begin_while_check(self):
        self.jump_stack.append(len(self.quadruple_list))

    def middle_while_check(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.BOOL:
            sys.exit('Semantic error: While statement requires a bool expression')
        else:
            self.generate(QuadrupleRegister.GOTOF, operand, None, None)
            self.jump_stack.append(len(self.quadruple_list) - 1)

    def end_while_check(self):
        false = self.jump_stack.pop()
        return_point = self.jump_stack.pop()
        self.generate(QuadrupleRegister.GOTO, None, None, return_point)
        self.fill_quadruple(false, len(self.quadruple_list))

    def begin_repeat_check(self):
        operand = self.operand_stack.pop()
        if operand['type'] == SemanticCube.INT:
            repeat_temp = self.__new_temp_var(SemanticCube.INT)
            self.generate(QuadrupleRegister.ASSIGNMENT, operand, None, repeat_temp)

            self.jump_stack.append(len(self.quadruple_list))
            c_zero = self.constant_handler.find_or_init_int_constant(0)
            self.constant_list.append(c_zero)
            temp_result = self.__new_temp_var(SemanticCube.BOOL)
            self.generate(QuadrupleRegister.GREATER, repeat_temp, c_zero, temp_result)

            self.generate(QuadrupleRegister.GOTOF, temp_result, None, None)
            self.jump_stack.append(len(self.quadruple_list) - 1)

            c_one = self.constant_handler.find_or_init_int_constant(1)
            self.constant_list.append(c_one)
            temp_result = self.__new_temp_var(SemanticCube.INT)
            self.generate(QuadrupleRegister.SUBSTRACTION, repeat_temp, c_one, repeat_temp)
        else:
            sys.exit('Semantic Error: Repeat statement requires an int expression')

    def end_repeat_check(self):
        false = self.jump_stack.pop()
        return_point = self.jump_stack.pop()
        self.generate(QuadrupleRegister.GOTO, None, None, return_point)
        self.fill_quadruple(false, len(self.quadruple_list))

    def generate_return_statement(self, function_variable):
        operand = self.operand_stack.pop()
        self.generate(OpCodes.ASSIGNMENT, operand, None, function_variable)

    def generate_era(self, function_name):
        self.generate(QuadrupleRegister.ERA, dict(name=function_name, address=function_name), None, None)

    def generate_return_action(self):
        self.generate(QuadrupleRegister.RET, None, None, None)

    def generate_gosub(self, start_quad):
        self.generate(QuadrupleRegister.GOSUB, dict(name=start_quad, address=start_quad), None, None)

    def verify_and_generate_argument(self, arg, arg_count, param_max):
        if(arg_count > param_max):
            sys.exit(" Error: el número de parámetros es incorrecto")

        operand = self.operand_stack.pop()
        if operand['type'] != arg['type']:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(QuadrupleRegister.PARAM, operand, None, arg['address'])
            print("Argumento agregado: " + str(arg_count))

######################## FUNCIONES PRIMITIVAS ##################################

    def generate_read(self):
        operand = self.operand_stack.pop()
        self.generate(OpCodes.READ, operand, None, None)

    def generate_write(self):
        operand = self.operand_stack.pop()
        if operand['type'] == SemanticCube.STRING or operand['type'] == SemanticCube.FLOAT or operand['type'] == SemanticCube.INT:
            self.generate(OpCodes.WRITE, operand, None, None)
        else:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)

    def generate_forward(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.FORWARD, operand, None, None)

    def generate_backward(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.BACKWARD, operand, None, None)

    def generate_right(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.RIGHT, operand, None, None)

    def generate_left(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.LEFT, operand, None, None)

    def generate_pos(self):
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.POS, operand_1, operand_2, None)

    def generate_pos_x(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.POS_X, operand, None, None)

    def generate_pos_y(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.POS_Y, operand, None, None)

    def generate_line_color(self):
        operand_3 = self.operand_stack.pop()
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT or operand_3['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.LINE_COLOR, operand_1, operand_2, operand_3)

    def generate_line_width(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            print('Generando line width')
            self.generate(OpCodes.LINE_WIDTH, operand, None, None)

    def generate_pen_up(self):
        self.generate(OpCodes.PEN_UP, None, None, None)

    def generate_pen_down(self):
        self.generate(OpCodes.PEN_DOWN, None, None, None)

    def generate_fill_true(self):
        self.generate(OpCodes.FILL_TRUE, None, None, None)

    def generate_fill_false(self):
        self.generate(OpCodes.FILL_FALSE, None, None, None)

    def generate_fill_color(self):
        operand_3 = self.operand_stack.pop()
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT or operand_3['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.FILL_COLOR, operand_1, operand_2, operand_3)

    def generate_background_color(self):
        operand_3 = self.operand_stack.pop()
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT or operand_3['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            print('Generando background color')
            self.generate(OpCodes.BACKGROUND_COLOR, operand_1, operand_2, operand_3)

    def generate_save_position(self):
        self.generate(OpCodes.SAVE_POS, None, None, None)

    def generate_restore_position(self):
        self.generate(OpCodes.RESTORE_POS, None, None, None)

    def generate_random(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.RANDOM, operand, None, None)

    def generate_circle(self):
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT:
            print('Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.CIRCLE, operand_1, operand_2, None)

    def generate(self, operator, operand_1, operand_2, result):
        quadruple = dict(operator = operator, operand_1 = operand_1, operand_2 = operand_2, result = result)
        self.quadruple_list.append(quadruple)

    def fill_quadruple(self, index, content):
        quadruple = self.quadruple_list[index]
        quadruple['result'] = content

    def get_next_quadruple(self):
        return len(self.quadruple_list)

    def print_debug_quadruples(self):
        counter = 0
        for quadruple in self.quadruple_list:
            print('* Quadruple ' + str(counter))
            print(' Operator: ' + str(quadruple['operator']) +
                ' Operand1: ' + str(quadruple['operand_1']) +
                ' Operand2: ' + str(quadruple['operand_2']) +
                ' Result: ' + str(quadruple['result']))
            counter = counter + 1

    def print_constants(self):
        for constant in self.constant_list:
            address = constant['address']
            value = constant['name']
            print(str(address) + ' ' + str(value))

    def print_quadruples(self):
        counter = 0
        for quadruple in self.quadruple_list:
            operator = quadruple['operator']
            operand_1 = quadruple['operand_1']
            operand_2 = quadruple['operand_2']
            operand_2_address = ''
            result = quadruple['result']
            if isinstance(operand_1, dict):
                operand_1 = operand_1['address']
            if operand_2 is not None:
                if isinstance(operand_2, dict):
                    operand_2_address = str(operand_2['address'])
                else:
                    operand_2_address = operand_2
            if isinstance(result, dict):
                result = result['address']
            print('*Quadruple ' + str(counter) + ':   ' + str(operator) + ' ' + str(operand_1) + ' ' + operand_2_address + ' ' + str(result))
            counter = counter + 1

    def print_name_quadruples(self):
        counter = 0
        for quadruple in self.quadruple_list:
            operator = quadruple['operator']
            operand_1 = quadruple['operand_1']
            operand_2 = quadruple['operand_2']
            operand_2_address = ''
            result = quadruple['result']
            if isinstance(operand_1, dict):
                operand_1 = operand_1['name']
            if operand_2 is not None:
                operand_2_address = str(operand_2['name'])
            if isinstance(result, dict):
                result = result['name']
            print('*Quadruple ' + str(counter) + ':   ' + str(operator) + ' ' + str(operand_1) + ' ' + operand_2_address + ' ' + str(result))
            counter = counter + 1

    def __new_temp_var(self, var_type):
        if var_type == SemanticCube.INT:
            var = dict(name = 'ti' + str(self.address_handler.temp_int_count), type = var_type,
                       address = self.address_handler.next_temp_int_address())
        elif var_type == SemanticCube.FLOAT:
            var = dict(name = 'tf' + str(self.address_handler.temp_float_count), type = var_type,
                       address = self.address_handler.next_temp_float_address())
        elif var_type == SemanticCube.STRING:
            var = dict(name = 'ts' + str(self.address_handler.temp_string_count), type = var_type,
                       address = self.address_handler.next_temp_string_address())
        elif var_type == SemanticCube.BOOL:
            var = dict(name = 'tb' + str(self.address_handler.temp_bool_count), type = var_type,
                       address = self.address_handler.next_temp_bool_address())
        else:
            print('Error: Tipo ' + str(var_type) + ' desconocido')
            exit(2)
            return None

        self.temp_count += 1
        self.operand_stack.append(var)
        return var

    def __arithmetic_check(self, operator):
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        result_type = self.semantic_cube.get_result_type(operand_1['type'], operand_2['type'], operator)
        print('Result Type :::::::::::::::::: ' + str(result_type) + ' ' + str(operand_1)+ ' ' + str(operand_2))
        if result_type is not None:
            self.generate(operator, operand_1, operand_2, self.__new_temp_var(result_type))
        else:
            print('Error: Operation type mismatch with operands ' + operand_1['name'] + ' and ' + operand_2['name'])
            exit(0)

    def __to_opcode(self, operator_s):
        if operator_s == '*':
            return QuadrupleRegister.MULTIPLICATION
        elif operator_s == '/':
            return QuadrupleRegister.DIVISION
        elif operator_s == '+':
            return QuadrupleRegister.SUM
        elif operator_s == '-':
            return QuadrupleRegister.SUBSTRACTION
        elif operator_s == '>':
            return QuadrupleRegister.GREATER
        elif operator_s == '<':
            return QuadrupleRegister.LESSER
        elif operator_s == '==':
            return QuadrupleRegister.EQUAL
        elif operator_s == '!=':
            return QuadrupleRegister.NOT_EQUAL
        elif operator_s == '&&':
            return QuadrupleRegister.AND
        elif operator_s == '||':
            return QuadrupleRegister.OR
        elif operator_s == '=':
            return QuadrupleRegister.ASSIGNMENT
        elif operator_s == '>=':
            return QuadrupleRegister.MAYOR_IGUAL
        elif operator_s == '<=':
            return QuadrupleRegister.MENOR_IGUAL
        else:
            print ('Error: operador desconocido ' + operator_s)
            exit(1)
            return None
