class ConstantTable:
    ''' Clase que maneja la tabla de constantes que se van a usar en la
        Máquina Virtual, estas contienen direcciones del 0 al 10000 y se
        manejan las direcciones según su tipo'''

    FALSE_CONSTANT = 0
    TRUE_CONSTANT = 1
    INT_CONSTANT_BASE = 1000
    FLOAT_CONSTANT_BASE = 2000
    STRING_CONSTANT_BASE = 3000

    # Se inicializa la tabla de constantes con listas vacías de enteros, flotantes
    # y strings
    def __init__(self):
        self.table = dict(int={}, float={}, string={})

    # Agrega una constante a la tabla, según la direccion de la constante se determina si es de tipo
    # entera, flotante, string o booleana y se agrega el valor a su lista correspondiente.
    # Si se da otra dirección que no sea de la 0 a la 10000 se marca un error por direccion desconocida
    def add_constant(self, address, value):
        if address >= ConstantTable.INT_CONSTANT_BASE and address < ConstantTable.FLOAT_CONSTANT_BASE:
            self.table['int'][self.translate_address(address, ConstantTable.INT_CONSTANT_BASE)] = value
        elif address >= ConstantTable.FLOAT_CONSTANT_BASE and address < ConstantTable.STRING_CONSTANT_BASE:
            self.table['float'][self.translate_address(address, ConstantTable.FLOAT_CONSTANT_BASE)] = value
        elif address >= ConstantTable.STRING_CONSTANT_BASE:
            self.table['string'][self.translate_address(address, ConstantTable.STRING_CONSTANT_BASE)] = value
        else:
            print('Error de ejecucion: Direccion virtual desconocida')
            return None

    # Regresa el valor de la constante entera de la dirección que se está pidiendo
    def get_int_value(self, address):
        return self.table['int'][self.translate_address(address, ConstantTable.INT_CONSTANT_BASE)]

    # Regresa el valor de la constante flotante de la dirección que se está pidiendo
    def get_float_value(self, address):
        return self.table['float'][self.translate_address(address, ConstantTable.FLOAT_CONSTANT_BASE)]

    # Regresa el valor de la constante string de la dirección que se está pidiendo
    def get_string_value(self, address):
        return self.table['string'][self.translate_address(address, ConstantTable.STRING_CONSTANT_BASE)]

    #Convierte la dirección dada a una direccion específica de una lista
    # Necesita la dirección base del tipo requerido, y la dirección que se está buscando
    def translate_address(self, address, offset):
        return address - offset
