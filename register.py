class Register:
    INT = 0
    FLOAT = 1
    STRING = 2
    BOOL = 3

    def __init__(self):
        self.current_scope = 0
        self.function_list = []
        self.address_handler = None

    def set_address_handler(self, address_handler):
        self.address_handler = address_handler

    def create(self, program_name):
        global_scope = dict(name = program_name, type = 'void', variables = [])
        self.function_list.append(global_scope)
        print("Se crea el Directorio de Funciones. Nombre: " + program_name + " Tipo: programa")

    def add_function(self, function_name):
        if (self.__function_exists(function_name)):
            print('Duplicate function name')
            exit(1)
            return None

        function = dict(name = function_name, type = None, variables = [])
        self.function_list.append(function)
        self.current_scope = len(self.function_list) - 1
        print("Nueva funcion -- ID: " + function_name + " Scope -- " + str(self.current_scope))

    def add_function_param(self, param_name, param_type):
        param = dict(name = param_name, type = param_type)
        self.function_list[self.current_scope]['variables'].append(param)
        self.function_list[self.current_scope]['params'].append(param)
        print("Parametro de funcion: " + param_name)

    def add_function_return_type(self, return_type):
        self.function_list[self.current_scope]['type'] = return_type
        print("Tipo de la funcion: " + return_type)

    def add_variable(self, variable_name, variable_type, variable_value = None, scope = None):
        if (self.__variable_exists(variable_name)):
            print('Duplicate variable name')
            exit(1)
            return None

        # Si no se le pasa un scope asume que es el scope actual
        if scope is None:
            scope = self.current_scope
        type_code = self.__type_to_int(variable_type)
        variable = dict(name = variable_name, type = type_code, address = self.address_handler.next_variable_address(type_code, scope))
        self.function_list[scope]['variables'].append(variable)
        print("Nueva variable-- ID: " + variable_name + ", Tipo: " + variable_type + ", Scope actual: " + str(scope))

    def clear_variables(self):
        self.function_list[self.current_scope]['variables'] = []
        print("Destruye las variables del scope:  " + str(self.current_scope) + "    Tabla actual: Global")
        self.current_scope = 0

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
        self.function_list[self.current_scope]['starting_quadruple'] = quadruple

    def print_table(self):
        print(self.function_list)

    def __variable_exists(self, var_name):
        return self.__is_in_scope(0, var_name) and self.__is_in_scope(self.current_scope, var_name)

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
        if type_s == 'int':
            return Register.INT
        elif type_s == 'float':
            return Register.FLOAT
        elif type_s == 'string':
            return Register.STRING
        elif type_s == 'bool':
            return Register.BOOL
        else:
            print ('Error: unknown type')
            exit(1)
            return None
