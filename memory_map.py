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

    def __init__(self, constant_table):
        self.memory_stack = []
        self.global_memory = Memory(true)
        self.memory_stack.append(self.global_memory)
        self.constant_table = constant_table

    def get_value(self, address):
        if address >= MemoryMap.INT_BASE and address < MemoryMap.LOCAL_INT_BASE:
            return self.get_global_value(address)
        elif address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.TEMP_INT_BASE:
            return self.get_local_value(address)
        elif address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.POINTER_BASE:
            return self.get_temp_value(address)
        elif address >= MemoryMap.INT_CONSTANT_BASE and < MemoryMap.INT_BASE:
            return self.get_constant_value(address)
        elif address == MemoryMap.FALSE_CONSTANT:
            return False
        elif address == MemoryMap.TRUE_CONSTANT:
            return True
        else:
            print('Error de ejecución: Dirección virtual desconocida')
            return None

    def set_value(self, address, value):
        if address >= MemoryMap.INT_BASE and address < MemoryMap.LOCAL_INT_BASE:
            return self.set_global_value(address, value)
        elif address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.TEMP_INT_BASE:
            return self.set_local_value(address, value)
        elif address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.POINTER_BASE:
            return self.set_temp_value(address, value)
        elif address >= MemoryMap.INT_CONSTANT_BASE and < MemoryMap.INT_BASE:
            print('Error de ejecución: Dirección virtual no válida')
            return None
        elif address == MemoryMap.FALSE_CONSTANT:
            print('Error de ejecución: Dirección virtual no válida')
            return None
        elif address == MemoryMap.TRUE_CONSTANT:
            print('Error de ejecución: Dirección virtual no válida')
            return None
        else:
            print('Error de ejecución: Dirección virtual desconocida')
            return None

    def get_global_value(self, address):
        if address >= MemoryMap.INT_BASE and address < MemoryMap.FLOAT_BASE:
            return self.global_memory.get_int_value(address)
        elif address >= MemoryMap.FLOAT_BASE and address < MemoryMap.STRING_BASE:
            return self.global_memory.get_float_value(address)
        elif address >= MemoryMap.STRING_BASE and address < MemoryMap.BOOL_BASE:
            return self.global_memory.get_string_value(address)
        elif address >= MemoryMap.BOOL_BASE and < MemoryMap.LOCAL_INT_BASE:
            return self.global_memory.get_bool_value(address)
        else:
            print('Error de ejecución: Dirección virtual desconocida')
            return None

    def get_local_value(self, address):
        if address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.LOCAL_FLOAT_BASE:
            return self.get_local_memory().get_int_value(address)
        elif address >= MemoryMap.LOCAL_FLOAT_BASE and address < MemoryMap.LOCAL_STRING_BASE:
            return self.get_local_memory().get_float_value(address)
        elif address >= MemoryMap.LOCAL_STRING_BASE and address < MemoryMap.LOCAL_BOOL_BASE:
            return self.get_local_memory().get_string_value(address)
        elif address >= MemoryMap.LOCAL_BOOL_BASE and < MemoryMap.TEMP_INT_BASE:
            return self.get_local_memory().get_bool_value(address)
        else:
            print('Error de ejecución: Dirección virtual desconocida')
            return None

    def get_temp_value(self, address):
        if address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.TEMP_FLOAT_BASE:
            return self.get_local_memory().get_temp_int_value(address)
        elif address >= MemoryMap.TEMP_FLOAT_BASE and address < MemoryMap.TEMP_STRING_BASE:
            return self.get_local_memory().get_temp_float_value(address)
        elif address >= MemoryMap.TEMP_STRING_BASE and address < MemoryMap.TEMP_BOOL_BASE:
            return self.get_local_memory().get_temp_string_value(address)
        elif address >= MemoryMap.TEMP_BOOL_BASE and < MemoryMap.POINTER_BASE:
            return self.get_local_memory().get_temp_bool_value(address)
        else:
            print('Error de ejecución: Dirección virtual desconocida')
            return None

    def get_constant_value(self, address):
        if address >= MemoryMap.INT_CONSTANT_BASE and address < MemoryMap.FLOAT_CONSTANT_BASE:
            return self.constant_table.get_int_value(address)
        elif address >= MemoryMap.FLOAT_CONSTANT_BASE and address < MemoryMap.STRING_CONSTANT_BASE:
            return self.constant_table.get_float_value(address)
        elif address >= MemoryMap.STRING_CONSTANT_BASE and address < MemoryMap.INT_BASE:
            return self.constant_table.get_string_value(address)
        else:
            print('Error de ejecución: Dirección virtual desconocida')
            return None

    def set_global_value(self, address, value):
        if address >= MemoryMap.INT_BASE and address < MemoryMap.FLOAT_BASE:
            return self.global_memory.set_int_value(address, value)
        elif address >= MemoryMap.FLOAT_BASE and address < MemoryMap.STRING_BASE:
            return self.global_memory.set_float_value(address, value)
        elif address >= MemoryMap.STRING_BASE and address < MemoryMap.BOOL_BASE:
            return self.global_memory.set_string_value(address, value)
        elif address >= MemoryMap.BOOL_BASE and < MemoryMap.LOCAL_INT_BASE:
            return self.global_memory.set_bool_value(address, value)
        else:
            print('Error de ejecución: Dirección virtual desconocida')
            return None

    def set_local_value(self, address, value):
        if address >= MemoryMap.LOCAL_INT_BASE and address < MemoryMap.LOCAL_FLOAT_BASE:
            return self.get_local_memory().set_int_value(address, value)
        elif address >= MemoryMap.LOCAL_FLOAT_BASE and address < MemoryMap.LOCAL_STRING_BASE:
            return self.get_local_memory().set_float_value(address, value)
        elif address >= MemoryMap.LOCAL_STRING_BASE and address < MemoryMap.LOCAL_BOOL_BASE:
            return self.get_local_memory().set_string_value(address, value)
        elif address >= MemoryMap.LOCAL_BOOL_BASE and < MemoryMap.TEMP_INT_BASE:
            return self.get_local_memory().set_bool_value(address, value)
        else:
            print('Error de ejecución: Dirección virtual desconocida')
            return None

    def set_temp_value(self, address, value):
        if address >= MemoryMap.TEMP_INT_BASE and address < MemoryMap.TEMP_FLOAT_BASE:
            return self.get_local_memory().set_temp_int_value(address, value)
        elif address >= MemoryMap.TEMP_FLOAT_BASE and address < MemoryMap.TEMP_STRING_BASE:
            return self.get_local_memory().set_temp_float_value(address, value)
        elif address >= MemoryMap.TEMP_STRING_BASE and address < MemoryMap.TEMP_BOOL_BASE:
            return self.get_local_memory().set_temp_string_value(address, value)
        elif address >= MemoryMap.TEMP_BOOL_BASE and < MemoryMap.POINTER_BASE:
            return self.get_local_memory().set_temp_bool_value(address, value)
        else:
            print('Error de ejecución: Dirección virtual desconocida')
            return None

    def get_local_memory(self):
        return self.memory_stack[-1]




