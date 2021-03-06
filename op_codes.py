class OpCodes:
    ''' Clase que contiene las codigos de operación para todos
        los operadores y primitivas'''

    FAKE_BOTTOM = -1
    MULTIPLICATION = 0
    DIVISION = 1
    SUM = 2
    SUBSTRACTION = 3
    GREATER = 4
    LESSER = 5
    EQUAL = 6
    NOT_EQUAL = 7
    AND = 8
    OR = 9
    ASSIGNMENT = 10
    MAYOR_IGUAL = 11
    MENOR_IGUAL = 12
    GOTO = 13
    GOTOF = 14
    GOTOT = 15
    PARAM = 16
    ERA = 17
    GOSUB = 18
    RET = 19
    RETURN = 20
    VERIFY = 21

    READ = 101
    WRITE = 102
    FORWARD = 103
    BACKWARD = 104
    RIGHT = 105
    LEFT = 106
    POS = 107
    POS_X = 108
    POS_Y = 109
    LINE_COLOR = 110
    LINE_WIDTH = 111
    PEN_UP = 112
    PEN_DOWN = 113
    FILL_TRUE = 114
    FILL_FALSE = 115
    FILL_COLOR = 116
    BACKGROUND_COLOR = 117
    SAVE_POS = 118
    RESTORE_POS = 119
    RANDOM = 120
    CIRCLE = 121
