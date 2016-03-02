#Mylittleduck scanner parser
#Mauricio Mendez Ruiz
#A00812794

#Lexer rules

#Lista de tokens
tokens = (
    #Palabras reservadas
    'PROGRAM',
    'VAR',
    'PRINT',
    'IF',
    'ELSE',
    'INT',
    'FLOAT',

    #Separadores
    'COMA',
    'PUNTOYCOMA',
    'DOSPUNTOS',
    'LLAVEI',
    'LLAVED',
    'PARENTESISI',
    'PARENTESISD',

    #Operadores
    'IGUAL',
    'SUMA',
    'RESTA',
    'MULTIP',
    'DIVISION',
    'MAYOR',
    'MENOR',
    'DIFERENTE',

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
t_IGUAL = r'='
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIP = r'\*'
t_DIVISION = r'/'
t_MAYOR = r'>'
t_MENOR = r'<'

def t_PROGRAM(t):
    r'program'
    return t

def t_VAR(t):
    r'var'
    return t

def t_PRINT(t):
    r'print'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_DIFERENTE(t):
    r'<>'
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

def t_newline(t):
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
    'program : PROGRAM ID PUNTOYCOMA prog1'
    print("Programa terminado con exito")
    pass

def p_prog1(p):
    '''prog1 : vars bloque
            | bloque'''
    pass

def p_vars(p):
    'vars : VAR var1'
    pass

def p_var1(p):
    'var1 : var2 DOSPUNTOS tipo PUNTOYCOMA var3'
    pass

def p_var2(p):
    'var2 : ID var21'
    pass

def p_var21(p):
    '''var21 : COMA var2
            | vacio'''
    pass

def p_var3(p):
    '''var3 : var1
            | vacio'''
    pass

def p_tipo(p):
    '''tipo : INT
            | FLOAT'''
    pass

def p_bloque(p):
    'bloque : LLAVEI bloque1 LLAVED'
    pass

def p_bloque1(p):
    '''bloque1 : estatuto bloque1
            | vacio'''
    pass

def p_estatuto(p):
    '''estatuto : asignacion
            | condicion
            | escritura'''
    pass

def p_asignacion(p):
    'asignacion : ID IGUAL expresion PUNTOYCOMA'
    pass

def p_escritura(p):
    'escritura : PRINT PARENTESISI escr1 PARENTESISD PUNTOYCOMA'
    pass

def p_escr1(p):
    '''escr1 : expresion escr1
            | CTESTRING escr2'''
    pass

def p_escr2(p):
    '''escr2 : COMA escr1
            | vacio'''
    pass

def p_expresion(p):
    'expresion : exp expres1'
    pass

def p_expres1(p):
    '''expres1 : MAYOR exp
            | MENOR exp
            | DIFERENTE exp
            | vacio'''
    pass

def p_exp(p):
    'exp : termino exp1'
    pass

def p_exp1(p):
    '''exp1 : SUMA exp
            | RESTA exp
            | vacio'''
    pass

def p_condicion(p):
    'condicion : IF PARENTESISI expresion PARENTESISD bloque cond1 PUNTOYCOMA'
    pass

def p_cond1(p):
    '''cond1 : ELSE bloque
            | vacio'''
    pass

def p_termino(p):
    'termino : factor term1'
    pass

def p_term1(p):
    '''term1 : MULTIP termino
            | DIVISION termino
            | vacio'''
    pass

def p_factor(p):
    '''factor : PARENTESISI expresion PARENTESISD
            | SUMA varcte
            | RESTA varcte
            | varcte'''
    pass

def p_varcte(p):
    '''varcte : ID
            | CTEI
            | CTEF'''
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
