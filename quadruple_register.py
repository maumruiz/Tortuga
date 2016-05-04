import ply.lex as lex
from semantic_cube import SemanticCube
from virtual_address_handler import VirtualAddressHandler
from constant_handler import ConstantHandler
from op_codes import OpCodes
from logger import Logger
import sys

class QuadrupleRegister:
    ''' Clase que se encarga del registro de cuádruplos, esta clase contiene el
        cubo semántico, las pilas de operadores y operandos, la pila de saltos,
        pila de repeticiones para el ciclo repetir, un objeto de la clase
        VirtualAddressHandler para asignar direcciones a variables y un
        ConstantHandler para manejar las constantes que se encuentren'''

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

    # La función init inicializa el cubo semántico, el contador de temporales en 1,
    # la lista de cuádruplos, pila de operandos, pila de operadores, la pila de saltos,
    # la pila del ciclo repeat, la lista de constantes, el address_handler y constant_handler
    def __init__(self, lexer):
        self.lexer = lexer
        self.semantic_cube = SemanticCube()
        self.temp_count = 1
        self.quadruple_list = []
        self.operand_stack = []
        self.operator_stack = []
        self.jump_stack = []
        self.repeat_stack = []
        self.constant_list = []
        self.address_handler = VirtualAddressHandler()
        self.constant_handler = ConstantHandler(self.address_handler)
        self.log = Logger(False)

    # La función push operand se encarga de aregar un operando a la lista de operandos
    def push_operand(self, operand):
        if operand is None:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: Variable no definida')
            exit(0)
        self.operand_stack.append(operand)

    # La función push_operator se encarga primero de convertir el operador que se
    # mande como argumento a su código entero, y después agregarlo a la lista de operadores
    def push_operator(self, operator):
        operator = self.__to_opcode(operator)
        self.log.write('Pushing operator: ' +  str(operator))
        self.operator_stack.append(operator)

    # La función push_fake_bottom se encarga de poner la marca de fondo FALSE_CONSTANT
    # en la pila de operadores
    def push_fake_bottom(self):
        self.operator_stack.append(QuadrupleRegister.FAKE_BOTTOM)

    # La función push_fake_bottom se encarga de sacar la marca de fondo FALSE_CONSTANT
    # en la pila de operadores. Si no encuentra un fondo falso al tope de la pila,
    # significa que hay un error en los paréntesis
    def pop_fake_bottom(self):
        if self.operator_stack[-1] == QuadrupleRegister.FAKE_BOTTOM:
            self.operator_stack.pop()
        else:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: los parentesis no coinciden')
            exit(0)

    # La función push_int_literal se encarga de mandar el literal al constant_handler
    # para conseguir la estructura de constante entera y agregarla a la lista de constantes
    # y a la pila de operandos
    def push_int_literal(self, literal):
        constant = self.constant_handler.find_or_init_int_constant(literal)
        self.constant_list.append(constant)
        self.operand_stack.append(constant)

    # La función push_float_literal se encarga de mandar el literal al constant_handler
    # para conseguir la estructura de constante flotante y agregarla a la lista de constantes
    # y a la pila de operandos
    def push_float_literal(self, literal):
        constant = self.constant_handler.find_or_init_float_constant(literal)
        self.constant_list.append(constant)
        self.operand_stack.append(constant)

    # La función push_float_string se encarga de mandar el literal al constant_handler
    # para conseguir la estructura de constante string y agregarla a la lista de constantes
    # y a la pila de operandos
    def push_string_literal(self, literal):
        string_lit = literal[1:-1]
        constant = self.constant_handler.find_or_init_string_constant(string_lit)
        self.constant_list.append(constant)
        self.operand_stack.append(constant)

    # La función push_bool_literal se encarga de mandar el literal al constant_handler
    # para conseguir la estructura de constante booleana y agregarla a la pila de operandos
    def push_bool_literal(self, literal):
        constant = self.constant_handler.assign_boolean_constant(literal)
        self.operand_stack.append(constant)

    # La función push_function_return recibe un tipo de retorno y una variable de función
    # para crear una nueva variable temporal y generar el cuádruplo de asignación de la
    # variable de función retornada a la variable temporal
    def push_function_return(self, return_type, function_variable):
        temp_var = self.__new_temp_var(return_type)
        self.generate(OpCodes.ASSIGNMENT, function_variable, None, temp_var)

    # La función term_check se encarga de ver si el siguiente operador es una multiplicación
    # o división. Si si es, saca el operador de la pila y llama a la función que checa
    # la aritmetica de tipos.
    def term_check(self):
        operator = self.operator_stack[-1] if self.operator_stack else None
        if operator == QuadrupleRegister.MULTIPLICATION or operator == QuadrupleRegister.DIVISION:
            self.operator_stack.pop()
            self.__arithmetic_check(operator)

    # La función exp_check se encarga de ver si el siguiente operador es una suma o una
    # resta. Si si es, saca el operador de la pila y llama a la función que checa
    # la aritmetica de tipos.
    def exp_check(self):
        operator = self.operator_stack[-1] if self.operator_stack else None
        if operator == QuadrupleRegister.SUM or operator == QuadrupleRegister.SUBSTRACTION:
            self.operator_stack.pop()
            self.__arithmetic_check(operator)

    # La función sexp_check se encarga de ver si el siguiente operador es un mayor, menor,
    # igual, diferente, mayor o igual o menor o igual. Si si es, saca el operador de la
    # pila y llama a la función que checa la aritmetica de tipos.
    def sexp_check(self):
        operator = self.operator_stack[-1] if self.operator_stack else None
        if (operator == QuadrupleRegister.GREATER or
            operator == QuadrupleRegister.LESSER or
            operator == QuadrupleRegister.EQUAL or
            operator == QuadrupleRegister.NOT_EQUAL or
            operator == QuadrupleRegister.MAYOR_IGUAL or
            operator == QuadrupleRegister.MENOR_IGUAL):
            self.operator_stack.pop()
            self.__arithmetic_check(operator)

    # La función ssexp_check se encarga de ver si el siguiente operador es un and o
    # un or. Si si es, saca el operador de la pila y llama a la función que checa
    # la aritmetica de tipos.
    def ssexp_check(self):
        operator = self.operator_stack[-1] if self.operator_stack else None
        if operator == QuadrupleRegister.AND or operator == QuadrupleRegister.OR:
            self.operator_stack.pop()
            self.__arithmetic_check(operator)

    # La función de assignment_check saca un operador de la lista. Si este operador
    # es una asignación, saca el el operando y la variable a la que se va a asignar
    # de la pila de operadores. Con estos dos, se revisa el tipo de la variable resultante,
    # y si es diferente de nulo, se crea el cuádruplo de asignación
    def assignment_check(self):
        operator = self.operator_stack[-1] if self.operator_stack else None
        if operator == QuadrupleRegister.ASSIGNMENT:
            self.operator_stack.pop()
            operand = self.operand_stack.pop()
            assigned = self.operand_stack.pop()
            self.log.write("Assigned type: " + str(assigned['type']) + "   Operand type: " + str(operand['type']) + '  Assigned address: ' + str(assigned['address']))
            result_type = self.semantic_cube.get_result_type(assigned['type'], operand['type'], operator)
            self.log.write('Result Type in assignment ::::: ' + str(result_type))
            if result_type is not None:
                self.generate(operator, operand, None, assigned)
            else:
                print(str(self.lexer.lineno) + ': ' + 'Error: Los tipos de datos en la asignación no coinciden')
                exit(0)

    # La función begin_if_check saca un operando de la lista de operandos, checa su tipo.
    # Si no es un booleano se manda un error requiriendo una expresión booleana para el if.
    # Si si es de tipo booleano, se genera el cuádruplo GoToF con este operando, y se agrega
    # el numero de cuádruplo a la pila de saltos
    def begin_if_check(self):
        self.print_quadruples()
        operand = self.operand_stack.pop()
        if  operand['type'] != SemanticCube.BOOL:
            sys.exit(str(self.lexer.lineno) + ': ' + 'Error Semantico: El estatuto if requiere una expresión booleana')
        else:
            self.generate(QuadrupleRegister.GOTOF, operand, None, None)
            self.jump_stack.append(len(self.quadruple_list) - 1)

    # La función if_check saca un elemento de la pila de saltos para llenar el cuadruplo
    # gotof del if con el número de cuadruplo actual
    def end_if_check(self):
        end = self.jump_stack.pop()
        self.fill_quadruple(end, len(self.quadruple_list))

    # La función else_check se encarga de generar un cuádruplo GoTo para cuando se llegue
    # desde un if. Después saca un elemento de la pila de saltos para llenar el cuadruplo
    # gotof del if con el número de cuadruplo actual y agrega el cuádruplo actual a la
    # pila de saltos.
    def else_check(self):
        self.generate(QuadrupleRegister.GOTO, None, None, None)
        false = self.jump_stack.pop()
        self.fill_quadruple(false, len(self.quadruple_list))
        self.jump_stack.append(len(self.quadruple_list) - 1)

    # La función begin_while_check mete el número de cuádruplo actual a la
    # pila de saltos
    def begin_while_check(self):
        self.jump_stack.append(len(self.quadruple_list))

    # La función de middle_while_check saca un operando de la pila de operandos y
    # checa su tipo. Si no es booleano, manda un error requiriendo una expresion booleana.
    # Si si es booleana, genera un cuádruplo GoToF con el operando, y agrega el número de
    # cuádruplo actual a la pila de saltos
    def middle_while_check(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.BOOL:
            sys.exit(str(self.lexer.lineno) + ': ' + 'Error semántico: El estatuto if requiere una expresión booleana')
        else:
            self.generate(QuadrupleRegister.GOTOF, operand, None, None)
            self.jump_stack.append(len(self.quadruple_list) - 1)

    # La función end_while_check saca un elemento de la pila de saltos y saca un punto
    # de retorno de la pila de saltos. Genera un cuádruplo GoTo con el punto de
    # retorno, que sería antes de ver la expresión del ciclo while y llama a la
    # función fill_quadruple para darle el número de cuádruplo actual al GoToF del
    # while que está después de la expresión.
    def end_while_check(self):
        false = self.jump_stack.pop()
        return_point = self.jump_stack.pop()
        self.generate(QuadrupleRegister.GOTO, None, None, return_point)
        self.fill_quadruple(false, len(self.quadruple_list))

    # La función begin_repeat_check primero saca un operando de la lista de operandos.
    # Si este operando no es entero, marca un error que requiere una expresion entera en
    # el ciclo repetir. Si si es entero, crea una nueva variable temporal entera y genera
    # un cuádruplo para asignar el valor del operando a esta nueva variable temporal.
    # Después mete a la lista de saltos el número de cuádruplo actual.
    # Llama al constant_handler para conseguir  una constante con el valor de 0 y la
    # agrega a la lista de constantes.
    # Crea otra variable temporal pero ahora una booleana y genera un cuádruplo que compara si
    # la expresión entera es mayor a cero y pone el resultado en la temporal booleana.
    # Genera un cuádruplo GoToF con la expresión booleana resultante.
    # Se mete el cuádruplo anterior a la pila de saltos señalando al GoToF
    # Después se llama al constant_handler para obtener una constante entera de 1, se
    # agrega al la lista de constantes. Se crea una nueva variable temporal entera y
    # se genera un cuádruplo que resta le resta 1 a la expresión entera del repear
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
            sys.exit(str(self.lexer.lineno) + ': ' + 'Error semántico: El estatuto if requiere una expresión booleana')

    # La función end_repeat_check saca de la pila de saltos primero el salto hacia el
    # cuadruplo de GoToF y después el punto de retorno hacia antes de la expresión.
    # Después genera un cuádruplo GoTo hacia el punto de retorno y llena el cuádruplo
    # del GoToF con el valor del cuádruplo actual
    def end_repeat_check(self):
        false = self.jump_stack.pop()
        return_point = self.jump_stack.pop()
        self.generate(QuadrupleRegister.GOTO, None, None, return_point)
        self.fill_quadruple(false, len(self.quadruple_list))

    # La función array_check saca una variable de la pila de operandos. Si esta
    # variable no tiene un límite superior marca error porque la variable no es
    # dimensionada. Si si tiene, se agrega un fondo falso a la pila de operadores
    # y regresa la variable.
    def array_check(self):
        variable = self.operand_stack.pop()
        if variable['upper_limit'] is None:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: La variable no es dimensionada')
            exit(1)
        else:
            self.push_fake_bottom()
            return variable

    # La función generate_return_statement recibe la variable de la función, saca un
    # operando de la pila de operandos (la expresión a retornar) y genera un cuádruplo
    # de asignación, donde a la función de la variable se le asigna el valor del operando.
    def generate_return_statement(self, function_variable):
        operand = self.operand_stack.pop()
        self.generate(OpCodes.ASSIGNMENT, operand, None, function_variable)
        self.generate_return_action()

    # La función generate_era recibe un nombre de función, y con este nombre, genera un
    # cuádruplo era con el mismo nombre de función
    def generate_era(self, function_name):
        self.generate(QuadrupleRegister.ERA, dict(name=function_name, address=function_name), None, None)

    # La función generate_return_action genera el cuádruplo de retorno que todas las funciones
    # tienen al final.
    def generate_return_action(self):
        self.generate(QuadrupleRegister.RET, None, None, None)

    # La función generate_gosub recibe un cuádruplo de inicio, y genera un cuádruplo
    # GoSub con este valor de inicio de función para mover la ejecución a ese
    # mismo cuádruplo
    def generate_gosub(self, start_quad):
        self.generate(QuadrupleRegister.GOSUB, dict(name=start_quad, address=start_quad), None, None)

    # La función verify_and_generate_argument recibe un argument, un contador de argumentos
    # y el número máximo de parámetros de la función. Si el número de argumento es mayor a
    # al número de parámetros máximo se manda un error porque el número de parámetros dados
    # es incorrecto. Después saca un operando de la pila de operandos. Si el tipo de este
    # operando es diferente del tipo del argumento, se manda un error. Si si son del mismo
    # tipo, se genera un cuádruplo param, para asignar el valor del operando al argumento
    # de la función.
    def verify_and_generate_argument(self, arg, arg_count, param_max):
        if(arg_count > param_max):
            sys.exit(str(self.lexer.lineno) + ': ' +" Error semántico: el número de parámetros dados es incorrecto")

        operand = self.operand_stack.pop()
        if operand['type'] != arg['type']:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(QuadrupleRegister.PARAM, operand, None, arg['address'])
            self.log.write("Argumento agregado: " + str(arg_count))

    # La función generate_array_access recibe una dirección base y un tamaño.
    # Se crea un índice viendo el último operando de la pila de operandos.
    # Se genera un cuádruplo Verify, con una base de 0, el tamaño que se recibió
    # y el índice obtenido.
    # Se saca el último operando de la pila de operandos, se inicializa un nuevo
    # pointer y se genera un cuádruplo de suma con el último operando, la dirección
    # base y el pointer creado.
    # Al final se saca el fondo falso del arreglo.
    def generate_array_access(self, base_address, size, array_type):
        index = self.operand_stack[-1]
        self.generate(OpCodes.VERIFY, 0, size, index)
        aux = self.operand_stack.pop()
        pointer = self.new_pointer(array_type)
        self.generate(OpCodes.SUM, aux, base_address, pointer)
        self.operand_stack.append(pointer)
        self.pop_fake_bottom()


    ######### FUNCIONES PRIMITIVAS ##############

    # Saca un operando de la pila de operandos y genera un cuádruplo read
    # para leer el input de teclado
    def generate_read(self):
        operand = self.operand_stack.pop()
        self.generate(OpCodes.READ, operand, None, None)

    # Saca el último operando de la pila de operandos y checa que el tipo sea string,
    # entero o flotante. Si si es, se genera el cuádruplo write que escribe en consola,
    # si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_write(self):
        operand = self.operand_stack.pop()
        if operand['type'] == SemanticCube.STRING or operand['type'] == SemanticCube.FLOAT or operand['type'] == SemanticCube.INT:
            self.generate(OpCodes.WRITE, operand, None, None)
        else:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)

    # Saca el último operando de la pila de operandos y checa que el tipo sea entero,
    # Si si es, se genera el cuádruplo forward que avanza hacia adelante el valor
    # del operando. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_forward(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.FORWARD, operand, None, None)

    # Saca el último operando de la pila de operandos y checa que el tipo sea entero,
    # Si si es, se genera el cuádruplo backward que avanza hacia atras el valor
    # del operando. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_backward(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.BACKWARD, operand, None, None)

    # Saca el último operando de la pila de operandos y checa que el tipo sea entero,
    # Si si es, se genera el cuádruplo right que mueve hacia la derecha con el valor
    # del operando. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_right(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.RIGHT, operand, None, None)

    # Saca el último operando de la pila de operandos y checa que el tipo sea entero,
    # Si si es, se genera el cuádruplo left que mueve hacia la izquierda con el valor
    # del operando. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_left(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.LEFT, operand, None, None)

    # Saca el último y penúltimo operando de la pila de operandos y checa que los tipos sean enteros,
    # Si si son, se genera el cuádruplo right que cambia a la posición con el valor
    # de los operandos. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_pos(self):
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.POS, operand_1, operand_2, None)

    # Saca el último operando de la pila de operandos y checa que el tipo sea entero,
    # Si si es, se genera el cuádruplo pos_x que cambia la posicion de x con el valor
    # del operando. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_pos_x(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.POS_X, operand, None, None)

    # Saca el último operando de la pila de operandos y checa que el tipo sea entero,
    # Si si es, se genera el cuádruplo pos_y que cambia la posicion de y con el valor
    # del operando. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_pos_y(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.POS_Y, operand, None, None)

    # Saca tres operandos de la pila de operandos y checa que los tipos sean enteros,
    # Si si son, se genera el cuádruplo line_color que cambia el color de la linea con el valor
    # de los operandos. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_line_color(self):
        operand_3 = self.operand_stack.pop()
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT or operand_3['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.LINE_COLOR, operand_1, operand_2, operand_3)

    # Saca el último operando de la pila de operandos y checa que el tipo sea entero,
    # Si si es, se genera el cuádruplo line_width que cambia el grosor de la linea con el valor
    # del operando. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_line_width(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.LINE_WIDTH, operand, None, None)

    # Genera el cuádruplo pen_up que alza la pluma para no dibujar
    def generate_pen_up(self):
        self.generate(OpCodes.PEN_UP, None, None, None)

    # Genera el cuádruplo pen_up que baja la pluma para dibujar
    def generate_pen_down(self):
        self.generate(OpCodes.PEN_DOWN, None, None, None)

    # Genera el cuádruplo fill_true que hace que haya un relleno en el dibujo
    def generate_fill_true(self):
        self.generate(OpCodes.FILL_TRUE, None, None, None)

    # Genera el cuádruplo fill_true que hace que no haya un relleno en el dibujo
    def generate_fill_false(self):
        self.generate(OpCodes.FILL_FALSE, None, None, None)

    # Saca tres operandos de la pila de operandos y checa que los tipos sean enteros,
    # Si si son, se genera el cuádruplo fill_color que cambia el color de relleno con el valor
    # de los operandos. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_fill_color(self):
        operand_3 = self.operand_stack.pop()
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT or operand_3['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.FILL_COLOR, operand_1, operand_2, operand_3)

    # Saca tres operandos de la pila de operandos y checa que los tipos sean enteros,
    # Si si son, se genera el cuádruplo background_color que cambia el color del fondo con el valor
    # de los operandos. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_background_color(self):
        operand_3 = self.operand_stack.pop()
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT or operand_3['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.BACKGROUND_COLOR, operand_1, operand_2, operand_3)

    # Genera el cuádruplo save_pos que guarda la posicion
    def generate_save_position(self):
        self.generate(OpCodes.SAVE_POS, None, None, None)

    # Genera el cuádruplo save_pos que restaura una posicion guardada
    def generate_restore_position(self):
        self.generate(OpCodes.RESTORE_POS, None, None, None)

    # Saca el último operando de la pila de operandos y checa que el tipo sea entero,
    # Si si es, se genera el cuádruplo random que genera un número random
    # Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_random(self):
        operand = self.operand_stack.pop()
        if operand['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            var = self.__new_temp_var(SemanticCube.INT)
            self.generate(OpCodes.RANDOM, operand, None, var)


    # Saca el último y penúltimo operando de la pila de operandos y checa que los tipos sean enteros,
    # Si si son, se genera el cuádruplo circle que dibuja un círculo con el radio y ángulo dado
    # por los operandos. Si no manda un error diciendo que el tipo de argumento no coincide.
    def generate_circle(self):
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        if operand_1['type'] != SemanticCube.INT or operand_2['type'] != SemanticCube.INT:
            print(str(self.lexer.lineno) + ': ' + 'Error semántico: El tipo de argumento no coincide')
            exit(1)
        else:
            self.generate(OpCodes.CIRCLE, operand_1, operand_2, None)

    # La función generate genera un cuádruplo con el operador, operando 1, operando 2 y
    # resultado dados como argumentos. Se guarda ese cuádruplo en la lista de cuádruplos
    def generate(self, operator, operand_1, operand_2, result):
        quadruple = dict(operator = operator, operand_1 = operand_1, operand_2 = operand_2, result = result)
        self.quadruple_list.append(quadruple)

    # La función fill_quadruple recibe un índice y un contenido como argumentos.
    # Guarda el contenido dado en el cuádruplo del índice
    def fill_quadruple(self, index, content):
        quadruple = self.quadruple_list[index]
        quadruple['result'] = content

    # la función get_next_quadruple regresa el número de cuádruplo actual
    def get_next_quadruple(self):
        return len(self.quadruple_list)

    # la función print_debug_quadruples imprime todos los cuádruplos
    def print_debug_quadruples(self):
        counter = 0
        for quadruple in self.quadruple_list:
            self.log.write('* Quadruple ' + str(counter))
            self.log.write(' Operator: ' + str(quadruple['operator']) +
                ' Operand1: ' + str(quadruple['operand_1']) +
                ' Operand2: ' + str(quadruple['operand_2']) +
                ' Result: ' + str(quadruple['result']))
            counter = counter + 1
    # la función print_constants imprime los nombres y direcciones de todas las constantes
    def print_constants(self):
        for constant in self.constant_list:
            address = constant['address']
            value = constant['name']
            self.log.write(str(address) + ' ' + str(value))

    # la función print_quadruples imprime las direcciones o nombres de los cuádruplos
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
            if isinstance(operand_2, dict):
                operand_2 = operand_2['name']
            if isinstance(result, dict):
                result = result['address']
            self.log.write('*Quadruple ' + str(counter) + ':   ' + str(operator) + ' ' + str(operand_1) + ' ' + str(operand_2) + ' ' + str(result))
            counter = counter + 1

    # la función print_name_quadruples imprime los nombres de todos los cuádruplos
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
            if isinstance(operand_2, dict):
                operand_2 = operand_2['name']
            if isinstance(result, dict):
                result = result['name']
            self.log.write('*Quadruple ' + str(counter) + ':   ' + str(operator) + ' ' + str(operand_1) + ' ' + str(operand_2) + ' ' + str(result))
            counter = counter + 1

    # La función new pointer crea un diccionario con el nombre, tipo y dirección del
    # nuevo pointer y lo regresa.
    def new_pointer(self, var_type):
        var = dict(name = 'ptr' + str(self.address_handler.pointer_count), type = var_type,
                   address = self.address_handler.next_pointer_address())
        return var

    # La función __new_temp_var recibe un tipo de variable, y con este tipo decide
    # que variable temporal crear. El contador de temporales se incrementa en 1 y se
    # agrega esta variable temporal a la pila de operandos. Al final se regresa la
    # variable temporal
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
            print(str(self.lexer.lineno) + ': ' + 'Error: Tipo ' + str(var_type) + ' desconocido')
            exit(2)
            return None

        self.temp_count += 1
        self.operand_stack.append(var)
        return var

    # La función __arithmetic_check recibe un operador, saca dos operandos de la pila de operandos
    # Y checa su tipo de resultado. Si el tipo de resultado es nulo, marca un error por
    # error de operacion entre operandos. Si no es nulo, se genera un cuádruplo con el operador
    # y operandos obtenidos, y como resultado se llama a la función para crear una nueva
    # variable temporal
    def __arithmetic_check(self, operator):
        operand_2 = self.operand_stack.pop()
        operand_1 = self.operand_stack.pop()
        result_type = self.semantic_cube.get_result_type(operand_1['type'], operand_2['type'], operator)
        self.log.write('Result Type :::::::::::::::::: ' + str(result_type) + ' ' + str(operand_1)+ ' ' + str(operand_2))
        if result_type is not None:
            self.generate(operator, operand_1, operand_2, self.__new_temp_var(result_type))
        else:
            print(str(self.lexer.lineno) + ': ' + 'Error: Operación entre tipos incompatibles')
            exit(0)

    # La función __to_opcode recibe un operador como string, y con esto regresa
    # su codigo de operador entero.
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
            print (str(self.lexer.lineno) + ': ' + 'Error: operador desconocido ' + operator_s)
            exit(1)
            return None
