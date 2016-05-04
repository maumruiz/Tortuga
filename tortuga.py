import sys

#Tortuga scanner y parser
# Archivo principal que lee un archivo para hacer su
# Análisis léxico, sintáctico y semántico, para despúes
# ejecutar los cuádruplos generados


#Lexer rules

#Lista de tokens
tokens = (
    #Palabras reservadas
    'PROGRAMA',
    'VAR',
    'SINO',
    'SI',
    'MIENTRAS',
    'REPETIR',
    'INT',
    'FLOAT',
    'STRING',
    'BOOL',
    'VERDADERO',
    'FALSO',
    'FUNC',
    'REGRESA',

    #Separadores
    'COMA',         # ,
    'PUNTOYCOMA',   # ;
    'DOSPUNTOS',    # :
    'LLAVEI',       #Llave izquierda ( {} )
    'LLAVED',       #Llave derecha ( } )
    'PARENTESISI',  #Parentesis Izquierdo ( ( )
    'PARENTESISD',  #Parentesis Derecho ( ) )
    'CORCHETEI',    #Corchete izquierdo ( [ )
    'CORCHETED',    #Corchete derecho ( ] )
    'ENDLINE',     # \n

    #Operadores
    'ASIGNACION',   # =
    'SUMA',         # +
    'RESTA',        # -
    'MULTIP',       # *
    'DIVISION',     # /
    'MAYOR',        # >
    'MENOR',        # <
    'MAYORIGUAL',   # >=
    'MENORIGUAL',   # <=
    'DIFERENTE',    # !=
    'IGUAL',        # ==
    'AND',          # &&
    'OR',           # ||

    #Primitivas
    'LEE',
    'ESCRIBE',
    'ADELANTE',
    'ATRAS',
    'DERECHA',
    'IZQUIERDA',
    'POSICION',
    'POSICION_X',
    'POSICION_Y',
    'COLOR_LINEA',
    'GROSOR_LINEA',
    'ALZAR_PLUMA',
    'BAJAR_PLUMA',
    'ACTIVAR_RELLENO',
    'DESACTIVAR_RELLENO',
    'COLOR_RELLENO',
    'COLOR_FONDO',
    'GUARDAR_POSICION',
    'RESTAURAR_POSICION',
    'RANDOM',
    'CIRCULO',

    # Tokens con expresiones regulares
    'ID',
    'CTEI',
    'CTEF',
    'CTESTRING',
)

#Expresiones regulares
t_COMA = r','
t_PUNTOYCOMA = r';'
t_DOSPUNTOS = r':'
t_LLAVEI = r'{'
t_LLAVED = r'}'
t_PARENTESISI = r'\('
t_PARENTESISD = r'\)'
t_CORCHETEI = r'\['
t_CORCHETED = r'\]'
t_ASIGNACION = r'='
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIP = r'\*'
t_DIVISION = r'/'
t_MAYOR = r'>'
t_MENOR = r'<'

# Funciones para las expresiones regulares
# Con más de un caracter
def t_PROGRAMA(t):
    r'programa'
    return t

def t_VAR(t):
    r'var'
    return t

def t_SINO(t):
    r'sino'
    return t

def t_SI(t):
    r'si'
    return t

def t_MIENTRAS(t):
    r'mientras'
    return t

def t_REPETIR(t):
    r'repetir'
    return t

def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_STRING(t):
    r'string'
    return t

def t_BOOL(t):
    r'bool'
    return t

def t_VERDADERO(t):
    r'verdadero'
    return t

def t_FALSO(t):
    r'falso'
    return t

def t_FUNC(t):
    r'func'
    return t

def t_REGRESA(t):
    r'regresa'
    return t

def t_DIFERENTE(t):
    r'!='
    return t

def t_IGUAL(t):
    r'=='
    return t

def t_MAYORIGUAL(t):
    r'>='
    return t

def t_MENORIGUAL(t):
    r'<='
    return t

def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_LEE(t):
    r'lee'
    return t

def t_ESCRIBE(t):
    r'escribe'
    return t

