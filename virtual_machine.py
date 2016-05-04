from memory_map import MemoryMap
from constant_table import ConstantTable
from semantic_cube import SemanticCube
from logger import Logger
from random import randint
import sys
import turtle


class VirtualMachine:
    ''' Clase Maquina Virtual que se encarga de la ejecución de los cuádruplos generados.
    Se ocupa de la memoria en ejecución y de las acciones de las funciones primitivas
    que permiten generar output gráfico'''

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

    # El init de la máquina virtual recibe la lista de cúadruplos, la lista de constantes
    # y la tabla de funciones. con esto se inicializa la memoria constante, la lista de cuádruplos
    # el mapa de memoria, el cuádruplo actual se inicializa en 0, se crea la pila de retornos
    # y una posición guardada.
    def __init__(self, quadruples, constants, functions):
        self.log = Logger(False)
        self.log.write("///////////////////////////// Virtual Machine init ///////////////////////")
        self.constant_table = ConstantTable()
        for constant in constants:
            self.constant_table.add_constant(constant['address'], constant['name'])

        self.quadruple_list = quadruples
        self.constant_memory = self.constant_table.table
        self.memory_map = MemoryMap(self.constant_table, functions)
        self.current_quadruple = 0
        self.return_stack = []
        self.saved_position = (0, 0)

    # La función execute_code inicia el modo gráfico de Tortuga y ejecuta el primer cuádruplo
    # de la lista de cuádruplos. Mientras el cuádruplo actual sea menor al número de cuádruplos
    # en la lista, se va a incrementar el cuádruplo actual por uno y se siguen ejecutando
    # cuádruplos hasta que el cuádruplo actual sea mayor al número de cuádruplos
    def execute_code(self):
        self.log.write('================Ejecutando maquina virtual==========================')
        turtle.mode("logo")
        while self.current_quadruple < len(self.quadruple_list):
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            self.options[action](self,quadruple)
            self.current_quadruple = self.current_quadruple + 1

        self.log.write(" ================ Termina ejecucion de cuadruplos ==================")

    # La función op_multiplication recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y hace la multiplicacion de ellos. Al final vuelve a llamar
    # al mapa de memoria para asignarle el valor resultado a la direccion del resultado
    def op_multiplication(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 * operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " * " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_division recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y hace la division de ellos. Al final vuelve a llamar
    # al mapa de memoria para asignarle el valor resultado a la direccion del resultado
    def op_division(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)

        result = operand1 / operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " / " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_sum recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y hace la suma de ellos. Al final vuelve a llamar
    # al mapa de memoria para asignarle el valor resultado a la direccion del resultado
    def op_sum(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)

        if result_dir >= MemoryMap.POINTER_BASE:
            operand2 = operand2_dir
            self.log.write('############ Pointer Arithmetic ##################')
            self.log.write('Operand 1: '+ str(operand1))
            self.log.write('Operand 2: '+ str(operand2))
            self.log.write('############ Pointer Arithmetic ##################')

        result = operand1 + operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " + " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_substraction recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y hace la resta de ellos. Al final vuelve a llamar
    # al mapa de memoria para asignarle el valor resultado a la direccion del resultado
    def op_substraction(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 - operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " - " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_greater recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y compara si el operando 1 es mayor al operando 2.
    # Al final vuelve a llamar al mapa de memoria para asignarle el valor resultado a
    # la direccion del resultado
    def op_greater(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 > operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " > " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_lesser recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y compara si el operando 1 es menor al operando 2.
    # Al final vuelve a llamar al mapa de memoria para asignarle el valor resultado a
    # la direccion del resultado
    def op_lesser(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 < operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " < " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_equal recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y compara si el operando 1 es igual al operando 2.
    # Al final vuelve a llamar al mapa de memoria para asignarle el valor resultado a
    # la direccion del resultado
    def op_equal(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 == operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " == " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_not_equal recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y compara si el operando 1 es diferente al operando 2.
    # Al final vuelve a llamar al mapa de memoria para asignarle el valor resultado a
    # la direccion del resultado
    def op_not_equal(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 != operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " != " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_and recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y compara si el operando 1 y el operando 2 son True
    # Al final vuelve a llamar al mapa de memoria para asignarle el valor resultado a
    # la direccion del resultado
    def op_and(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 and operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " && " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_or recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y compara si el operando 1 o el operando 2 es True
    # Al final vuelve a llamar al mapa de memoria para asignarle el valor resultado a
    # la direccion del resultado
    def op_or(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 or operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " || " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_assignment recibe un cuádruplo. Saca la dirección del operando 1
    # y del resultado. Llama al mapa de memoria para conseguir el valor del operando 1.
    # Si la direccion del resultado es un pointer, llama al mapa de memoria para conseguir
    # su dirección. Al final vuelve a llamar al mapa de memoria para asignarle el valor
    # del operando 1 direccion del resultado
    def op_assignment(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)

        if result_dir >= MemoryMap.POINTER_BASE:
            result_dir = self.memory_map.get_pointer_address(result_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(result_dir) + " = " + str(operand1))

        self.memory_map.set_value(result_dir, operand1)

    # La función op_mayor_igual recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y compara si el operando 1 es mayor o igual al operando 2.
    # Al final vuelve a llamar al mapa de memoria para asignarle el valor resultado a
    # la direccion del resultado
    def op_mayor_igual(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 >= operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " >= " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_menor_igual recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir los valores
    # del operando 1 y operando 2 y compara si el operando 1 es menor o igual al operando 2.
    # Al final vuelve a llamar al mapa de memoria para asignarle el valor resultado a
    # la direccion del resultado
    def op_menor_igual(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        result_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        result = operand1 <= operand2

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   op2dir: " + str(operand2_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * " + str(operand1) + " <= " + str(operand2) + " = " + str(result))

        self.memory_map.set_value(result_dir, result)

    # La función op_goto recibe un cuádruplo. Saca el valor del operando 1 y actualiza
    # el cuádruplo actual con ese valor. Se ejecuta el cuádruplo del nuevo
    # cuádruplo actual
    def op_goto(self, quad):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")

        self.current_quadruple = int(quad['result'])

        self.log.write(" * GoTo: " + str(self.current_quadruple))

        quadruple = self.quadruple_list[self.current_quadruple];
        action = quadruple['operator']
        self.options[action](self, quadruple)

    # La función op_gotof recibe un cuádruplo. Saca la dirección del operando 1
    # y del resultado. Llama al mapa de memoria para conseguir el valor bool del operando 1.
    # Si la condición obtenida es False, se actualiza el cuádruplo actual con el valor del
    # resultado y se ejecuta el cuádruplo del nuevo cuádruplo actual
    def op_gotof(self, quad):
        operand1_dir = int(quad['operand_1'])
        result = int(quad['result'])

        condition = self.memory_map.get_value(operand1_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * GoToF: " + str(result) + "  condition: " + str(operand1_dir))

        if(not(condition)):
            self.current_quadruple = quad['result']
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            self.options[action](self, quadruple)

    # La función op_gotot recibe un cuádruplo. Saca la dirección del operando 1
    # y del resultado. Llama al mapa de memoria para conseguir el valor bool del operando 1.
    # Si la condición obtenida es True, se actualiza el cuádruplo actual con el valor del
    # resultado y se ejecuta el cuádruplo del nuevo cuádruplo actual
    def op_gotot(self, quad):
        operand1_dir = int(quad['operand_1'])
        result = int(quad['result'])

        condition = self.memory_map.get_value(operand1_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * GoToT: " + str(result) + "  condition: " + str(operand1_dir))

        if(condition):
            self.current_quadruple = quad['result']
            quadruple = self.quadruple_list[self.current_quadruple];
            action = quadruple['operator']
            self.options[action](self, quadruple)

    # La función op_era recibe un cuádruplo. Se incrementa en uno el nivel de
    # llamadas anidadas. Saca la dirección del operando 1 (es una dirección de función).
    # Se agrega a la pila de memoria, la función con el nombre encontrado
    def op_era(self, quadruple):
        self.memory_map.nested_call_level += 1

        func_name = quadruple['operand_1']

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * era: " + str(func_name))

        self.memory_map.push_local(func_name)

    # La función op_gosub recibe un cuádruplo. Se decrementa en uno el nivel de
    # llamadas anidadas. Saca la dirección del operando 1 (es una dirección de función).
    # Se agrega el siguiente número de cuádruplo a la pila de retorno (despues de la llamada)
    # Se actualiza el cuádruplo actual con el valor de la dirección de función
    # y se ejecuta el cuádruplo del nuevo cuádruplo actual
    def op_gosub(self, quadruple):
        self.memory_map.nested_call_level -= 1

        func_dir = int(quadruple['operand_1'])

        self.return_stack.append(self.current_quadruple + 1)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * gosub: " + str(func_dir))
        self.log.write(" * Return stack: " + str(self.return_stack))

        self.current_quadruple = func_dir
        quadruple = self.quadruple_list[self.current_quadruple];
        action = quadruple['operator']
        self.options[action](self, quadruple)

    # La función op_ret_act recibe un cuádruplo. Se saca una memoria local de la pila de memorias,
    # Se actualiza el cuádruplo actual sacando un valor de la pila de retorno
    # y se ejecuta el cuádruplo del nuevo cuádruplo actual
    def op_ret_act(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * return to func call: ")
        self.log.write(" * return stack: " + str(self.return_stack))

        self.memory_map.pop_local()
        self.current_quadruple = self.return_stack.pop()
        quadruple = self.quadruple_list[self.current_quadruple];
        action = quadruple['operator']
        self.options[action](self, quadruple)

    def op_return(self, quadruple):
        self.op_ret_act(quadruple)

    # La función op_param recibe un cuádruplo. Saca la dirección del operando 1
    # y del resultado. Llama al mapa de memoria para conseguir el valor del operando 1 (parametro).
    # Al final vuelve a llamar al mapa de memoria para asignarle el valor del parametro a
    # la direccion del resultado
    def op_param(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        result_dir = int(quadruple['result'])

        param_value = self.memory_map.get_param_value(operand1_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * op1dir: " + str(operand1_dir) + "   resdir: " + str(result_dir))
        self.log.write(" * param: " + str(result_dir) + " = " + str(param_value))

        self.memory_map.set_value(result_dir, param_value)

    # La función op_verify recibe un cuádruplo. Saca la dirección del operando 1,
    # del operando 2 y del resultado. Llama al mapa de memoria para conseguir el valor
    # del resultado. Si el valor de resultado es menor al operando 1 o mayor al operando 2
    # Marca un error de que el índice dado está fuera de los límites
    def op_verify(self, quadruple):
        operand1 = int(quadruple['operand_1'])
        operand2 = int(quadruple['operand_2'])
        subject_dir = int(quadruple['result'])

        value = self.memory_map.get_value(subject_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * verify: " + str(value) + " | " + str(operand1) + '-' + str(operand2))

        if value < operand1 or value >= operand2:
            self.log.write('Error: Indice fuera de los limites')
            exit(1)

    # La función read recibe un cuádruplo. Saca la dirección del operando 1, lee
    # una variable del teclado y se le asigna el valor al operando 1
    def read(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        value = self.memory_map.read_by_type(operand1_dir)
        self.log.write(" * read: " + str(value) + '->' + str(operand1_dir))

        self.memory_map.set_value(operand1_dir, value)

    # La función write recibe un cuádruplo. Saca la dirección del operando 1, y llama
    # al mapa de memoria para conseguir su valor. Al final imprime el valor en la consola
    def write(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * write: " + str(operand1_dir))
        print(str(operand1))

    # La función forward recibe un cuádruplo. Saca la dirección del operando 1, y llama
    # al mapa de memoria para conseguir su valor. Al final mueve la grafica adelante por el valor
    def forward(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * forward: " + str(operand1))
        turtle.forward(operand1)

    # La función backward recibe un cuádruplo. Saca la dirección del operando 1, y llama
    # al mapa de memoria para conseguir su valor. Al final mueve la grafica atras por el valor
    def backward(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * backward: " + str(operand1))
        turtle.backward(operand1)

    # La función right recibe un cuádruplo. Saca la dirección del operando 1, y llama
    # al mapa de memoria para conseguir su valor. Al final mueve la grafica a la derecha por el valor
    def right(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * right: " + str(operand1))
        turtle.right(operand1)

    # La función left recibe un cuádruplo. Saca la dirección del operando 1, y llama
    # al mapa de memoria para conseguir su valor. Al final mueve la grafica a la izquierda por el valor
    def left(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * left: " + str(operand1))
        turtle.left(operand1)

    # La función pos recibe un cuádruplo. Saca la dirección del operando 1 y el operando 2, y llama
    # al mapa de memoria para conseguir los valores. Al final cambia la posicion por estos valores en x y y
    def pos(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pos: " + str(operand1) + ' ' + str(operand1))
        turtle.setposition(operand1, operand2)

    # La función pos_x recibe un cuádruplo. Saca la dirección del operando 1, y llama
    # al mapa de memoria para conseguir su valor. Al final cambia la posicion de x por el valor
    def pos_x(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pos_x: " + str(operand1))
        turtle.setx(operand1)

    # La función pos_y recibe un cuádruplo. Saca la dirección del operando 1, y llama
    # al mapa de memoria para conseguir su valor. Al final cambia la posicion de y por el valor
    def pos_y(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pos_y: " + str(operand1))
        turtle.sety(operand1)

    # La función line_color recibe un cuádruplo. Saca la dirección del operando 1, el operando 2, y el resultado,
    # y llama al mapa de memoria para conseguir los valores. Al final cambia el color de linea por estos valores en rgb
    def line_color(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        operand3_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        operand3 = self.memory_map.get_value(operand3_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * line_color: " + str(operand1) + ' ' + str(operand1) + ' ' + str(operand3))
        turtle.colormode(255)
        turtle.pencolor(operand1, operand2, operand3)

    # La función line_width recibe un cuádruplo. Saca la dirección del operando 1, y llama
    # al mapa de memoria para conseguir su valor. Al final cambia el grosor de la linea por el valor
    def line_width(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand1 = self.memory_map.get_value(operand1_dir)
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * line_width: " + str(operand1))
        turtle.pensize(operand1)

    # La función pen_up recibe un cuádruplo, y alza la pluma para que no se pueda dibujar
    def pen_up(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pen_up: ")
        turtle.penup()

    # La función pen_down recibe un cuádruplo, y alza la pluma para que se pueda dibujar
    def pen_down(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * pen_down: ")
        turtle.pendown()

    # La función fill_true recibe un cuádruplo, y hace que haya un relleno en el dibujo
    def fill_true(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_true: ")
        turtle.begin_fill()

    # La función fill_false recibe un cuádruplo, y hace que no haya un relleno en el dibujo
    def fill_false(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_false: ")
        turtle.end_fill()

    # La función fill_color recibe un cuádruplo. Saca la dirección del operando 1, el operando 2, y el resultado,
    # y llama al mapa de memoria para conseguir los valores. Al final cambia el color de relleno por estos valores en rgb
    def fill_color(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        operand3_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        operand3 = self.memory_map.get_value(operand3_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_color: " + str(operand1) + ' ' + str(operand1) + ' ' + str(operand3))
        turtle.colormode(255)
        turtle.fillcolor(operand1, operand2, operand3)

    # La función background_color recibe un cuádruplo. Saca la dirección del operando 1, el operando 2, y el resultado,
    # y llama al mapa de memoria para conseguir los valores. Al final cambia el color de fondo por estos valores en rgb
    def background_color(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])
        operand3_dir = int(quadruple['result'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)
        operand3 = self.memory_map.get_value(operand3_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * background_color: " + str(operand1) + ' ' + str(operand1) + ' ' + str(operand3))
        turtle.colormode(255)
        turtle.bgcolor(operand1, operand2, operand3)

    # La función save_pos recibe un cuádruplo, y guarda la posicion
    def save_pos(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_true: ")
        self.saved_position = turtle.pos()

    # La función restore_pos recibe un cuádruplo, y restaura una posicion guardada
    def restore_pos(self, quadruple):
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * fill_true: ")
        turtle.setposition(self.saved_position[0], self.saved_position[1])

    # La función random recibe un cuádruplo. Saca la dirección del operando 1, y llama
    # al mapa de memoria para conseguir su valor. Al final genera un número random
    def random(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        result_dir = int(quadruple['result'])
        operand1 = self.memory_map.get_value(operand1_dir)
        
        result = randint(0, operand1)

        self.memory_map.set_value(result_dir, result)
        
        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * random: " + str(operand1))
        # turtle.pensize(operand1)

    # La función circle recibe un cuádruplo. Saca la dirección del operando 1 y el operando 2, y llama
    # al mapa de memoria para conseguir los valores. Al final se dibuja un circulo con el radio del valor del
    # operando 1 y angulo del valor del operando 2
    def circle(self, quadruple):
        operand1_dir = int(quadruple['operand_1'])
        operand2_dir = int(quadruple['operand_2'])

        operand1 = self.memory_map.get_value(operand1_dir)
        operand2 = self.memory_map.get_value(operand2_dir)

        self.log.write(" ****************** Quadruple " + str(self.current_quadruple) + " **********************")
        self.log.write(" * circle: " + str(operand1) + ' ' + str(operand1))
        turtle.circle(operand1, operand2)

    # La función op_end termina la ejecución gráfica de turtle.
    def op_end(self, quad):
        turtle.exitonclick()
        self.log.write(" end ")

    # Lista de opciones que se usa como switch
    options = {0 : op_multiplication,
                1: op_division,
                2: op_sum,
                3: op_substraction,
                4: op_greater,
                5: op_lesser,
                6: op_equal,
                7: op_not_equal,
                8: op_and,
                9: op_or,
                10: op_assignment,
                11: op_mayor_igual,
                12: op_menor_igual,
                13: op_goto,
                14: op_gotof,
                15: op_gotot,
                16: op_param,
                17: op_era,
                18: op_gosub,
                19: op_ret_act,
                20: op_return,
                21: op_verify,
                101: read,
                102: write,
                103: forward,
                104: backward,
                105: right,
                106: left,
                107: pos,
                108: pos_x,
                109: pos_y,
                110: line_color,
                111: line_width,
                112: pen_up,
                113: pen_down,
                114: fill_true,
                115: fill_false,
                116: fill_color,
                117: background_color,
                118: save_pos,
                119: restore_pos,
                120: random,
                121: circle,
                "end": op_end,
    }
