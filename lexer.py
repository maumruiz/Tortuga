import ply.lex as lex

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


lexer = lex.lex()

def lex(input):
  lexer.input(input)
