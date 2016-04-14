import sys

#Tortuga scanner y parser

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
    'ADELANTE',
    'ATRAS',
    'DERECHA',
    'IZQUIERDA',
    'ESCRIBIR',
    'POSICION',
    'COLOR_LINEA',
    'GROSOR_LINEA',
    'COLOR_RELLENO',
    'COLOR_FONDO',
    'SALTAR',
    'GUARDAR_POSICION',
    'RESTAURAR_POSICION',
    'GUARDAR_ESTILO',
    'RESTAURAR_ESTILO',
    'ALZAR_PLUMA',
    'BAJAR_PLUMA',
    'RANDOM',

    #Regex
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

def t_ESCRIBIR(t):
    r'escribir'
    return t

def t_POSICION(t):
    r'posicion'
    return t

def t_COLOR_LINEA(t):
    r'color_linea'
    return t

def t_GROSOR_LINEA(t):
    r'grosor_linea'
    return t

def t_COLOR_RELLENO(t):
    r'color_relleno'
    return t

def t_COLOR_FONDO(t):
    r'color_fondo'
    return t

def t_SALTAR(t):
    r'saltar'
    return t

def t_GUARDAR_POSICION(t):
    r'guardar_posicion'
    return t

def t_RESTAURAR_POSICION(t):
    r'restaurar_posicion'
    return t

def t_GUARDAR_ESTILO(t):
    r'guardar_estilo'
    return t

def t_RESTAURAR_ESTILO(t):
    r'restaurar_estilo'
    return t

def t_ALZAR_PLUMA(t):
    r'alzar_pluma'
    return t

def t_BAJAR_PLUMA(t):
    r'bajar_pluma'
    return t

def t_RANDOM(t):
    r'random'
    return t

def t_ID(t):
    r'[a-zA-Z](_?[a-zA-Z0-9])*'
    return t

