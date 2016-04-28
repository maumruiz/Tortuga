from semantic_cube import SemanticCube
from virtual_address_handler import VirtualAddressHandler
from constant_handler import ConstantHandler
from virtual_machine import VirtualMachine
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

    def __init__(self):
        self.semantic_cube = SemanticCube()
        self.temp_count = 1
        self.count = 0
        self.quadruple_list = []
        self.operand_stack = []
        self.operator_stack = []
        self.jump_stack = []
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
        self.operand_stack.append(constant)

    def push_string_literal(self, literal):
        constant = self.constant_handler.find_or_init_string_constant(literal)
        self.constant_list.append(constant)
        self.operand_stack.append(constant)

    def push_bool_literal(self, literal):
        constant = self.constant_handler.assign_boolean_constant(literal)
        self.constant_list.append(constant)
        self.operand_stack.append(constant)

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
            sys.exit('Semantic error: If statement requires a bool expression')
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
        self.jump_stack.append(len(self.quadruple_list))

    def end_repeat_check(self):
        print('Pending')

    def generate(self, operator, operand_1, operand_2, result):
        quadruple = dict(operator = operator, operand_1 = operand_1, operand_2 = operand_2, result = result)
        self.quadruple_list.append(quadruple)
        #print('Added quadruple')
        #print('Operators: '  + str(self.operator_stack))
        #print('Operands: '  + str(self.operand_stack))
        #print(self.quadruple_list)

    def fill_quadruple(self, index, content):
        quadruple = self.quadruple_list[index]
        quadruple['result'] = content

    def print_debug_quadruples(self):
        for quadruple in self.quadruple_list:
            print('Operator: ' + str(quadruple['operator']) +
                ' Operand1: ' + str(quadruple['operand_1']) +
                ' Operand2: ' + str(quadruple['operand_2']) +
                ' Result: ' + str(quadruple['result']))
        # print(self.operand_stack)
        # print(self.operator_stack)

    def print_constants(self):
        for constant in self.constant_list:
            address = constant['address']
            value = constant['name']
            print(str(address) + ' ' + str(value))

    def print_quadruples(self):
        for quadruple in self.quadruple_list:
            operator = quadruple['operator']
            operand_1 = quadruple['operand_1']['address']
            operand_2 = quadruple['operand_2']
            operand_2_address = ''
            result = quadruple['result']
            if operand_2 is not None:
                operand_2_address = str(operand_2['address'])
            if isinstance(result, dict):
                result = result['address']
            print(str(operator) + ' ' + str(operand_1) + ' ' + operand_2_address + ' ' + str(result))



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
            print('Error desconocido')
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

    def execute_quadruples(self):
        self.vm = VirtualMachine(self.quadruple_list, self.constant_list)
        self.vm.execute_code()

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
