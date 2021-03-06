class Memory:
    ''' Clase que maneja una estructura de memoria que va a utilizar la Máquina Virtual
        Contiene la memoria de variables ya sea globales o locales con sus temporales
        correspondientes. Se lleva un registro de variables enteras, flotantes, string, bool
        y pointers y registro de temporales con los mismos tipos'''

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

    # Inicializa la memoria. Recibe un booleano especificando si la memoria es global o local,
    # también recibe un size_dict con las variables a inicializar
    def __init__(self, is_global, size_dict):
        self.register = dict(int=[], float=[], string=[], bool=[], pointer=[])
        self.temp_register = dict(int=[], float=[], string=[], bool=[])
        if is_global:
            self.int_offset = Memory.INT_BASE
            self.float_offset = Memory.FLOAT_BASE
            self.string_offset = Memory.STRING_BASE
            self.bool_offset = Memory.BOOL_BASE
            self.pointer_offset = Memory.POINTER_BASE
            self.register['pointer'] = [0 for x in range(size_dict['pointer'])]
        else:
            self.int_offset = Memory.LOCAL_INT_BASE
            self.float_offset = Memory.LOCAL_FLOAT_BASE
            self.string_offset = Memory.LOCAL_STRING_BASE
            self.bool_offset = Memory.LOCAL_BOOL_BASE
        self.temp_int_offset = Memory.TEMP_INT_BASE
        self.temp_float_offset = Memory.TEMP_FLOAT_BASE
        self.temp_string_offset = Memory.TEMP_STRING_BASE
        self.temp_bool_offset = Memory.TEMP_BOOL_BASE
        self.register['int'] = [0 for x in range(size_dict['int'])]
        self.register['float'] = [0 for x in range(size_dict['float'])]
        self.register['string'] = ['' for x in range(size_dict['string'])]
        self.register['bool'] = [False for x in range(size_dict['bool'])]
        self.temp_register['int'] = [0 for x in range(size_dict['int_temp'])]
        self.temp_register['float'] = [0 for x in range(size_dict['float_temp'])]
        self.temp_register['string'] = ['' for x in range(size_dict['string_temp'])]
        self.temp_register['bool'] = [False for x in range(size_dict['bool_temp'])]

    # Función que agrega una variable global. Se determina el tipo de variable según la
    # dirección que recibe, y agrega al registro la variable dada con un valor default
    def add_global_variable(self, address):
        if address >= Memory.INT_BASE and address < Memory.FLOAT_BASE:
            self.register['int'][self.translate_address(address, self.int_offset)] = 0
        elif address >= Memory.FLOAT_BASE and address < Memory.STRING_BASE:
            self.register['float'][self.translate_address(address, self.float_offset)] = 0
        elif address >= Memory.STRING_BASE and address < Memory.BOOL_BASE:
            self.register['string'][self.translate_address(address, self.string_offset)] = ""
        elif address >= Memory.BOOL_BASE and address < Memory.LOCAL_INT_BASE:
            self.register['bool'][self.translate_address(address, self.bool_offset)] = False
        else:
            print('Error de ejecucion: Direccion virtual desconocida')
            return None

    # Función que agrega una variable local. Se determina el tipo de variable según la
    # dirección que recibe, y agrega al registro la variable dada con un valor default
    def add_local_variable(self, address):
        if address >= Memory.LOCAL_INT_BASE and address < Memory.LOCAL_FLOAT_BASE:
            self.register['int'][self.translate_address(address, self.int_offset)] = 0
        elif address >= Memory.LOCAL_FLOAT_BASE and address < Memory.LOCAL_STRING_BASE:
            self.register['float'][self.translate_address(address, self.float_offset)] = 0
        elif address >= Memory.LOCAL_STRING_BASE and address < Memory.LOCAL_BOOL_BASE:
            self.register['string'][self.translate_address(address, self.string_offset)] = ""
        elif address >= Memory.LOCAL_BOOL_BASE and address < Memory.TEMP_INT_BASE:
            self.register['bool'][self.translate_address(address, self.bool_offset)] = False
        else:
            print('Error de ejecucion: Direccion virtual desconocida')
            return None

    # Función que agrega una variable temporal. Se determina el tipo de variable según la
    # dirección que recibe, y agrega al registro la variable dada con un valor default
    def add_temp_variable(self, address):
        if address >= Memory.TEMP_INT_BASE and address < Memory.TEMP_FLOAT_BASE:
            self.temp_register['int'][self.translate_address(address, self.temp_int_offset)] = 0
        elif address >= Memory.TEMP_FLOAT_BASE and address < Memory.TEMP_STRING_BASE:
            self.temp_register['float'][self.translate_address(address, self.temp_float_offset)] = 0
        elif address >= Memory.TEMP_STRING_BASE and address < Memory.TEMP_BOOL_BASE:
            self.temp_register['string'][self.translate_address(address, self.temp_string_offset)] = ""
        elif address >= Memory.TEMP_BOOL_BASE and address < Memory.POINTER_BASE:
            self.temp_register['bool'][self.translate_address(address, self.temp_bool_offset)] = False
        else:
            print('Error de ejecucion: Direccion virtual desconocida')
            return None

    # Función que regresa el valor entero, ya sea global o local segun el tipo de memoria,
    # de la dirección que se recibe
    def get_int_value(self, address):
        return self.register['int'][self.translate_address(address, self.int_offset)]

    # Función que regresa el valor flotante, ya sea global o local segun el tipo de memoria,
    # de la dirección que se recibe
    def get_float_value(self, address):
        return self.register['float'][self.translate_address(address, self.float_offset)]

    # Función que regresa el valor string, ya sea global o local segun el tipo de memoria,
    # de la dirección que se recibe
    def get_string_value(self, address):
        return self.register['string'][self.translate_address(address, self.string_offset)]

    # Función que regresa el valor bool, ya sea global o local segun el tipo de memoria,
    # de la dirección que se recibe
    def get_bool_value(self, address):
        return self.register['bool'][self.translate_address(address, self.bool_offset)]

    # Función que regresa el valor entero temporal
    # de la dirección que se recibe
    def get_temp_int_value(self, address):
        return self.temp_register['int'][self.translate_address(address, self.temp_int_offset)]

    # Función que regresa el valor float temporal
    # de la dirección que se recibe
    def get_temp_float_value(self, address):
        return self.temp_register['float'][self.translate_address(address, self.temp_float_offset)]

    # Función que regresa el valor string temporal
    # de la dirección que se recibe
    def get_temp_string_value(self, address):
        return self.temp_register['string'][self.translate_address(address, self.temp_string_offset)]

    # Función que regresa el valor bool temporal
    # de la dirección que se recibe
    def get_temp_bool_value(self, address):
        return self.temp_register['bool'][self.translate_address(address, self.temp_bool_offset)]

    # Función que regresa el valor del pointer
    # de la dirección que se recibe
    def get_pointer_value(self, address):
        return self.register['pointer'][self.translate_address(address, self.pointer_offset)]

    # Función que le pone un valor entero a la dirección recibida en el registro
    def set_int_value(self, address, value):
        self.register['int'][self.translate_address(address, self.int_offset)] = value

    # Función que le pone un valor flotante a la dirección recibida en el registro
    def set_float_value(self, address, value):
        self.register['float'][self.translate_address(address, self.float_offset)] = value

    # Función que le pone un valor string a la dirección recibida en el registro
    def set_string_value(self, address, value):
        self.register['string'][self.translate_address(address, self.string_offset)] = value

    # Función que le pone un valor bool a la dirección recibida en el registro
    def set_bool_value(self, address, value):
        self.register['bool'][self.translate_address(address, self.bool_offset)] = value

    # Función que le pone un valor entero temporal a la dirección recibida en el registro
    def set_temp_int_value(self, address, value):
        self.temp_register['int'][self.translate_address(address, self.temp_int_offset)]  = value

    # Función que le pone un valor flotante temporal a la dirección recibida en el registro
    def set_temp_float_value(self, address, value):
        self.temp_register['float'][self.translate_address(address, self.temp_float_offset)] = value

    # Función que le pone un valor string temporal a la dirección recibida en el registro
    def set_temp_string_value(self, address, value):
        self.temp_register['string'][self.translate_address(address, self.temp_string_offset)] = value

    # Función que le pone un valor bool temporal a la dirección recibida en el registro
    def set_temp_bool_value(self, address, value):
        self.temp_register['bool'][self.translate_address(address, self.temp_bool_offset)] = value

    # Función que le pone un valor pointer a la dirección recibida en el registro
    def set_pointer_value(self, address, value):
        self.register['pointer'][self.translate_address(address, self.pointer_offset)] = value

    #Convierte la dirección dada a una direccion específica de una lista
    # Necesita la dirección base del tipo requerido, y la dirección que se está buscando
    def translate_address(self, address, offset):
        return address - offset
