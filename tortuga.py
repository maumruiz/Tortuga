#Tortuga scanner y parser

#Lexer rules

#Lista de tokens
tokens = (
    #Palabras reservadas
    'PROGRAMA',
    'VAR',
    'SI',
    'SINO',
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

def t_SI(t):
    r'si'
    return t

def t_SINO(t):
    r'sino'
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

def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'||'
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

def t_CTEI(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CTEF(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTESTRING(t):
    r'\'([ a-zA-Z0-9_,;:\{\}\(\)=+\-*/\>\<\t\n])*\''
    return t

#Caracteres ignorados
t_ignore = ' \t'

def t_ENDLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Lexical error: Illegal character '%s'" % t.value)
    t.lexer.skip(1)

#Build lexer
import ply.lex as lex
lexer = lex.lex()

#Parsing rules

def p_programa(p):
    'programa : PROGRAMA ID ENDLINE progvar progfunc block'
    print("Programa terminado con exito")
    pass

def p_progvar(p):
    '''progvar : var progvar
            | vacio'''
    pass

def p_progfunc(p):
    '''progfunc : function progfunc
            | vacio'''
    pass

def p_var(p):
    'var : VAR ID arrsino varasign DOSPUNTOS type ENDLINE'
    pass

def p_arrsino(p):
    '''arrsino : arraccess
            | vacio'''
    pass

def p_varasign(p):
    '''varasign : ASIGNACION ssexp
            | vacio'''
    pass

def p_type(p):
    '''tipo : INT arrsino
            | FLOAT arrsino
            | STRING arrsino
            | BOOL arrsino'''
    pass

def p_block(p):
    'block : LLAVEI block1 LLAVED'
    pass

def p_block1(p):
    '''block1 : statute block1
            | vacio'''
    pass

def p_statute(p):
    '''statute : assignment
            | var
            | condition
            | while
            | loop
            | functionStmt'''
    pass

def p_function(p):
    'function : FUNC ID PARENTESISI params PARENTESISD function1 block'
    pass

def p_function1(p):
    '''function1 : DOSPUNTOS type
            | vacio'''
    pass

def p_params(p):
    '''params : params1
            | vacio'''
    pass

def p_params1(p):
    'params1 : ID DOSPUNTOS type params2'
    pass

def p_params2(p):
    '''params2 : COMA params1
            | vacio'''
    pass

def p_assignment(p):
    'assignment : ID arrsino IGUAL ssexp ENDLINE'
    pass

def p_ssexp(p):
    'ssexp : sexp ssexp2'
    pass

def p_ssexp2(p):
    '''ssexp2 : AND sexp
            | OR sexp
            | vacio'''
    pass

def p_sexp(p):
    'sexp : exp sexp2'
    pass

def p_sexp2(p):
    '''sexp2 : MAYOR exp
            | MENOR exp
            | DIFERENTE exp
            | IGUAL exp
            | vacio'''
    pass

def p_exp(p):
    'exp : term exp1'
    pass

def p_exp1(p):
    '''exp1 : SUMA exp
            | RESTA exp
            | vacio'''
    pass

def p_term(p):
    'term : factor term1'
    pass

def p_term1(p):
    '''term1 : MULTIP term
            | DIVISION term
            | vacio'''
    pass

def p_factor(p):
    '''factor : PARENTESISI ssexp PARENTESISD
            | ID arrsino
            | varconst
            | functioncall'''
    pass

def p_condition(p):
    'condition : SI PARENTESISI ssexp PARENTESISD block cond1 ENDLINE'
    pass

def p_cond1(p):
    '''cond1 : SINO block
            | vacio'''
    pass

def p_while(p):
    'while : MIENTRAS PARENTESISI ssexp PARENTESISD block ENDLINE'
    pass

def p_loop(p):
    'loop : REPETIR PARENTESISI ssexp PARENTESISD block ENDLINE'
    pass

def p_functionStmt(p):
    'functionStmt : functioncall ENDLINE'
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

def p_cond1(p):
    '''args2 : COMA args1
            | vacio'''
    pass

def p_varconst(p):
    '''varconst : CTESTRING
            | CTEI
            | CTEF
            | boolvalue'''
    pass

def p_arraccess(p):
    'arraccess : CORCHETEI ssexp CORCHETED'
    pass

def p_boolvalue(p):
    '''boolvalue : VERDADERO
            | FALSO'''
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
            | COLOR_RELLENO PARENTESISI ssexp COMA ssexp COMA ssexp PARENTESISD
            | COLOR_FONDO PARENTESISI ssexp COMA ssexp COMA ssexp PARENTESISD
            | SALTAR PARENTESISI ssexp PARENTESISD
            | GUARDAR_POSICION PARENTESISI PARENTESISD
            | RESTAURAR_POSICION PARENTESISI PARENTESISD
            | GUARDAR_ESTILO PARENTESISI PARENTESISD
            | RESTAURAR_ESTILO PARENTESISI PARENTESISD
            | ALZAR_PLUMA PARENTESISI PARENTESISD
            | BAJAR_PLUMA PARENTESISI PARENTESISD
            | RANDOM PARENTESISI PARENTESISD'''
    pass

def p_vacio(p):
    'vacio :'
    pass

#Manejo de errores
def p_error(p):
    print("Syntax error at line " + str(p.lexer.lineno) + " : Unexpected token  " + str(p.value) )
    pass

import ply.yacc as yacc
parser = yacc.yacc()

if __name__ == '__main__':
    data = '''
            program alfa ;
            var a, b, c : int;
                d, e, f : float;
            {
                a = 5 + 4 ;
                if ( a > 10 )
                {
                    print ( 'es mayor' );
                }
                else
                {
                    print ( 'es menor' );
                } ;
                print ( 'terminar' );
            }
            '''
    parser.parse(data,tracking = True)
