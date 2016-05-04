from semantic_cube import SemanticCube
import sys

class VirtualAddressHandler:
    ''' Clase que se encarga del manejo de variables virtuales.
    La clase crea direcciones según si son globales, locales, constantes o temporales,
    y para cada una de estas revisa si son variables enteras, flotantes, strings o booleanos'''

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

    # Inicializa el virtual address handler con valores de 0
    # en los contadores de todos los tipos de variables
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

    # La función reset_local_counters reinicia los contadores de todas
    # las variables locales
    def reset_local_counters(self):
        self.local_int_count = 0
        self.local_float_count = 0
        self.local_string_count = 0
        self.local_bool_count = 0

    # La función reset_temp_counters reinicia los contadores de todas
    # las variables temporales
    def reset_temp_counters(self):
        self.temp_int_count = 0
        self.temp_float_count = 0
        self.temp_bool_count = 0
        self.temp_string_count = 0

    # La función return_size_dict crea un diccionario con los contadores de
    # todas las variables locales y temporales. Resetea los contadores locales
    # y los contadores temporales, y regresa el diccionario creado
    def return_size_dict(self):
        size_dict = dict(int=self.local_int_count, float=self.local_float_count,
                         string=self.local_string_count, bool=self.local_bool_count,
                         int_temp=self.temp_int_count, float_temp=self.temp_float_count,
                         string_temp=self.temp_string_count, bool_temp=self.temp_bool_count)
        self.reset_local_counters()
        self.reset_temp_counters()
        return size_dict

    # La función return_size_dict crea un diccionario con los contadores de
    # todas las variables globales y temporales. Resetea los contadores
    # temporales, y regresa el diccionario creado
    def return_global_size_dict(self):
        size_dict = dict(int=self.int_count, float=self.float_count,
                         string=self.string_count, bool=self.bool_count,
                         int_temp=self.temp_int_count, float_temp=self.temp_float_count,
                         string_temp=self.temp_string_count, bool_temp=self.temp_bool_count,
                         pointer=self.pointer_count)
        self.reset_temp_counters()
        return size_dict

    # La función next_variable_address recibe el tipo de variable y el scope,
    # si el scope es global, llama a la función que regresa una variable global,
    # si el scope es local, llama a la función que regresa una variable local
    def next_variable_address(self, variable_type, scope):
        if scope == self.GLOBAL_SCOPE:
            return self.next_global_variable_address(variable_type)
        else:
            return self.next_local_variable_address(variable_type)

    # La función next_global_variable_address recibe un tipo de variable, y con
    # este tipo de variable decide el tipo de variable global a crear
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

    # La función next_local_variable_address recibe un tipo de variable, y con
    # este tipo de variable decide el tipo de variable local a crear
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

    # La función next_temp_variable_address recibe un tipo de variable, y con
    # este tipo de variable decide el tipo de variable temporal a crear
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

    # la función next_int_constant_address regresa una dirección sumando la dirección
    # base de constantes enteras y el contador de constantes enteras
    # Se le suma uno al contador de constantes enteras
    def next_int_constant_address(self):
        address = VirtualAddressHandler.INT_CONSTANT_BASE + self.int_constant_count
        self.int_constant_count += 1
        return address

    # la función next_float_constant_address regresa una dirección sumando la dirección
    # base de constantes flotantes y el contador de constantes flotantes
    # Se le suma uno al contador de constantes flotantes
    def next_float_constant_address(self):
        address = VirtualAddressHandler.FLOAT_CONSTANT_BASE + self.float_constant_count
        self.float_count += 1
        return address

    # la función next_string_constant_address regresa una dirección sumando la dirección
    # base de constantes string y el contador de constantes string
    # Se le suma uno al contador de constantes string
    def next_string_constant_address(self):
        address = VirtualAddressHandler.STRING_CONSTANT_BASE + self.string_constant_count
        self.string_constant_count += 1
        return address

    # la función next_int_address regresa una dirección sumando la dirección
    # base de enteros globales y el contador de globales enteros
    # Se le suma uno al contador de globales enteros
    def next_int_address(self):
        address = VirtualAddressHandler.INT_BASE + self.int_count
        self.int_count += 1
        return address

    # la función next_float_address regresa una dirección sumando la dirección
    # base de flotantes globales y el contador de globales flotantes
    # Se le suma uno al contador de globales flotantes
    def next_float_address(self):
        address = VirtualAddressHandler.FLOAT_BASE + self.float_count
        self.float_count += 1
        return address

    # la función next_string_address regresa una dirección sumando la dirección
    # base de strings globales y el contador de globales strings
    # Se le suma uno al contador de globales strings
    def next_string_address(self):
        address = VirtualAddressHandler.STRING_BASE + self.string_count
        self.string_count += 1
        return address

    # la función next_bool_address regresa una dirección sumando la dirección
    # base de bools globales y el contador de globales bools
    # Se le suma uno al contador de globales bools
    def next_bool_address(self):
        address = VirtualAddressHandler.BOOL_BASE + self.bool_count
        self.bool_count += 1
        return address

    # la función next_local_int_address regresa una dirección sumando la dirección
    # base de enteros locales y el contador de locales enteros
    # Se le suma uno al contador de locales enteros
    def next_local_int_address(self):
        address = VirtualAddressHandler.LOCAL_INT_BASE + self.local_int_count
        self.local_int_count += 1
        return address

    # la función next_local_float_address regresa una dirección sumando la dirección
    # base de enteros flotantes y el contador de locales flotantes
    # Se le suma uno al contador de locales flotantes
    def next_local_float_address(self):
        address = VirtualAddressHandler.LOCAL_FLOAT_BASE + self.local_float_count
        self.local_float_count += 1
        return address

    # la función next_local_string_address regresa una dirección sumando la dirección
    # base de strings locales y el contador de locales strings
    # Se le suma uno al contador de locales strings
    def next_local_string_address(self):
        address = VirtualAddressHandler.LOCAL_STRING_BASE + self.local_string_count
        self.local_string_count += 1
        return address

    # la función next_bool_int_address regresa una dirección sumando la dirección
    # base de enteros bool y el contador de locales bool
    # Se le suma uno al contador de locales bool
    def next_local_bool_address(self):
        address = VirtualAddressHandler.LOCAL_BOOL_BASE + self.local_bool_count
        self.local_bool_count += 1
        return address

    # la función next_temp_int_address regresa una dirección sumando la dirección
    # base de enteros temporales y el contador de temporales enteros
    # Se le suma uno al contador de temporales enteros
    def next_temp_int_address(self):
        address = VirtualAddressHandler.TEMP_INT_BASE + self.temp_int_count
        self.temp_int_count += 1
        return address

    # la función next_temp_float_address regresa una dirección sumando la dirección
    # base de flotantes temporales y el contador de temporales flotantes
    # Se le suma uno al contador de temporales flotantes
    def next_temp_float_address(self):
        address = VirtualAddressHandler.TEMP_FLOAT_BASE + self.temp_float_count
        self.temp_float_count += 1
        return address

    # la función next_temp_string_address regresa una dirección sumando la dirección
    # base de strings temporales y el contador de temporales strings
    # Se le suma uno al contador de temporales string
    def next_temp_string_address(self):
        address = VirtualAddressHandler.TEMP_STRING_BASE + self.temp_string_count
        self.temp_string_count += 1
        return address

    # la función next_temp_bool_address regresa una dirección sumando la dirección
    # base de bool temporales y el contador de temporales bool
    # Se le suma uno al contador de temporales bool
    def next_temp_bool_address(self):
        address = VirtualAddressHandler.TEMP_BOOL_BASE + self.temp_bool_count
        self.temp_bool_count += 1
        return address

    # la función next_pointer_address regresa una dirección sumando la dirección
    # base de pointers y el contador de pointers
    # Se le suma uno al contador de pointers
    def next_pointer_address(self):
        address = VirtualAddressHandler.POINTER_BASE + self.pointer_count
        self.pointer_count += 1
        return address

    # La función increment_address_count recibe un tipo de variable, un scope y
    # un contador. Si el scope es 0 se busca el tipo de variable global y se agrega
    # el numero del contador. Si es diferente scope se busca el tipo de variable
    # local y se agrega el numero del contador.
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

    # Incrementa el contador de enteros globales por la cantidad recibida
    def increment_int_count(self, count):
        self.int_count += count

    # Incrementa el contador de flotantes globales por la cantidad recibida
    def increment_float_count(self, count):
        self.float_count += count

    # Incrementa el contador de strings globales por la cantidad recibida
    def increment_string_count(self, count):
        self.string_count += count

    # Incrementa el contador de bools globales por la cantidad recibida
    def increment_bool_count(self, count):
        self.bool_count += count

    # Incrementa el contador de enteros locales por la cantidad recibida
    def increment_local_int_count(self, count):
        self.local_int_count += count

    # Incrementa el contador de flotantes locales por la cantidad recibida
    def increment_local_float_count(self, count):
        self.local_float_count += count

    # Incrementa el contador de strings locales por la cantidad recibida
    def increment_local_string_count(self, count):
        self.local_string_count += count

    # Incrementa el contador de bools locales por la cantidad recibida
    def increment_local_bool_count(self, count):
        self.local_bool_count += count
