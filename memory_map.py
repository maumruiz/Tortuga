from memory import Memory
from constant_table import ConstantTable

class MemoryMap:
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

    def __init__(self, constant_table, functions):
        print(" ////////////////////////   Memory Map init ////////////////////")
        global_variables = []
        for function in functions:
            if(function['name'] == "main"):
                global_variables = function["variables"]

        self.functions_table = functions
        self.memory_stack = []
        self.global_memory = Memory(True, global_variables)
        self.memory_stack.append(self.global_memory)
        self.constant_table = constant_table
        self.nested_call_level = 0

        print( "=============== functions dir ==================")
        print(self.functions_table)
        print( "=============== global memory ==================")
        print(self.global_memory.register)
        print(self.global_memory.temp_register)
        print( "=============== constant memory ==================")
        print(self.constant_table.table)

    def push_local(self, function_name):
        for function in self.functions_table:
            if(function['name'] == function_name):
                new_local_variables = function['variables']
        local_memory = Memory(False, new_local_variables)
        self.memory_stack.append(local_memory)

    def pop_local(self):
        self.memory_stack.pop()

    def get_value(self, address):
        if self.nested_call_level <= 0:
            if address >= MemoryMap.INT_BASE and address < MemoryMap.LOCAL_INT_BASE:
                return self.get_global_value(address)
            elif address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.TEMP_INT_BASE:
                return self.get_local_value(address)
            elif address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.POINTER_BASE:
                return self.get_temp_value(address)
            elif address >= MemoryMap.INT_CONSTANT_BASE and address < MemoryMap.INT_BASE:
                return self.get_constant_value(address)
            elif address == MemoryMap.FALSE_CONSTANT:
                return False
            elif address == MemoryMap.TRUE_CONSTANT:
                return True
            else:
                print('Error de ejecucion: Direccion virtual desconocida')
                exit(1)
                return None
        else:
            return self.get_param_value(address)

    def set_value(self, address, value):
        if address >= MemoryMap.INT_BASE and address < MemoryMap.LOCAL_INT_BASE:
            return self.set_global_value(address, value)
        elif address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.TEMP_INT_BASE:
            return self.set_local_value(address, value)
        elif address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.POINTER_BASE:
            return self.set_temp_value(address, value)
        elif address >= MemoryMap.INT_CONSTANT_BASE and address < MemoryMap.INT_BASE:
            print('Error de ejecucion: Direccion virtual desconocida')
            return None
        elif address == MemoryMap.FALSE_CONSTANT:
            print('Error de ejecucion: Direccion virtual desconocida')
            return None
        elif address == MemoryMap.TRUE_CONSTANT:
            print('Error de ejecucion: Direccion virtual desconocida')
            return None
        else:
            print('Error de ejecucion: Direccion virtual desconocida')
            return None

    def get_global_value(self, address):
        if address >= MemoryMap.INT_BASE and address < MemoryMap.FLOAT_BASE:
            return self.global_memory.get_int_value(address)
        elif address >= MemoryMap.FLOAT_BASE and address < MemoryMap.STRING_BASE:
            return self.global_memory.get_float_value(address)
        elif address >= MemoryMap.STRING_BASE and address < MemoryMap.BOOL_BASE:
            return self.global_memory.get_string_value(address)
        elif address >= MemoryMap.BOOL_BASE and address < MemoryMap.LOCAL_INT_BASE:
            return self.global_memory.get_bool_value(address)
        else:
            print('Error de ejecucion: Direccion virtual global desconocida')
            return None

    def get_local_value(self, address):
        if address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.LOCAL_FLOAT_BASE:
            return self.get_local_memory().get_int_value(address)
        elif address >= MemoryMap.LOCAL_FLOAT_BASE and address < MemoryMap.LOCAL_STRING_BASE:
            return self.get_local_memory().get_float_value(address)
        elif address >= MemoryMap.LOCAL_STRING_BASE and address < MemoryMap.LOCAL_BOOL_BASE:
            return self.get_local_memory().get_string_value(address)
        elif address >= MemoryMap.LOCAL_BOOL_BASE and address < MemoryMap.TEMP_INT_BASE:
            return self.get_local_memory().get_bool_value(address)
        else:
            print('Error de ejecucion: Direccion virtual local desconocida')
            return None

    def get_temp_value(self, address):
        if address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.TEMP_FLOAT_BASE:
            return self.get_local_memory().get_temp_int_value(address)
        elif address >= MemoryMap.TEMP_FLOAT_BASE and address < MemoryMap.TEMP_STRING_BASE:
            return self.get_local_memory().get_temp_float_value(address)
        elif address >= MemoryMap.TEMP_STRING_BASE and address < MemoryMap.TEMP_BOOL_BASE:
            return self.get_local_memory().get_temp_string_value(address)
        elif address >= MemoryMap.TEMP_BOOL_BASE and address < MemoryMap.POINTER_BASE:
            return self.get_local_memory().get_temp_bool_value(address)
        else:
            print('Error de ejecucion: Direccion virtual temporal desconocida')
            return None

    def get_constant_value(self, address):
        if address >= MemoryMap.INT_CONSTANT_BASE and address < MemoryMap.FLOAT_CONSTANT_BASE:
            return self.constant_table.get_int_value(address)
        elif address >= MemoryMap.FLOAT_CONSTANT_BASE and address < MemoryMap.STRING_CONSTANT_BASE:
            return self.constant_table.get_float_value(address)
        elif address >= MemoryMap.STRING_CONSTANT_BASE and address < MemoryMap.INT_BASE:
            return self.constant_table.get_string_value(address)
        else:
            print('Error de ejecucion: Direccion virtual constante desconocida')
            return None

    def set_global_value(self, address, value):
        if address >= MemoryMap.INT_BASE and address < MemoryMap.FLOAT_BASE:
            return self.global_memory.set_int_value(address, value)
        elif address >= MemoryMap.FLOAT_BASE and address < MemoryMap.STRING_BASE:
            return self.global_memory.set_float_value(address, value)
        elif address >= MemoryMap.STRING_BASE and address < MemoryMap.BOOL_BASE:
            return self.global_memory.set_string_value(address, value)
        elif address >= MemoryMap.BOOL_BASE and address < MemoryMap.LOCAL_INT_BASE:
            return self.global_memory.set_bool_value(address, value)
        else:
            print('Error de ejecucion: Direccion virtual global desconocida')
            return None

    def set_local_value(self, address, value):
        if address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.LOCAL_FLOAT_BASE:
            return self.get_local_memory().set_int_value(address, value)
        elif address >= MemoryMap.LOCAL_FLOAT_BASE and address < MemoryMap.LOCAL_STRING_BASE:
            return self.get_local_memory().set_float_value(address, value)
        elif address >= MemoryMap.LOCAL_STRING_BASE and address < MemoryMap.LOCAL_BOOL_BASE:
            return self.get_local_memory().set_string_value(address, value)
        elif address >= MemoryMap.LOCAL_BOOL_BASE and address < MemoryMap.TEMP_INT_BASE:
            return self.get_local_memory().set_bool_value(address, value)
        else:
            print('Error de ejecucion: Direccion virtual local desconocida')
            return None

    def set_temp_value(self, address, value):
        if address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.TEMP_FLOAT_BASE:
            return self.get_local_memory().set_temp_int_value(address, value)
        elif address >= MemoryMap.TEMP_FLOAT_BASE and address < MemoryMap.TEMP_STRING_BASE:
            return self.get_local_memory().set_temp_float_value(address, value)
        elif address >= MemoryMap.TEMP_STRING_BASE and address < MemoryMap.TEMP_BOOL_BASE:
            return self.get_local_memory().set_temp_string_value(address, value)
        elif address >= MemoryMap.TEMP_BOOL_BASE and address < MemoryMap.POINTER_BASE:
            return self.get_local_memory().set_temp_bool_value(address, value)
        else:
            print('Error de ejecucion: Direccion virtual temporal desconocida')
            return None

    def get_param_value(self, address):
        if address < MemoryMap.INT_BASE:
            return self.get_constant_value(address)
        elif address >= MemoryMap.INT_BASE and address < MemoryMap.LOCAL_INT_BASE:
            return self.get_global_value(address)
        elif address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.LOCAL_FLOAT_BASE:
            return self.get_previous_memory().get_int_value(address)
        elif address >= MemoryMap.LOCAL_FLOAT_BASE and address < MemoryMap.LOCAL_STRING_BASE:
            return self.get_previous_memory().get_float_value(address)
        elif address >= MemoryMap.LOCAL_STRING_BASE and address < MemoryMap.LOCAL_BOOL_BASE:
            return self.get_previous_memory().get_string_value(address)
        elif address >= MemoryMap.LOCAL_BOOL_BASE and address < MemoryMap.TEMP_INT_BASE:
            return self.get_previous_memory().get_bool_value(address)
        elif address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.POINTER_BASE:
            return self.get_temp_value(address)
        else:
            print('Error de ejecucion: Direccion virtual local desconocida')
            return None

    def get_local_memory(self):
        return self.memory_stack[-1]

    def get_previous_memory(self):
        return self.memory_stack[-2]

    def read_by_type(self, address):
        if address >= MemoryMap.INT_BASE and address < MemoryMap.FLOAT_BASE:
            return self.read_int()
        elif address >= MemoryMap.FLOAT_BASE and address < MemoryMap.STRING_BASE:
            return self.read_float()
        elif address >= MemoryMap.STRING_BASE and address < MemoryMap.BOOL_BASE:
            return self.read_string()
        elif address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.LOCAL_FLOAT_BASE:
            return self.read_int()
        elif address >= MemoryMap.LOCAL_FLOAT_BASE and address < MemoryMap.LOCAL_STRING_BASE:
            return self.read_float()
        elif address >= MemoryMap.LOCAL_STRING_BASE and address < MemoryMap.LOCAL_BOOL_BASE:
            return self.read_string()
        elif address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.TEMP_FLOAT_BASE:
            return self.read_int()
        elif address >= MemoryMap.TEMP_FLOAT_BASE and address < MemoryMap.TEMP_STRING_BASE:
            return self.read_float()
        elif address >= MemoryMap.TEMP_STRING_BASE and address < MemoryMap.TEMP_BOOL_BASE:
            return self.read_string()
        else:
            print('Error de ejecucion: Direccion virtual temporal desconocida o invalida')
            return None

    def read_int(self):
        return int(input())

    def read_float(self):
        return float(input())

    def read_string(self):
        return input()