def t_ADELANTE(t):
    r'adelante'
    return t

def t_ATRAS(t):
    r'atras'
    return t

def t_DERECHA(t):
    r'derecha'
    return t

def t_IZQUIERDA(t):
    r'izquierda'
    return t

def t_POSICION(t):
    r'posicion'
    return t

def t_POSICION_X(t):
    r'posicion_x'
    return t

def t_POSICION_Y(t):
    r'posicion_y'
    return t

def t_COLOR_LINEA(t):
    r'color_linea'
    return t

def t_GROSOR_LINEA(t):
    r'grosor_linea'
    return t

def t_ALZAR_PLUMA(t):
    r'alzar_pluma'
    return t

def t_BAJAR_PLUMA(t):
    r'bajar_pluma'
    return t

def t_ACTIVAR_RELLENO(t):
    r'activar_relleno'
    return t

def t_DESACTIVAR_RELLENO(t):
    r'desactivar_relleno'
    return t

def t_COLOR_RELLENO(t):
    r'color_relleno'
    return t

def t_COLOR_FONDO(t):
    r'color_fondo'
    return t

def t_GUARDAR_POSICION(t):
    r'guardar_posicion'
    return t

def t_RESTAURAR_POSICION(t):
    r'restaurar_posicion'
    return t

def t_RANDOM(t):
    r'random'
    return t

def t_CIRCULO(t):
    r'circulo'
    return t

def t_ID(t):
    r'[a-zA-Z](_?[a-zA-Z0-9])*'
    return t

def t_CTEF(t):
    r'-?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'-?[0-9]+'
    t.value = int(t.value)
    return t

def t_CTESTRING(t):
    r'("[^"]*")|(\'[^\']*\')'
    return t

#Caracteres ignorados
# Espacio y tabulador
t_ignore = ' \t'

def t_ENDLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Lexical error: Illegal character '%s'" % t.value)
    t.lexer.skip(1)

#Build lexer
import ply.lex as lex
lexer = lex.lex()

# Importa las clases necesarias para el compilador
from register import Register
from quadruple_register import QuadrupleRegister
from op_codes import OpCodes
from virtual_machine import VirtualMachine

# Inicializacion de clases
register = Register()
quadruple_reg = QuadrupleRegister(lexer)
register.set_address_handler(quadruple_reg.address_handler)
main_goto_quadruple = 0


#Parsing rules

# Sintaxis principal de todo el programa
def p_programa(p):
    'programa : dec_programa progvar main_goto progfunc main_block'

    print("/////////////Programa terminado con exito///////////////")
    print(" ######### Register table  ###########")
    register.print_table()
    print(" ####### Debug Quadruples ############")
    quadruple_reg.print_debug_quadruples()
    print('########## Constants ###########')
    quadruple_reg.print_constants()
    print('########## Quadruple names ###########')
    quadruple_reg.print_name_quadruples()
    print('########## Quadruple dirs ###########')
    quadruple_reg.print_quadruples()

    print('##')
    register.function_list[0]['size_dict'] = register.address_handler.return_global_size_dict()
    # Cosigue el directorio de funciones de la clase register
    dir_funciones = register.function_list
    # Guarda la tabla de constantes que se tenía en el quadruple_register
    constant_table = quadruple_reg.constant_list
    # Guarda la lista de cuádruplos generados
    quadruple_list = quadruple_reg.quadruple_list

    quadruples = []
    # Guarda sólo las direcciones en los cuádruplos
    for quadruple in quadruple_list:
        oper = quadruple['operator']
        op_1 = quadruple['operand_1']
        op_2 = quadruple['operand_2']
        res = quadruple['result']
        if isinstance(op_1, dict):
            op_1 = op_1['address']
        if op_2 is not None:
            if isinstance(op_2, dict):
                op_2 = str(op_2['address'])
            else:
                op_2 = str(op_2)
        if isinstance(res, dict):
            res = res['address']
        quadruple_new = dict(operator=oper, operand_1=op_1, operand_2=op_2, result=res)
        quadruples.append(quadruple_new)
    # Genera un último cuádruplo al final que termina el programa
    quadruple_new = dict(operator="end", operand_1=None, operand_2=None, result=None)
    quadruples.append(quadruple_new)
    # Inicializa la máquina virtual y ejecuta los cuádruplos
    vm = VirtualMachine(quadruples, constant_table, dir_funciones)
    vm.execute_code()

