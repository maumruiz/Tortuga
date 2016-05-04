class SemanticCube:
    ''' Clase que se contiene el cubo semántico que se usa para los tipos de operación'''
    INT = 0
    FLOAT = 1
    STRING = 2
    BOOL = 3

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

    # El orden es: i f s b
    #          int                             float                          string                      boolean
    cube = [[[INT, FLOAT, None, None],   [FLOAT, FLOAT, None, None],  [None, None, None, None],   [None, None, None, None]], # Multiplicacion
            [[INT, FLOAT, None, None],   [FLOAT, FLOAT, None, None],  [None, None, None, None],   [None, None, None, None]], # Division
            [[INT, FLOAT, None, None],   [FLOAT, FLOAT, None, None],  [None, None, None, None],   [None, None, None, None]], # Sum
            [[INT, FLOAT, None, None],   [FLOAT, FLOAT, None, None],  [None, None, None, None],   [None, None, None, None]], # Substraction
            [[BOOL, BOOL, None, None],   [BOOL, BOOL, None, None],    [None, None, BOOL, None],   [None, None, None, None]], # Greater
            [[BOOL, BOOL, None, None],   [BOOL, BOOL, None, None],    [None, None, BOOL, None],   [None, None, None, None]], # Lesser
            [[BOOL, BOOL, None, None],   [BOOL, BOOL, None, None],    [None, None, BOOL, None],   [None, None, None, BOOL]], # Equal
            [[BOOL, BOOL, None, None],   [BOOL, BOOL, None, None],    [None, None, BOOL, None],   [None, None, None, BOOL]], # Not equal
            [[None, None, None, None],   [None, None, None, None],    [None, None, None, None],   [None, None, None, BOOL]], # AND
            [[None, None, None, None],   [None, None, None, None],    [None, None, None, None],   [None, None, None, BOOL]], # OR
            [[INT,  None, None, None],   [FLOAT, FLOAT, None, None],  [None, None, STRING, None], [None, None, None, BOOL]], # Assignment
            [[BOOL, BOOL, None, None],   [BOOL, BOOL, None, None],    [None, None, BOOL, None],   [None, None, None, None]], # MayorIgual
            [[BOOL, BOOL, None, None],   [BOOL, BOOL, None, None],    [None, None, BOOL, None],   [None, None, None, None]]] # MenorIgual

    # La función get_result_type recibe dos operandos y un codigo de operación.
    # Con respecto a esto busca en el cubo semántico el tipo del resultado de
    # esa operación
    def get_result_type(self, operand_1, operand_2, operation_code):
        return self.cube[operation_code][operand_1][operand_2]
