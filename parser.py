import ply.yacc as yacc
from lexer import tokens
# Parsing rules

def p_programa(p):
    'programa : dec_programa progvar progfunc block'
    print("Programa terminado con exito")
    pass

def p_dec_programa(p):
    'dec_programa : PROGRAMA ID ENDLINE'
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
    '''type : INT arrsino
            | FLOAT arrsino
            | STRING arrsino
            | BOOL arrsino'''
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
    'assignment : ID arrsino ASIGNACION ssexp ENDLINE'
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
    'condition : SI PARENTESISI ssexp PARENTESISD block cond1'
    pass

def p_cond1(p):
    '''cond1 : SINO block
            | vacio'''
    pass

def p_while(p):
    'while : MIENTRAS PARENTESISI ssexp PARENTESISD block'
    pass

def p_loop(p):
    'loop : REPETIR PARENTESISI ssexp PARENTESISD block'
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

def p_args2(p):
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
    pass

parser = yacc.yacc()