# El ID del programa se guarda en el registro de directorio de procedimientos
def p_dec_programa(p):
    'dec_programa : PROGRAMA ID ENDLINE'
    #register.create(p[2])
    register.create("main")

# Declaración de variables
def p_progvar(p):
    '''progvar : var ENDLINE progvar
            | vacio'''

# Se crea el primer cuadruplo, que tendrá un goto
# a la primera instrucción del main
def p_main_goto(p):
    'main_goto :'
    register.main_goto_quadruple = quadruple_reg.get_next_quadruple()
    quadruple_reg.generate(OpCodes.GOTO, None, None, None)

# Declaración de funciones
def p_progfunc(p):
    '''progfunc : function progfunc
            | vacio'''

# Declaración de variables completas
def p_var(p):
    'var : VAR ID DOSPUNTOS type add_var arrdec varasign'
    # print("Nueva variable-- ID: " + p[2] + "   Tipo: " + p[6] + "   Valor: " + str(p[4]))

# Checa si la variable es un arreglo
def p_arrdec(p):
    '''arrdec : arrdec1
            | vacio'''

# Declaración del arreglo con su dimensión correspondiente
# Se crean en el registro las direcciones del arreglo
def p_arrdec1(p):
    'arrdec1 : CORCHETEI CTEI CORCHETED'
    variable = p[-1]
    register.create_array(variable['name'], p[2])
    register.address_handler.increment_address_count(variable['type'], register.current_scope, p[2])

# Agrega la variable encontrada con su id y tipo
def p_add_var(p):
    'add_var :'
    p[0] = register.add_variable(p[-3], p[-1])

# Agrega la variable al stack de operandos
def p_push_var(p):
    'push_var :'
    variable = register.get_variable(p[-5])
    quadruple_reg.push_operand(variable)

# Asigna un valor a una variable que se esta declarando
# Checa si los tipos de variable coinciden
def p_varasign(p):
    '''varasign : push_var ASIGNACION push_operator ssexp
            | vacio'''
    quadruple_reg.assignment_check()

# Tipos de variable
# Entero, flotante, string o bool
def p_type(p):
    '''type : INT
            | FLOAT
            | STRING
            | BOOL'''
    p[0] = p[1]

# Bloque principal del programa
def p_main_block(p):
    'main_block : fill_goto block1'

# Llena el primer cuádruplo del main con el número de cuádruplo de la
# primera instruccion del main
def p_fill_goto(p):
    'fill_goto :'
    quadruple_reg.fill_quadruple(register.main_goto_quadruple, quadruple_reg.get_next_quadruple())

# Endline opcional
def p_optional_endline(p):
    '''optional_endline : ENDLINE
                        | vacio'''

# Ciclo de estatutos que pueden estar en un bloque
def p_block1(p):
    '''block1 : statute block1
            | vacio'''

# Los estatutos que pueden estar en un bloque son asignación, declaración de variables,
# Condicionales, ciclos while o repeat, llamadas a funciónes y primitivas del lenguaje
def p_statute(p):
    '''statute : assignment ENDLINE
            | var ENDLINE
            | condition ENDLINE
            | while ENDLINE
            | loop ENDLINE
            | function_call ENDLINE
            | primitive_func ENDLINE'''

# Llamada a una funcion completa, con id y numero de parámetros
# Se limpian las variables que se van a usar y se genera un
# cuádruplo de retorno
def p_function(p):
    'function : FUNC ID dec_func PARENTESISI dec_varloc params PARENTESISD function_type func_block'
    register.clear_variables()
    quadruple_reg.generate_return_action()

# Se agrega la funcion con su id al registro de funciones
def p_dec_func(p):
    'dec_func :'
    register.add_function(p[-1])

