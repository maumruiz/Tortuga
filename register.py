class Register:
    INT = 0
    FLOAT = 1
    STRING = 2
    BOOL = 3

    def __init__(self):
        self.current_scope = 0
        self.function_list = []
        self.address_handler = None
        self.params_counter = 0
        self.current_function_call = 0
        self.main_goto_quadruple = 0
        self.add_param_counter = 0

    def set_address_handler(self, address_handler):
        self.address_handler = address_handler

    def create(self, program_name):
        global_scope = dict(name = program_name, type = 'void', variables = [])
        self.function_list.append(global_scope)
        print("Se crea el Directorio de Funciones. Nombre: " + program_name + " Tipo: programa")

    def add_function(self, function_name):
        if (self.__function_exists(function_name)):
            print('Error de semántica: Nombre de funcion ' + function_name + ' duplicado')
            exit(1)
            return None

        size_dict = dict(int=0, float=0, string=0, bool=0, int_temp=0, float_temp=0, string_temp=0, bool_temp=0)
        function = dict(name = function_name, type = None, size = size_dict, start_dir = None, variables = [], params = [], param_size = 0, return_register = None)
        self.function_list.append(function)
        self.current_scope = len(self.function_list) - 1
        print("Nueva funcion -- ID: " + function_name + " Scope -- " + str(self.current_scope))

    def add_function_param(self, param_name, param_type):
        type_code = self.__type_to_int(param_type)
        scope = self.current_scope
        param = dict(name = param_name, type = type_code, address = self.address_handler.next_variable_address(type_code, scope))
        self.function_list[self.current_scope]['variables'].append(param)
        param['param_num'] = self.add_param_counter
        self.function_list[self.current_scope]['params'].append(param)
        self.function_list[self.current_scope]['param_size'] = self.add_param_counter
        print("Parametro de funcion: " + param_name)

    def set_function_start_dir(self, quadruple):
        self.function_list[self.current_scope]['start_dir'] = quadruple

    def add_function_return_type(self, return_type):
        if return_type != 'void':
            type_code = self.__type_to_int(return_type)
            self.function_list[self.current_scope]['type'] = type_code
            function_address = self.add_variable(self.function_list[self.current_scope]['name'], type_code, None, 0)['address']
            self.function_list[self.current_scope]['return_register'] = function_address
        print("Tipo de la funcion: " + return_type)

    def add_variable(self, variable_name, variable_type, variable_value = None, scope = None):
        if (self.__variable_exists(variable_name)):
            print('Error de semántica: Nombre de variable ' + variable_name + ' duplicado')
            exit(1)
            return None

        # Si no se le pasa un scope asume que es el scope actual
        if scope is None:
            scope = self.current_scope
        type_code = self.__type_to_int(variable_type)
        variable = dict(name = variable_name, type = type_code, address = self.address_handler.next_variable_address(type_code, scope), upper_limit = None)
        self.function_list[scope]['variables'].append(variable)
        print("Nueva variable-- ID: " + variable_name + ", Tipo: " + str(variable_type) + ", Scope actual: " + str(scope))
        return variable

    def clear_variables(self):
        #self.function_list[self.current_scope]['variables'] = []
        self.function_list[self.current_scope]['size_dict'] = self.address_handler.return_size_dict()
        print('############## SIZE DICT #####################')
        print(self.function_list[self.current_scope]['size_dict'])
        print("Destruye las variables del scope:  " + str(self.current_scope) + "    Tabla actual: Global")
        self.current_scope = 0
        self.add_param_counter = 0

    # Regresa el dict con los datos de la variable basada en su nombre
    def get_variable(self, variable_name):
        for variable in self.function_list[self.current_scope]['variables']:
            if variable['name'] == variable_name:
                return variable
        for variable in self.function_list[0]['variables']:
            if variable['name'] == variable_name:
                return variable
        return None

    def set_starting_quadruple(self, quadruple):
        self.function_list[self.current_scope]['start_dir'] = quadruple

    def get_function_starting_quadruple(self):
        return self.function_list[self.current_function_call]['start_dir']

    def set_current_function_call(self, function_name):
        for index, function in enumerate(self.function_list):
            if function_name == function['name']:
                self.current_function_call = index
                print("Current function index: " + str(index))
                return index
        print("Error: Funcion no declarada: " + function_name)
        print(self.function_list)
        exit(1)

    def get_expected_arg_type(self):
        for arg in self.function_list[self.current_function_call]['params']:
            if(int(arg['param_num']) == int(self.params_counter)):
                return arg
        return None

    def get_param_max(self):
        return self.function_list[self.current_function_call]['param_size']

    def get_current_function(self):
        return self.function_list[self.current_function_call]

    def verify_params_count(self):
        expected_count = len(self.function_list[self.current_function_call]['params'])
        if self.params_counter != expected_count:
            print(expected_count)
            print(self.params_counter)
            print("Error: El numero de los parametros es incorrecto")
            exit(1)

    def create_array(self, variable_name, size):
        for variable in self.function_list[self.current_scope]['variables']:
            if variable['name'] == variable_name:
                variable['upper_limit'] = size


    def print_table(self):
        print(self.function_list)

    def __variable_exists(self, var_name):
        return self.__is_in_scope(0, var_name) and self.__is_in_scope(self.current_scope, var_name) or self.__is_in_scope(self.current_scope, var_name)

    def __is_in_scope(self, scope, var_name):
        for variable in self.function_list[scope]['variables']:
            if variable['name'] == var_name:
                return True
        return False

    def __function_exists(self, function_name):
        for function in self.function_list:
            if function['name'] == function_name:
                return True
        return False

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
            print ('Error: Tipo de dato ' + type_s + ' desconocido')
            exit(1)
            return None
