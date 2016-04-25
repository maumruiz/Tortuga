class Memory:
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

    def __init__(self, is_global):
        self.register = dict(int=[], float=[], string=[], bool=[])
        self.temp_register = dict(int=[], float=[], string=[], bool=[])
        if is_global:
            self.int_offset = Memory.INT_BASE
            self.float_offset = Memory.FLOAT_BASE
            self.string_offset = Memory.STRING_BASE
            self.bool_base = Memory.BOOL_BASE
        else: 
            self.int_offset = Memory.LOCAL_INT_BASE
            self.float_offset = Memory.LOCAL_FLOAT_BASE
            self.string_offset = Memory.LOCAL_STRING_BASE
            self.bool_base = Memory.LOCAL_BOOL_BASE
        self.temp_int_offset = Memory.TEMP_INT_BASE
        self.temp_float_offset = Memory.TEMP_FLOAT_BASE
        self.temp_string_offset = Memory.TEMP_STRING_BASE
        self.temp_bool_offset = Memory.TEMP_BOOL_BASE

    def get_int_value(self, address):
        return self.register['int'][translate_address(address, self.int_offset)]

    def get_float_value(self, address):
        return self.register['float'][translate_address(address, self.float_offset)]

    def get_string_value(self, address):
        return self.register['string'][translate_address(address, self.string_offset)]

    def get_bool_value(self, address):
        return self.register['bool'][translate_address(address, self.bool_offset)]

    def get_temp_int_value(self, address):
        return self.temp_register['int'][translate_address(address, self.int_offset)]

    def get_temp_float_value(self, address):
        return self.temp_register['float'][translate_address(address, self.float_offset)]

    def get_temp_string_value(self, address):
        return self.temp_register['string'][translate_address(address, self.string_offset)]

    def get_temp_bool_value(self, address):
        return self.temp_register['bool'][translate_address(address, self.bool_offset)]


    def set_int_value(self, address, value):
        self.register['int'][translate_address(address, self.int_offset)] = value

    def set_float_value(self, address, value):
        self.register['float'][translate_address(address, self.int_offset)] = value

    def set_string_value(self, address, value):
        self.register['string'][translate_address(address, self.string_offset)] = value

    def set_bool_value(self, address, value):
        self.register['bool'][translate_address(address, self.bool_offset)] = value

    def set_temp_int_value(self, address, value):
        self.temp_register['int'][translate_address(address, self.int_offset)]  = value

    def set_temp_float_value(self, address, value):
        self.temp_register['float'][translate_address(address, self.float_offset)] = value

    def set_temp_string_value(self, address, value):
        self.temp_register['string'][translate_address(address, self.string_offset)] = value

    def set_temp_bool_value(self, address, value):
        self.temp_register['bool'][translate_address(address, self.bool_offset)] = value

    def translate_address(self, address, offset):
        return address - offset