# Checa si existen parámetros
def p_params(p):
    '''params : params1
            | vacio'''

# Checa el id y el tipo de parámetro que se está dando
def p_params1(p):
    'params1 : ID DOSPUNTOS type add_param params2'

# Agrega el parámetro para checar si coincide con su declaración
# y para darle el valor al parámetro
def p_add_param(p):
    'add_param : '
    register.add_param_counter += 1
    register.add_function_param(p[-3], p[-1])

# Checa si hay más parámetros
def p_params2(p):
    '''params2 : COMA params1
            | vacio'''

#Checa el tipo de funcion y se agrega al registro de funiones su tipo,
# Si no se declara algun tipo, se guarda como void
# Se guarda el cuádruplo siguiente en el el registro de función
def p_function_type(p):
    '''function_type : DOSPUNTOS type
            | vacio'''
    if p[1] is None:
        register.add_function_return_type('void')
    else:
        register.add_function_return_type(p[2])
    quadruple = quadruple_reg.get_next_quadruple()
    register.set_starting_quadruple(quadruple)

# Bloque de una funcion
def p_func_block(p):
    'func_block : LLAVEI optional_endline func_block1 LLAVED optional_endline'

#  Loop de estatutos de una funcion
def p_func_block1(p):
    '''func_block1 : func_statements func_block1
            | vacio'''

# Los estatutos para una funcion son asignacion, declaración de variables,
# Condicionales, ciclos while y repeat, llamadas a funcion y primitivas
def p_func_statements(p):
    '''func_statements : assignment ENDLINE
            | var ENDLINE
            | condition ENDLINE
            | while ENDLINE
            | loop ENDLINE
            | function_call ENDLINE
            | primitive_func ENDLINE
            | return ENDLINE'''

# Return de una función. Se guarda la función actual para guardarla en
# el scope global
def p_return(p):
    'return : REGRESA ssexp'
    function = register.function_list[register.current_scope]
    function_variable = register.get_variable(function['name'])
    quadruple_reg.generate_return_statement(function_variable)

def p_dec_varloc(p):
    'dec_varloc :'
    # print("Se crea la tabla de variables local. Tabla actual: " + p[-3])

# Asignación de un valor a una variable previamente declarada
def p_assignment(p):
    'assignment : ID push_id arrsino ASIGNACION push_operator ssexp'
    quadruple_reg.assignment_check()

# Super Super Expresion
def p_ssexp(p):
    'ssexp : sexp ssexp_check ssexp2'

def p_ssexp_check(p):
    'ssexp_check :'
    quadruple_reg.ssexp_check()

# La super super expresion contiene and y or, se agregan a la pila de operadores
def p_ssexp2(p):
    '''ssexp2 : AND push_operator sexp ssexp_check
            | OR push_operator sexp ssexp_check
            | vacio'''
    pass

# Super Expresion
def p_sexp(p):
    'sexp : exp sexp2'

# La super expresion contine los operadores binarios >, <, !=, ==, >= y <=
def p_sexp2(p):
    '''sexp2 : MAYOR push_operator exp sexp_check
            | MENOR push_operator exp sexp_check
            | DIFERENTE push_operator exp sexp_check
            | IGUAL push_operator exp sexp_check
            | MAYORIGUAL push_operator exp sexp_check
            | MENORIGUAL push_operator exp sexp_check
            | vacio'''

def p_sexp_check(p):
    'sexp_check :'
    quadruple_reg.sexp_check()

# Expresion
def p_exp(p):
    'exp : term exp_check exp1'

def p_exp_check(p):
    'exp_check :'
    quadruple_reg.exp_check()

# La expresion tiene los operadores de + y -
def p_exp1(p):
    '''exp1 : SUMA push_operator exp
            | RESTA push_operator exp
            | vacio'''

# Termino
def p_term(p):
    'term : factor term_check term1'

def p_term_check(p):
    'term_check :'
    quadruple_reg.term_check()

# Los terminos tienen los operadores de * y /
def p_term1(p):
    '''term1 : MULTIP push_operator term
            | DIVISION push_operator term
            | vacio'''

