class ConstantTable:
    FALSE_CONSTANT = 0
    TRUE_CONSTANT = 1
    INT_CONSTANT_BASE = 1000
    FLOAT_CONSTANT_BASE = 2000
    STRING_CONSTANT_BASE = 3000

    def __init__(self):
        self.table = dict(int=[], float=[], string=[])

    def add_constant(self, address, value):
        if address >= ConstantTable.INT_CONSTANT_BASE and address < ConstantTable.FLOAT_CONSTANT_BASE:
            self.table['int'][self.translate_address(address, ConstantTable.INT_CONSTANT_BASE)] = value
        elif address >= ConstantTable.FLOAT_CONSTANT_BASE and address < ConstantTable.STRING_CONSTANT_BASE:
            self.table['float'][self.translate_address(address, ConstantTable.FLOAT_CONSTANT_BASE)] = value
        elif address >= ConstantTable.STRING_CONSTANT_BASE and address < ConstantTable.INT_BASE:
            self.table['string'][self.translate_address(address, ConstantTable.STRING_CONSTANT_BASE)] = value
        else:
            print('Error de ejecucion: Direccion virtual desconocida')
            return None

    def get_int_value(self, address):
        return self.table['int'][self.translate_address(address, ConstantTable.INT_CONSTANT_BASE)]

    def get_float_value(self, address):
        return self.table['float'][self.translate_address(address, ConstantTable.FLOAT_CONSTANT_BASE)]

    def get_string_value(self, address):
        return self.table['string'][self.translate_address(address, ConstantTable.BOOL_CONSTANT_BASE)]

    def translate_address(self, address, offset):
        return address - offset
