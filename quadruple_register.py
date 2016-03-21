from semantic_cube import SemanticCube

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

    def __init__(self):
        self.semantic_cube = SemanticCube()
        self.temp_count = 1
        self.count = 0
        self.quadruple_list = []
        self.operand_stack = []
        self.operator_stack = []

    def push_operand(self, operand):
        if operand is None:
            print('Error: undefined variable')
        self.operand_stack.append(operand)

    def push_operator(self, operator):
        operator = self.__to_opcode(operator)
        self.operator_stack.append(operator)

    def push_fake_bottom(self):
        self.operator_stack.append(QuadrupleRegister.FAKE_BOTTOM)

    def pop_fake_bottom(self):
        if self.operator_stack[-1] == QuadrupleRegister.FAKE_BOTTOM:
            self.operator_stack.pop()
        else:
            print('Error: parenthesis mismatch')

    def push_int_literal(self, literal):
        literal = dict(name = '_lit' + str(literal), type = SemanticCube.INT)
        self.operand_stack.append(literal)

    def push_float_literal(self, literal):
        literal = dict(name = '_lit' + str(literal), type = SemanticCube.FLOAT)
        self.operand_stack.append(literal)

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
        operator = self.operator_stack[-1] if self.operator_stack else None
        if (operator == QuadrupleRegister.GREATER or
            operator == QuadrupleRegister.LESSER or
            operator == QuadrupleRegister.EQUAL or
            operator == QuadrupleRegister.NOT_EQUAL):
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
            self.generate(operator, operand['name'], None, assigned['name'])

    def generate(self, operator, operand_1, operand_2, result):
        quadruple = dict(operator = operator, operand_1 = operand_1, operand_2 = operand_2, result = result)
        self.quadruple_list.append(quadruple)
        print('Added quadruple')
        print('Operators: '  + str(self.operator_stack))
        print('Operands: '  + str(self.operand_stack))

    def print_quadruple(self):
        for quadruple in self.quadruple_list:
            print('Operator: ' + str(quadruple['operator']) +
                ' Operand 1: ' + str(quadruple['operand_1']) +
                ' Operand 2: ' + str(quadruple['operand_2']) +
                ' Result: ' + str(quadruple['result']))

    def __new_temp_var(self, var_type):
        var = dict(name = 't' + str(self.temp_count), type = var_type)
        self.temp_count += 1
        self.operand_stack.append(var)
        return var['name']

    def __arithmetic_check(self, operator):
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        result_type = self.semantic_cube.get_result_type(operand_1['type'], operand_2['type'], operator)
        if result_type is not None:
            self.generate(operator, operand_1['name'], operand_2['name'], self.__new_temp_var(result_type))
        else:
            print('Error: Type mismatch')

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
        else:
            print ('Error: unknown operator ' + operator_s)
            return None