# Se agrega el operador a la pila de operadores
def p_push_operator(p):
    'push_operator :'
    quadruple_reg.push_operator(p[-1])

# Factor
# Un factor puede ser una expresión entre paréntesis, una constante,
# una variable, una llamada a función o una primitiva
def p_factor(p):
    '''factor : PARENTESISI push_fake_bottom ssexp PARENTESISD pop_fake_bottom
            | varconst
            | ID push_id arrsino
            | function_call push_function_return
            | primitive_func ENDLINE'''

# Agrega el retorno de la función, con su tipo y valor a la pila de retornos de función
def p_push_function_return(p):
    'push_function_return :'
    function = p[-1]
    return_type = function['type']
    function_variable = register.get_variable(function['name'])
    quadruple_reg.push_function_return(return_type, function_variable)

# Se agrega el ID de la variable a la pila de operandos
def p_push_id(p):
    'push_id :'
    variable = register.get_variable(p[-1])
    quadruple_reg.push_operand(variable)

# Agrega un fondo falso a la pila de operadores para poder manejar paréntesis y llaves
def p_push_fake_bottom(p):
    'push_fake_bottom :'
    quadruple_reg.push_fake_bottom()

# Quita un fondo falso de la pila de operadores
def p_pop_fake_bottom(p):
    'pop_fake_bottom :'
    quadruple_reg.pop_fake_bottom()

# Estatuto de condicion si, sino
def p_condition(p):
    'condition : SI PARENTESISI ssexp PARENTESISD start_if_check control_block cond1 end_if_check'

# Checa el inicio del if en el quadruple register
def p_start_if_check(p):
    'start_if_check :'
    quadruple_reg.begin_if_check()

# Termina el if después todo el bloque
def p_end_if_check(p):
    'end_if_check :'
    quadruple_reg.end_if_check()

# Checa si hay un sino
def p_cond1(p):
    '''cond1 : SINO else_check control_block
            | vacio'''

# Checa el sino en el quadruple register
def p_else_check(p):
    'else_check :'
    quadruple_reg.else_check()

# Declaración de un ciclo while
def p_while(p):
    'while : MIENTRAS start_while_check PARENTESISI ssexp PARENTESISD mid_while_check control_block end_while_check'

# Inicia el ciclo while en el quadruple register
def p_start_while_check(p):
    'start_while_check :'
    quadruple_reg.begin_while_check()

# Checa el ciclo while después de la expresión y paréntesis
def p_mid_while_check(p):
    'mid_while_check :'
    quadruple_reg.middle_while_check()

# Checa el final del while en el quadruple register
def p_end_while_check(p):
    'end_while_check :'
    quadruple_reg.end_while_check()

# Declaración del ciclo repetir
def p_loop(p):
    'loop : REPETIR PARENTESISI ssexp PARENTESISD start_repeat_check control_block end_repeat_check'

# Inicia el ciclo repetir después de la expresión y paréntesis
def p_start_repeat_check(p):
    'start_repeat_check :'
    quadruple_reg.begin_repeat_check()

# Termina el ciclo repetir al final del bloque
def p_end_repeat_check(p):
    'end_repeat_check :'
    quadruple_reg.end_repeat_check()

# El bloque de control de estatutos y condicionales
def p_control_block(p):
    'control_block : LLAVEI optional_endline control_block1 LLAVED'

# Loop de los estatutos de control
def p_control_block1(p):
    '''control_block1 : control_statements control_block1
            | vacio'''

# Los estatutos de control pueden ser asignaciones, condicionales, cilos while y repetir,
# Llamada a función o primitivas
def p_control_statements(p):
    '''control_statements : assignment ENDLINE
            | condition ENDLINE
            | while ENDLINE
            | loop ENDLINE
            | function_call ENDLINE
            | primitive_func ENDLINE
            | return ENDLINE'''

