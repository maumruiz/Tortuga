from semantic_cube import SemanticCube
from virtual_address_handler import VirtualAddressHandler
import sys

class ConstantHandler:
    """docstring for ConstantHandler"""
  
    def __init__(self, address_handler):
        self.address_handler = address_handler
        self.int_constants_list = []
        self.float_constants_list = []
        self.string_constants_list = []
        self.bool_constants_list = []
        self.__init_bool_constants()

    def __init_bool_constants(self):
        false_constant = dict(name = 'falso', type = SemanticCube.BOOL, address = self.address_handler.FALSE_CONSTANT)
        true_constant = dict(name = 'verdadero', type = SemanticCube.BOOL, address = self.address_handler.TRUE_CONSTANT)
        self.bool_constants_list.append(false_constant)
        self.bool_constants_list.append(true_constant)

    def assign_boolean_constant(self, constant):
        if constant == 'verdadero':
            return self.bool_constants_list[-1]
        elif constant == 'falso':
            return self.bool_constants_list[0]
        else:
            print('Constante booleana desconocida')
            exit(1)
            return None

    def find_or_init_int_constant(self, int_constant):
        for constant in self.int_constants_list:
            if constant == int_constant:
                return constant
        
        new_constant = dict(name = int_constant,
                            type = SemanticCube.INT,
                            address = self.address_handler.next_int_constant_address())
        self.int_constants_list.append(new_constant)
        return new_constant

    def find_or_init_float_constant(self, float_constant):
        for constant in self.float_constants_list:
            if constant == float_constant:
                return constant
        
        new_constant = dict(name = float_constant,
                            type = SemanticCube.FLOAT,
                            address = self.address_handler.next_float_constant_address())
        self.float_constants_list.append(new_constant)
        return new_constant

    def find_or_init_string_constant(self, string_constant):
        for constant in self.string_constants_list:
            if constant == string_constant:
                return constant
        
        new_constant = dict(name = string_constant,
                            type = SemanticCube.STRING,
                            address = self.address_handler.next_string_constant_address())
        self.string_constants_list.append(new_constant)
        return new_constant

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

