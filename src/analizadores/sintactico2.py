#Analizador sintáctico para HandTech (.ht)

#imports
import ply.yacc as yacc

from lexico import tokens

#Prioridad de operaciones
precedence = (
    ('right','ASSIGN'),
    ('right','EQUALS'),
    ('left','NE'),
    ('left', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LPARENT', 'RPARENT'),
)

#Reglas de produccion
def p_expression_bisop(p):
    '''expression : expression PLUS expression 
                | expression MINUS expression 
                | expression TIMES expression
                | expression DIVIDE expression
    '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_number(p):
    '''expression : NUMBER 
                  | DECIMAL'''
    p[0] = p[1]

def p_expression_parentheses(p):
    'expression : LPARENT expression RPARENT'
    p[0] = p[2]

def p_expression_final(p):
    'expression : expression FIN_DE_INSTRUCCION'
    p[0] = p[1]

def p_error(p):
    #print("Error de sintaxis en la entrada: '%s'" % p.value)
    #print("Error de sintaxis en la entrada '%s'" % p.value)
    if p:
        raise yacc.YaccError("Error sintactico de tipo {} en el valor {}".format(str(p.type), str(p.value)))
    else:
        raise yacc.YaccError("Error sintactico")

#construir el analizador sintactico
parser = yacc.yacc()

def prueba(input):
    return parser.parse(input)