# Llamada a una función, Al final de la llamada genera un cuádruplo de gosub con la
# direccion de inicio de la función obtenida por el register.
def p_function_call(p):
    '''function_call : ID function_check PARENTESISI generate_era args PARENTESISD'''
    start_dir = register.get_function_starting_quadruple()
    register.verify_params_count()
    quadruple_reg.generate_gosub(start_dir)
    quadruple_reg.pop_fake_bottom()
    p[0] = register.get_current_function()
    # pop
    print("Function called")
    print(p[0])
    quadruple_reg.print_name_quadruples()

# Se checa que la función exista con el ID dado
def p_function_check(p):
    'function_check :'
    function_name = p[-1]
    register.set_current_function_call(function_name)
    quadruple_reg.push_fake_bottom()
    pass

# Genera un cuádruplo era con el nombre de la función y se inicializa el
# contador de parámetros en 0
def p_generate_era(p):
    'generate_era :'
    function_name = register.get_current_function()['name']
    quadruple_reg.generate_era(function_name)
    register.params_counter = 0
    print(register.get_current_function())

# Checa si hay argumentos en la llamada a función
def p_args(p):
    '''args : args1
            | vacio'''


def p_args1(p):
    'args1 : ssexp increment_counter init_argument args2'

# Se guarda el argumento,
# Checa si el tipo de argumento que se esta dando es el esperado
# y verifica que el numero de argumentos sea correcto
def p_init_argument(p):
    'init_argument :'
    arg_type = register.get_expected_arg_type()
    params_counter = register.params_counter
    param_max = register.get_param_max()
    quadruple_reg.verify_and_generate_argument(arg_type, params_counter, param_max)

# Checa si hay mas argumentos
def p_args2(p):
    '''args2 : COMA args1
            | vacio'''

# Incrementa el contador de parametros
def p_increment_counter(p):
    'increment_counter : '
    register.params_counter += 1

# las constantes pueden ser string, flotante, enteras o booleanas
def p_varconst(p):
    '''varconst : CTESTRING push_string_literal
            | CTEF push_float_literal
            | CTEI push_int_literal
            | boolvalue push_bool_literal'''

# Se agrega el registro de la constante string
def p_push_string_literal(p):
    'push_string_literal :'
    quadruple_reg.push_string_literal(str(p[-1]))

# Se agrega el registro de la constante etera
def p_push_int_literal(p):
    'push_int_literal :'
    quadruple_reg.push_int_literal(int(p[-1]))

# Se agrega el registro de la constante flotante
def p_push_float_literal(p):
    'push_float_literal :'
    quadruple_reg.push_float_literal(float(p[-1]))

# Se agrega el registro de la constante booleana
def p_push_bool_literal(p):
    'push_bool_literal :'
    quadruple_reg.push_bool_literal(p[-1])

# Checa si es arreglo la variable
def p_arrsino(p):
    '''arrsino : arraccess
            | vacio'''

# Accesa a la direccion del arreglo dado
def p_arraccess(p):
    'arraccess : CORCHETEI array_check ssexp CORCHETED'
    quadruple_reg.generate_array_access(p[2]['address'], p[2]['upper_limit'])

# Verifica el arreglo
def p_array_check(p):
    'array_check :'
    p[0] = quadruple_reg.array_check()

#Posibles valores del bool (verdadero y falso)
def p_boolvalue(p):
    '''boolvalue : VERDADERO
            | FALSO'''
    p[0] = p[1]

