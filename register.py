from logger import Logger

class Register:
    ''' Clase que se encarga del registro de funciones y variables, esta clase contiene
        la lista de funciones, el address habdler, el scope actual de funciones y la
        llamada de la funcion actual.'''

    INT = 0
    FLOAT = 1
    STRING = 2
    BOOL = 3

    # Init de la clase Register. Inicializa la lista de funciones como vacía y
    # las variables en 0
    def __init__(self):
        self.current_scope = 0
        self.function_list = []
        self.address_handler = None
        self.params_counter = 0
        self.current_function_call = 0
        self.main_goto_quadruple = 0
        self.add_param_counter = 0
        self.log = Logger(False)

    # Función que recibe un objeto de la clase address_handler y se la asigna al
    # address_handler handler de la clase register
    def set_address_handler(self, address_handler):
        self.address_handler = address_handler

    # La función create recibe el nombre del programa y crea el directorio de función
    # para el scope global con el nomre de 'main', tipo 'void' y variables vacías
    # este scope global se agrega a la lista de funciones
    def create(self, program_name):
        global_scope = dict(name = program_name, type = 'void', variables = [])
        self.function_list.append(global_scope)
        self.log.write("Se crea el Directorio de Funciones. Nombre: " + program_name + " Tipo: programa")

    # La función add_function_param recibe el nombre de una función. Checa si el
    # nombre de la función ya existe. Si ya existe marca un error de semántica.
    # Si no existe crea un diccionario con los tamaños de variables inicializados en 0,
    # un diccionario de funcion con el nombre (nombre de la funcion), tipo(None por ahora),
    # size(el tamaño de variables creado anteriormente), indice cuádruplo de inicio (None),
    # lista de variables(vacia), lista de parametros(vacia), tamaño de parametros y el
    # registro de retorno
    # Después se agrega este diccionario a la lista de funciones y se actualiza el
    # scope actual con el scope de la nueva funcion
    def add_function(self, function_name):
        if (self.__function_exists(function_name)):
            print(str(self.lexer.lineno) + ': ' + 'Error de semántica: Nombre de funcion ' + function_name + ' duplicado')
            exit(1)
            return None

        size_dict = dict(int=0, float=0, string=0, bool=0, int_temp=0, float_temp=0, string_temp=0, bool_temp=0)
        function = dict(name = function_name, type = None, size = size_dict, start_dir = None, variables = [], params = [], param_size = 0, return_register = None)
        self.function_list.append(function)
        self.current_scope = len(self.function_list) - 1
        self.log.write("Nueva funcion -- ID: " + function_name + " Scope -- " + str(self.current_scope))

    # La función add_function_param recibe el nombre de parámetro y el tipo de parámetro.
    # Se consigue el codigo entero del tipo con la funcion __type_to_int, se localiza
    # el scope actual y se crea un diccionario de parametro con el nombre, tipo y dirección
    # (creada con el address_handler).
    # Este parametro se agrega a la lista de variables de la función, se agrega al diccionario
    # el número de parámetro y se agrega el parametro a la lista de parámetros de la función.
    # Se actualiza el tamaño de los parámetros
    def add_function_param(self, param_name, param_type):
        type_code = self.__type_to_int(param_type)
        scope = self.current_scope
        param = dict(name = param_name, type = type_code, address = self.address_handler.next_variable_address(type_code, scope))
        self.function_list[self.current_scope]['variables'].append(param)
        param['param_num'] = self.add_param_counter
        self.function_list[self.current_scope]['params'].append(param)
        self.function_list[self.current_scope]['param_size'] = self.add_param_counter
        self.log.write("Parametro de funcion: " + param_name)

    # La función set_function_start_dir recibe un cuádruplo y se lo asigna
    # a la dirección de inicio de la función con el scope actual
    def set_function_start_dir(self, quadruple):
        self.function_list[self.current_scope]['start_dir'] = quadruple

    # La función add_function_return_type recibe un tipo de retorno. Si el tipo de
    # retorno no es void, se asigna el tipo de retorno al tipo de función con el
    # scope actual. Se agrega una variable con el nombre de la función y se asigna su dirección
    # al return register de la función con el scope actual
    def add_function_return_type(self, return_type):
        if return_type != 'void':
            type_code = self.__type_to_int(return_type)
            self.function_list[self.current_scope]['type'] = type_code
            function_address = self.add_variable(self.function_list[self.current_scope]['name'], type_code, None, 0)['address']
            self.function_list[self.current_scope]['return_register'] = function_address
        self.log.write("Tipo de la funcion: " + return_type)

    # La función add variable recibe un nombre, un tipo, un valor y un scope.
    # Checa si el nombre de la variable existe. Si ya existe se manda un error de
    # semántica. Si no existe crea una variable nueva con el nombre y tipo dados,
    # y una dirección creada por el address_handler.
    # Esta variable se agrega a la lista de variables de la funcion con scope actual
    def add_variable(self, variable_name, variable_type, variable_value = None, scope = None):
        if (self.__variable_exists(variable_name)):
            print(str(self.lexer.lineno) + ': ' + 'Error de semántica: Nombre de variable ' + variable_name + ' duplicado')
            exit(1)
            return None

        # Si no se le pasa un scope asume que es el scope actual
        if scope is None:
            scope = self.current_scope
        type_code = self.__type_to_int(variable_type)
        variable = dict(name = variable_name, type = type_code, address = self.address_handler.next_variable_address(type_code, scope), upper_limit = None)
        self.function_list[scope]['variables'].append(variable)
        self.log.write("Nueva variable-- ID: " + variable_name + ", Tipo: " + str(variable_type) + ", Scope actual: " + str(scope))
        return variable

    # La función clear variables le asigna a la funcion actual el diccionario de tamaño de
    # variables. Se regresa el scope al global y se reinicia el add_param_counter con 0
    def clear_variables(self):
        #self.function_list[self.current_scope]['variables'] = []
        self.function_list[self.current_scope]['size_dict'] = self.address_handler.return_size_dict()
        
        self.log.write('############## SIZE DICT #####################')
        self.log.write(self.function_list[self.current_scope]['size_dict'])
        self.log.write("Destruye las variables del scope:  " + str(self.current_scope) + "    Tabla actual: Global")
        
        self.current_scope = 0
        self.add_param_counter = 0

    # La función get_variable regresa el dict con los datos de la variable basada en su nombre
    def get_variable(self, variable_name):
        for variable in self.function_list[self.current_scope]['variables']:
            if variable['name'] == variable_name:
                return variable
        for variable in self.function_list[0]['variables']:
            if variable['name'] == variable_name:
                return variable
        return None

    # La función set_starting_quadruple le asigna la dirección de cuádruplo de
    # inicio de la función.
    def set_starting_quadruple(self, quadruple):
        self.function_list[self.current_scope]['start_dir'] = quadruple

    # La función get_function_starting_quadruple regresa la dirección de cuádruplo
    # de inicio de la función
    def get_function_starting_quadruple(self):
        return self.function_list[self.current_function_call]['start_dir']

    # La función set_current_function_call recibe un nombre de función
    # y busca el índice de esa función para asignarle ese indice al
    # function call actual
    def set_current_function_call(self, function_name):
        for index, function in enumerate(self.function_list):
            if function_name == function['name']:
                self.current_function_call = index
                self.log.write("Current function index: " + str(index))
                return index
        self.log.write(str(self.lexer.lineno) + ': ' + "Error: Funcion no declarada: " + function_name)
        exit(1)

    # La función get_expected_arg_type busca en la función con function call
    # actual, el número de parámetro de la lista de parámetros. Regresa
    # todo el parametro.
    def get_expected_arg_type(self):
        for arg in self.function_list[self.current_function_call]['params']:
            if(int(arg['param_num']) == int(self.params_counter)):
                return arg
        return None

    # La función get_param_max regresa el tamaño de parámetros de la función
    # con el function call actual
    def get_param_max(self):
        return self.function_list[self.current_function_call]['param_size']

    # La función get_current_function regresa la función con el function call actual
    def get_current_function(self):
        return self.function_list[self.current_function_call]

    # La función verify_params_count busca la cantidad de parámetros de la función.
    # Si el número obtenido es diferente al contador de parámetros actual marca
    # error por número de parámetros incorrecto
    def verify_params_count(self):
        expected_count = len(self.function_list[self.current_function_call]['params'])
        if self.params_counter != expected_count:
            print(str(self.lexer.lineno) + ': ' + "Error: El numero de los parametros es incorrecto")
            exit(1)

    # La función create_array recobe el nombre de una variable y el tamaño.
    # Busca el nombre de la variable en la lista de variables de la función actual
    # y le asigna a su limite superior el tamaño recibido como argumento
    def create_array(self, variable_name, size):
        for variable in self.function_list[self.current_scope]['variables']:
            if variable['name'] == variable_name:
                variable['upper_limit'] = size


    # Imprime la tabla de funciones
    def print_table(self):
        self.log.write(self.function_list)

    # La función __variable_exists recibe un nombre de variable y revisa si
    # el nombre existe en el scope actual y global, o en el scope actual
    def __variable_exists(self, var_name):
        return self.__is_in_scope(0, var_name) and self.__is_in_scope(self.current_scope, var_name) or self.__is_in_scope(self.current_scope, var_name)

    # La función revisa si un nombre de variable ya existe en el scope dado,
    # checando la lista de variables de la función
    def __is_in_scope(self, scope, var_name):
        for variable in self.function_list[scope]['variables']:
            if variable['name'] == var_name:
                return True
        return False

    # La función __function_exists recibe el nombre de la función y revisa la lista
    # de funciones para verficar si existe ya ese nombre de función.
    def __function_exists(self, function_name):
        for function in self.function_list:
            if function['name'] == function_name:
                return True
        return False

    # La función __type_to_int recibe un string de tipo y lo convierte a su
    # código entero.
    def __type_to_int(self, type_s):
        if isinstance(type_s, int):
            return type_s
        elif type_s == 'int':
            return Register.INT
        elif type_s == 'float':
            return Register.FLOAT
        elif type_s == 'string':
            return Register.STRING
        elif type_s == 'bool':
            return Register.BOOL
        else:
            print (str(self.lexer.lineno) + ': ' + 'Error: Tipo de dato ' + type_s + ' desconocido')
            exit(1)
            return None
