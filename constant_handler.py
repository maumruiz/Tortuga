from semantic_cube import SemanticCube
from virtual_address_handler import VirtualAddressHandler
import sys

class ConstantHandler:
    """# Clase que maneja una lista de constantes, y las genera con su nombre, tipo y dirección,
       # para poder usarlas en los operandos y cuádruplos correspondientes            """

    #Inicializa el ConstantHandler con una clase de address_handler y listas vacias de
    # constantes enteras, flotantes, strings y bools, las constantes booleanas siempre van a ser
    # verdadero y falso
    def __init__(self, address_handler):
        self.address_handler = address_handler
        self.int_constants_list = []
        self.float_constants_list = []
        self.string_constants_list = []
        self.bool_constants_list = []
        self.__init_bool_constants()

    # Inicializa las constantes booleanas de verdadero y falso y las arega a la lista de constantes booleanas
    def __init_bool_constants(self):
        false_constant = dict(name = 'falso', type = SemanticCube.BOOL, address = self.address_handler.FALSE_CONSTANT)
        true_constant = dict(name = 'verdadero', type = SemanticCube.BOOL, address = self.address_handler.TRUE_CONSTANT)
        self.bool_constants_list.append(false_constant)
        self.bool_constants_list.append(true_constant)

    # Regresa la constante booleana que se está asignando con nombre, tipo y direccion
    def assign_boolean_constant(self, constant):
        if constant == 'verdadero':
            return self.bool_constants_list[-1]
        elif constant == 'falso':
            return self.bool_constants_list[0]
        else:
            print('Constante booleana desconocida')
            exit(1)
            return None

    # Si se pasa una constante entera que ya existe, se regresa esa constante,
    # si no, se crea una nueva constante con nombre, tipo y dirección, se
    # agrega a la lista de constantes enteras y regresa la constante
    def find_or_init_int_constant(self, int_constant):
        for constant in self.int_constants_list:
            if constant['name'] == int_constant:
                return constant

        new_constant = dict(name = int_constant,
                            type = SemanticCube.INT,
                            address = self.address_handler.next_int_constant_address())
        self.int_constants_list.append(new_constant)
        return new_constant

    # Si se pasa una constante flotante que ya existe, se regresa esa constante,
    # si no, se crea una nueva constante con nombre, tipo y dirección, se
    # agrega a la lista de constantes flotantes y regresa la constante
    def find_or_init_float_constant(self, float_constant):
        for constant in self.float_constants_list:
            if constant['name'] == float_constant:
                return constant

        new_constant = dict(name = float_constant,
                            type = SemanticCube.FLOAT,
                            address = self.address_handler.next_float_constant_address())
        self.float_constants_list.append(new_constant)
        return new_constant

    # Si se pasa una constante string que ya existe, se regresa esa constante,
    # si no, se crea una nueva constante con nombre, tipo y dirección, se
    # agrega a la lista de constantes string y regresa la constante
    def find_or_init_string_constant(self, string_constant):
        for constant in self.string_constants_list:
            if constant['name'] == string_constant:
                return constant

        new_constant = dict(name = string_constant,
                            type = SemanticCube.STRING,
                            address = self.address_handler.next_string_constant_address())
        self.string_constants_list.append(new_constant)
        return new_constant

    # Funcion que llama a la función que busca o inicializa una constante según
    # el tipo que se esté buscando
    def __find_or_init_constant(self, constant, constant_type):
        if constant_type == SemanticCube.BOOL:
            return self.__assign_boolean_constant(constant)
        elif constant_type == SemanticCube.INT:
            return self.__find_or_init_int_constant(constant)
        elif constant_type == SemanticCube.FLOAT:
            return self.__find_or_init_float_constant(constant)
        elif constant_type == SemanticCube.STRING:
            return self.__find_or_init_string_constant(constant)
        else:
            print('Constante desconocida')
            exit(1)
            return None
