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

    POINTER_BASE = 40000

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
        self.pointer_count = 0

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

    def return_size_dict(self):
        size_dict = dict(int=self.local_int_count, float=self.local_float_count,
                         string=self.local_string_count, bool=self.local_bool_count,
                         int_temp=self.temp_int_count, float_temp=self.temp_float_count,
                         string_temp=self.temp_string_count, bool_temp=self.temp_bool_count)
        self.reset_local_counters()
        self.reset_temp_counters()
        return size_dict

    def return_global_size_dict(self):
        size_dict = dict(int=self.int_count, float=self.float_count,
                         string=self.string_count, bool=self.bool_count,
                         int_temp=self.temp_int_count, float_temp=self.temp_float_count,
                         string_temp=self.temp_string_count, bool_temp=self.temp_bool_count,
                         pointer=self.pointer_count)
        self.reset_temp_counters()
        return size_dict

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

    def next_pointer_address(self):
        address = VirtualAddressHandler.POINTER_BASE + self.pointer_count
        self.pointer_count += 1
        return address

    def increment_address_count(self, var_type, scope, count):
        if scope == 0:
            if var_type == SemanticCube.INT:
                self.increment_int_count(count)
            elif var_type == SemanticCube.FLOAT:
                self.increment_float_count(count)
            elif var_type == SemanticCube.STRING:
                self.increment_string_count(count)
            elif var_type == SemanticCube.BOOL:
                self.increment_bool_count(count)
        else:
            if var_type == SemanticCube.INT:
                self.increment_local_int_count(count)
            elif var_type == SemanticCube.FLOAT:
                self.increment_local_float_count(count)
            elif var_type == SemanticCube.STRING:
                self.increment_local_string_count(count)
            elif var_type == SemanticCube.BOOL:
                self.increment_local_bool_count(count)

    def increment_int_count(self, count):
        self.int_count += count

    def increment_float_count(self, count):
        self.float_count += count

    def increment_string_count(self, count):
        self.string_count += count

    def increment_bool_count(self, count):
        self.bool_count += count

    def increment_local_int_count(self, count):
        self.local_int_count += count

    def increment_local_float_count(self, count):
        self.local_float_count += count

    def increment_local_string_count(self, count):
        self.local_string_count += count

    def increment_local_bool_count(self, count):
        self.local_bool_count += count