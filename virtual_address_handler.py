from semantic_cube import SemanticCube
import sys

class VirtualAddressHandler:
    GLOBAL_SCOPE = 0

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

    def __init__(self):
        self.int_constant_count = 0
        self.float_constant_count = 0
        self.string_constant_count = 0
        self.int_count = 0
        self.float_count = 0
        self.bool_count = 0
        self.string_count = 0
        self.local_int_count = 0
        self.local_float_count = 0
        self.local_string_count = 0
        self.local_bool_count = 0
        self.temp_int_count = 0
        self.temp_float_count = 0
        self.temp_bool_count = 0
        self.temp_string_count = 0

    def reset_local_counters(self):
        self.local_int_count = 0
        self.local_float_count = 0
        self.local_string_count = 0
        self.local_bool_count = 0

    def reset_temp_counters(self):
        self.temp_int_count = 0
        self.temp_float_count = 0
        self.temp_bool_count = 0
        self.temp_string_count = 0

    def next_variable_address(self, variable_type, scope):
        if scope == self.GLOBAL_SCOPE:
            return self.next_global_variable_address(variable_type)
        else:
            return self.next_local_variable_address(variable_type)

    def next_global_variable_address(self, var_type):
        if var_type == SemanticCube.INT:
            return self.next_int_address()
        elif var_type == SemanticCube.FLOAT:
            return self.next_float_address()
        elif var_type == SemanticCube.STRING:
            return self.next_string_address()
        elif var_type == SemanticCube.BOOL:
            return self.next_bool_address()
        else:
            print('Error desconocido')
            exit(2)
            return None

    def next_local_variable_address(self, var_type):
        if var_type == SemanticCube.INT:
            return self.next_local_int_address()
        elif var_type == SemanticCube.FLOAT:
            return self.next_local_float_address()
        elif var_type == SemanticCube.STRING:
            return self.next_local_string_address()
        elif var_type == SemanticCube.BOOL:
            return self.next_local_bool_address()
        else:
            print('Error desconocido')
            exit(2)
            return None

    def next_temp_variable_address(self, var_type):
        if var_type == SemanticCube.INT:
            return self.next_temp_int_address()
        elif var_type == SemanticCube.FLOAT:
            return self.next_temp_float_address()
        elif var_type == SemanticCube.STRING:
            return self.next_temp_string_address()
        elif var_type == SemanticCube.BOOL:
            return self.next_temp_bool_address()
        else:
            print('Error desconocido')
            exit(2)
            return None

    def next_int_constant_address(self):
        address = VirtualAddressHandler.INT_CONSTANT_BASE + self.int_constant_count
        self.int_constant_count += 1
        return address

    def next_float_constant_address(self):
        address = VirtualAddressHandler.FLOAT_CONSTANT_BASE + self.float_constant_count
        self.float_count += 1
        return address

    def next_string_constant_address(self):
        address = VirtualAddressHandler.STRING_CONSTANT_BASE + self.string_constant_count
        self.string_constant_count += 1
        return address

    def next_int_address(self):
        address = VirtualAddressHandler.INT_BASE + self.int_count
        self.int_count += 1
        return address

    def next_float_address(self):
        address = VirtualAddressHandler.FLOAT_BASE + self.float_count
        self.float_count += 1
        return address

    def next_string_address(self):
        address = VirtualAddressHandler.STRING_BASE + self.string_count
        self.string_count += 1
        return address

    def next_bool_address(self):
        address = VirtualAddressHandler.BOOL_BASE + self.bool_count
        self.bool_count += 1
        return address

    def next_local_int_address(self):
        address = VirtualAddressHandler.LOCAL_INT_BASE + self.local_int_count
        self.local_int_count += 1
        return address

    def next_local_float_address(self):
        address = VirtualAddressHandler.LOCAL_FLOAT_BASE + self.local_float_count
        self.local_float_count += 1
        return address

    def next_local_string_address(self):
        address = VirtualAddressHandler.LOCAL_STRING_BASE + self.local_string_count
        self.local_string_count += 1
        return address

    def next_local_bool_address(self):
        address = VirtualAddressHandler.LOCAL_BOOL_BASE + self.local_bool_count
        self.local_bool_count += 1
        return address

    def next_temp_int_address(self):
        address = VirtualAddressHandler.TEMP_INT_BASE + self.temp_int_count
        self.temp_int_count += 1
        return address

    def next_temp_float_address(self):
        address = VirtualAddressHandler.TEMP_FLOAT_BASE + self.temp_float_count
        self.temp_float_count += 1
        return address

    def next_temp_string_address(self):
        address = VirtualAddressHandler.TEMP_STRING_BASE + self.temp_string_count
        self.temp_string_count += 1
        return address

    def next_temp_bool_address(self):
        address = VirtualAddressHandler.TEMP_BOOL_BASE + self.temp_bool_count
        self.temp_bool_count += 1
        return address