#Lista de funciones primitivas con sus parámetros
def p_primitive_func(p):
    '''primitive_func : ESCRIBE PARENTESISI ssexp PARENTESISD generate_write
            | LEE PARENTESISI ssexp PARENTESISD generate_read
            | ADELANTE PARENTESISI ssexp PARENTESISD generate_forward
            | ATRAS PARENTESISI ssexp PARENTESISD generate_backward
            | DERECHA PARENTESISI ssexp PARENTESISD generate_right
            | IZQUIERDA PARENTESISI ssexp PARENTESISD generate_left
            | POSICION PARENTESISI ssexp COMA ssexp PARENTESISD generate_pos
            | POSICION_X PARENTESISI ssexp PARENTESISD generate_pos_x
            | POSICION_Y PARENTESISI ssexp PARENTESISD generate_pos_y
            | COLOR_LINEA PARENTESISI ssexp COMA ssexp COMA ssexp PARENTESISD generate_line_color
            | GROSOR_LINEA PARENTESISI ssexp PARENTESISD generate_line_width
            | ALZAR_PLUMA PARENTESISI PARENTESISD generate_pen_up
            | BAJAR_PLUMA PARENTESISI PARENTESISD generate_pen_down
            | ACTIVAR_RELLENO PARENTESISI PARENTESISD generate_fill_true
            | DESACTIVAR_RELLENO PARENTESISI PARENTESISD generate_fill_false
            | COLOR_RELLENO PARENTESISI ssexp COMA ssexp COMA ssexp PARENTESISD generate_fill_color
            | COLOR_FONDO PARENTESISI ssexp COMA ssexp COMA ssexp PARENTESISD generate_background_color
            | GUARDAR_POSICION PARENTESISI PARENTESISD generate_save_position
            | RESTAURAR_POSICION PARENTESISI PARENTESISD generate_restore_position
            | RANDOM PARENTESISI ssexp PARENTESISD generate_random
            | CIRCULO PARENTESISI ssexp COMA ssexp PARENTESISD generate_circle '''

# Genera los cuádruplos de las siguientes primitivas

def p_generate_read(p):
    'generate_read :'
    quadruple_reg.generate_read()

def p_generate_write(p):
    'generate_write :'
    quadruple_reg.generate_write()

def p_generate_forward(p):
    'generate_forward :'
    quadruple_reg.generate_forward()

def p_generate_backward(p):
    'generate_backward :'
    quadruple_reg.generate_backward()

def p_generate_right(p):
    'generate_right :'
    quadruple_reg.generate_right()

def p_generate_left(p):
    'generate_left :'
    quadruple_reg.generate_left()

def p_generate_pos(p):
    'generate_pos :'
    quadruple_reg.generate_pos()

def p_generate_pos_x(p):
    'generate_pos_x :'
    quadruple_reg.generate_pos_x()

def p_generate_pos_y(p):
    'generate_pos_y :'
    quadruple_reg.generate_pos_y()

def p_generate_line_color(p):
    'generate_line_color :'
    quadruple_reg.generate_line_color()

def p_generate_line_width(p):
    'generate_line_width :'
    quadruple_reg.generate_line_width()

def p_generate_pen_up(p):
    'generate_pen_up :'
    quadruple_reg.generate_pen_up()

def p_generate_pen_down(p):
    'generate_pen_down :'
    quadruple_reg.generate_pen_down()

def p_generate_fill_true(p):
    'generate_fill_true :'
    quadruple_reg.generate_fill_true()

def p_generate_fill_false(p):
    'generate_fill_false :'
    quadruple_reg.generate_fill_false()

def p_generate_fill_color(p):
    'generate_fill_color :'
    quadruple_reg.generate_fill_color()

def p_generate_background_color(p):
    'generate_background_color :'
    quadruple_reg.generate_background_color()

def p_generate_save_position(p):
    'generate_save_position :'
    quadruple_reg.generate_save_position()

def p_generate_restore_position(p):
    'generate_restore_position :'
    quadruple_reg.generate_restore_position()

def p_generate_random(p):
    'generate_random :'
    quadruple_reg.generate_random()

def p_generate_circle(p):
    'generate_circle :'
    quadruple_reg.generate_circle()


# Expresion para un vacio
def p_vacio(p):
    'vacio :'

#Manejo de errores de sintaxis
def p_error(p):
    print("Syntax error at line " + str(p.lexer.lineno) + " : Unexpected token  " + str(p.value) )
    sys.exit

import ply.yacc as yacc
parser = yacc.yacc()

# Abre el archivo del input para leerlo y analizarlo
def main(argv):
    filename = sys.argv[1]
    file = open(filename)
    data = file.read()
    file.close()

    print(data)
    parser.parse(data, tracking = True)

if __name__ == '__main__':
    main(sys.argv)