def t_CTEF(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CTESTRING(t):
    r'\'([ a-zA-Z0-9_,;:\{\}\(\)=+\-*/\>\<\t\n])*\''
    return t

#Caracteres ignorados
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
from register import Register
from quadruple_register import QuadrupleRegister

#Parsing rules
register = Register()
quadruple_reg = QuadrupleRegister()

def p_programa(p):
    'programa : dec_programa dec_varglob progvar progfunc block'
    print("Programa terminado con exito")
    register.print_table()
    quadruple_reg.print_quadruple()
    pass

def p_dec_programa(p):
    'dec_programa : PROGRAMA ID ENDLINE'
    register.create(p[2])
    pass

def p_dec_varglob(p):
    'dec_varglob :'
    print("Se crea la tabla de variables globales. Tabla actual: global")
    pass

def p_progvar(p):
    '''progvar : var ENDLINE progvar
            | vacio'''
    pass

def p_progfunc(p):
    '''progfunc : function progfunc
            | vacio'''
    pass

def p_var(p):
    'var : VAR ID arrsino DOSPUNTOS type add_var varasign'
    # print("Nueva variable-- ID: " + p[2] + "   Tipo: " + p[6] + "   Valor: " + str(p[4]))
    pass

def p_arrsino(p):
    '''arrsino : arraccess
            | vacio'''
    pass

def p_add_var(p):
    'add_var :'
    register.add_variable(p[-4], p[-1])
    pass

def p_push_var(p):
    'push_var :'
    variable = register.get_variable(p[-5])
    quadruple_reg.push_operand(variable)
    pass

def p_varasign(p):
    '''varasign : push_var ASIGNACION push_operator ssexp
            | vacio'''
    # p[0] = p[2]
    quadruple_reg.assignment_check()
    pass

def p_type(p):
    '''type : INT arrsino
            | FLOAT arrsino
            | STRING arrsino
            | BOOL arrsino'''
    p[0] = p[1]
    pass

def p_block(p):
    'block : LLAVEI optional_endline block1 LLAVED ENDLINE'
    pass

def p_optional_endline(p):
    '''optional_endline : ENDLINE
                        | vacio'''

def p_block1(p):
    '''block1 : statute block1
            | vacio'''
    pass

def p_statute(p):
    '''statute : assignment ENDLINE
            | var ENDLINE
            | condition ENDLINE
            | while ENDLINE
            | loop ENDLINE
            | functionStmt ENDLINE'''
    pass

def p_function(p):
    'function : FUNC ID dec_func PARENTESISI dec_varloc params PARENTESISD function_type block'
    register.clear_variables()
    # print("Destruye tabla local:  " + p[2] + "    Tabla actual: Global")
    pass

def p_dec_func(p):
    'dec_func :'
    register.add_function(p[-1])
    pass

def p_dec_varloc(p):
    'dec_varloc :'
    # print("Se crea la tabla de variables local. Tabla actual: " + p[-3])
    pass

def p_function_type(p):
    '''function_type : DOSPUNTOS type
            | vacio'''
    if p[1] is None:
        register.add_function_return_type('void')
    else:
        register.add_function_return_type(p[1])
    pass

def p_params(p):
    '''params : params1
            | vacio'''
    pass

def p_params1(p):
    'params1 : ID DOSPUNTOS type params2'
    register.add_function_param(p[1], p[3])
    pass

def p_params2(p):
    '''params2 : COMA params1
            | vacio'''
    pass

def p_assignment(p):
    'assignment : ID arrsino push_id ASIGNACION push_operator ssexp'
    quadruple_reg.assignment_check()
    pass

# Super Super Expresion
def p_ssexp(p):
    'ssexp : sexp ssexp_check ssexp2'
    pass

def p_ssexp_check(p):
    'ssexp_check :'
    quadruple_reg.ssexp_check()
    pass

def p_ssexp2(p):
    '''ssexp2 : AND push_operator sexp ssexp_check
            | OR push_operator sexp ssexp_check
            | vacio'''
    pass

# Super Expresion
def p_sexp(p):
    'sexp : exp sexp2'
    pass

def p_sexp2(p):
    '''sexp2 : MAYOR push_operator exp sexp_check
            | MENOR push_operator exp sexp_check
            | DIFERENTE push_operator exp sexp_check
            | IGUAL push_operator exp sexp_check
            | MAYORIGUAL push_operator exp sexp_check
            | MENORIGUAL push_operator exp sexp_check
            | vacio'''
    pass

def p_sexp_check(p):
    'sexp_check :'
    quadruple_reg.sexp_check()
    pass

# Expresion
def p_exp(p):
    'exp : term exp_check exp1'
    pass

def p_exp_check(p):
    'exp_check :'
    quadruple_reg.exp_check()
    pass

def p_exp1(p):
    '''exp1 : SUMA push_operator exp
            | RESTA push_operator exp
            | vacio'''
    pass

# Termino
def p_term(p):
    'term : factor term_check term1'
    pass

def p_term_check(p):
    'term_check :'
    quadruple_reg.term_check()
    pass

def p_term1(p):
    '''term1 : MULTIP push_operator term
            | DIVISION push_operator term
            | vacio'''
    pass

def p_push_operator(p):
    'push_operator :'
    quadruple_reg.push_operator(p[-1])

# Factor
def p_factor(p):
    '''factor : PARENTESISI push_fake_bottom ssexp PARENTESISD pop_fake_bottom
            | varconst
            | ID arrsino push_id
            | functioncall'''
    pass

def p_push_id(p):
    'push_id :'
    variable = register.get_variable(p[-2])
    quadruple_reg.push_operand(variable)
    pass

def p_push_fake_bottom(p):
    'push_fake_bottom :'
    quadruple_reg.push_fake_bottom()
    pass

def p_pop_fake_bottom(p):
    'pop_fake_bottom :'
    quadruple_reg.pop_fake_bottom()
    pass

def p_condition(p):
    'condition : SI PARENTESISI ssexp PARENTESISD start_if_check control_block cond1 end_if_check'
    pass

def p_start_if_check(p):
    'start_if_check :'
    quadruple_reg.begin_if_check()
    pass

def p_end_if_check(p):
    'end_if_check :'
    quadruple_reg.end_if_check()
    pass

def p_cond1(p):
    '''cond1 : SINO else_check control_block
            | vacio'''
    pass

def p_else_check(p):
    'else_check :'
    quadruple_reg.else_check()
    pass

def p_while(p):
    'while : MIENTRAS PARENTESISI ssexp PARENTESISD control_block'
    pass

def p_loop(p):
    'loop : REPETIR PARENTESISI ssexp PARENTESISD control_block'
    pass

def p_control_block(p):
    'control_block : LLAVEI optional_endline control_block1 LLAVED'
    pass

def p_control_block1(p):
    '''control_block1 : control_statements block1
            | vacio'''
    pass

def p_control_statements(p):
    '''control_statements : assignment ENDLINE
            | condition ENDLINE
            | while ENDLINE
            | loop ENDLINE
            | functionStmt ENDLINE'''
    pass

def p_functionStmt(p):
    'functionStmt : functioncall'
    pass

def p_functioncall(p):
    '''functioncall : ID PARENTESISI args PARENTESISD
            | primitivefunc'''
    pass

def p_args(p):
    '''args : args1
            | vacio'''
    pass

def p_args1(p):
    'args1 : ssexp args2'
    pass

def p_args2(p):
    '''args2 : COMA args1
            | vacio'''
    pass

def p_varconst(p):
    '''varconst : CTESTRING
            | CTEI push_int_literal
            | CTEF push_float_literal
            | boolvalue push_bool_literal'''
    pass

def p_push_int_literal(p):
    'push_int_literal :'
    quadruple_reg.push_int_literal(int(p[-1]))
    pass

def p_push_float_literal(p):
    'push_float_literal :'
    quadruple_reg.push_int_literal(float(p[-1]))
    pass

def p_push_bool_literal(p):
    'push_bool_literal :'
    quadruple_reg.push_bool_literal(p[-1])
    pass

def p_arraccess(p):
    'arraccess : CORCHETEI ssexp CORCHETED'
    pass

def p_boolvalue(p):
    '''boolvalue : VERDADERO
            | FALSO'''
    p[0] = p[1]
    pass

def p_primitivefunc(p):
    '''primitivefunc : ADELANTE PARENTESISI ssexp PARENTESISD
            | ATRAS PARENTESISI ssexp PARENTESISD
            | DERECHA PARENTESISI PARENTESISD
            | DERECHA PARENTESISI ssexp PARENTESISD
            | DERECHA PARENTESISI ssexp COMA ssexp PARENTESISD
            | IZQUIERDA PARENTESISI PARENTESISD
            | IZQUIERDA PARENTESISI ssexp PARENTESISD
            | IZQUIERDA PARENTESISI ssexp COMA ssexp PARENTESISD
            | ESCRIBIR PARENTESISI ssexp PARENTESISD
            | POSICION PARENTESISI ssexp COMA ssexp PARENTESISD
            | COLOR_LINEA PARENTESISI ssexp COMA ssexp COMA ssexp PARENTESISD
            | GROSOR_LINEA PARENTESISI ssexp PARENTESISD
            | COLOR_RELLENO PARENTESISI ssexp COMA ssexp COMA ssexp COMA ssexp PARENTESISD
            | COLOR_FONDO PARENTESISI ssexp COMA ssexp COMA ssexp PARENTESISD
            | SALTAR PARENTESISI ssexp PARENTESISD
            | GUARDAR_POSICION PARENTESISI PARENTESISD
            | RESTAURAR_POSICION PARENTESISI PARENTESISD
            | GUARDAR_ESTILO PARENTESISI PARENTESISD
            | RESTAURAR_ESTILO PARENTESISI PARENTESISD
            | ALZAR_PLUMA PARENTESISI PARENTESISD
            | BAJAR_PLUMA PARENTESISI PARENTESISD
            | RANDOM PARENTESISI ssexp PARENTESISD'''
    pass

def p_vacio(p):
    'vacio :'
    pass

#Manejo de errores
def p_error(p):
    print("Syntax error at line " + str(p.lexer.lineno) + " : Unexpected token  " + str(p.value) )
    sys.exit
    pass

import ply.yacc as yacc
parser = yacc.yacc()

def main(argv):
    filename = sys.argv[1]
    file = open(filename)
    data = file.read()
    file.close()

    print(data)
    parser.parse(data, tracking = True)

if __name__ == '__main__':
    data = '''programa poligonos

func poligono(n: int) {
  repetir(n) {
  adelante(50)
  derecha(360.0 / n)
  }
}

{
  color_linea(84, 84, 84)
  var n = 3 : int
  mientras(n < 14) {
    var rojo = random(255) : int
    var azul = random(255) : int
    var verde = random(255) : int
    var alfa = 1 : int
    color_relleno(rojo,verde,azul,alfa-0.16)
    poligono(n)
    derecha(36)
    n = n+1
  }
}
    '''
    # parser.parse(data,tracking = True)
    main(sys.argv)
