#Analizador sintáctico para HandTech (.ht)

#imports
import ply.yacc as yacc

from lexico import tokens

'''precedence = (
    ('right','ASSIGN'),
    ('left','NE'),
    ('left', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LPARENT', 'RPARENT'),
)'''

#métodos para validar cada una de las gramaticas que componen el lenguaje
#gramatica base
def p_programa(prod):
    '''
    programa : main
             | objeto
             | main objeto
             | programa funcion
    '''
    if len(prod) == 3:
        prod[0] = ('program', prod[1], prod[2])
    else:
        prod[0] = ('programa', prod[1])
    
#gramatica para método principal
def p_main(prod):
    '''
    main : method run LPARENT RPARENT LKEY bloque RKEY
    '''
    prod[0] = ('main', prod[6])

#bloque de código
def p_bloque(prod):
    '''
    bloque : instruccion 
           | bloque instruccion
           | asignacion
           | bloque asignacion
           | ciclo
           | bloque ciclo
           | condicion
           | bloque condicion
           | llamada
           | bloque llamada
    '''
    if len(prod) == 3:
        prod[0] = ('bloque', prod[1], prod[2])
    else:
        prod[0] = prod[1]
    
#expression
def p_expression(prod):
    '''
    expression : ID 
                | NUMBER 
                | BOOL 
                | DECIMAL 
                | ID DOT ID
                | true
                | false
    '''
    if len(prod) == 4:
        prod[0] = ('expression', prod[1], prod[3])
    else:
        prod[0] = prod [1]

#operadores aritmeticas
def p_operadoresAritmeticos(prod):
    '''
    operadorA : PLUS 
                | MINUS 
                | TIMES 
                | DIVIDE
    '''
    prod[0] = prod [1]

#operadores logicas
def p_operadoresLogicos(prod):
    '''
    operadorL : GT 
                | LT 
                | GTE 
                | LTE 
                | EQUALS 
                | NE
    '''
    prod[0] = prod [1]

#operaciones aritmeticas
def p_operacionesAritmeticas(prod):
    '''
    operacionA : expression operadorA expression 
               | LPARENT operacionA RPARENT
               | ID INCRE 
               | ID DECRE
    '''
    if len(prod) == 4:
        if prod[1] == '(':
            prod[0] = ('grupo', prod[2])
        else:
            prod[0] = ('operacionA', prod[1], prod[2], prod[3])
    else:
        prod[0] = prod[1]

#operaciones lógicas
def p_operacionesLogicas(prod):
    '''
    operacionL : expression operadorL expression
               | LPARENT operacionL RPARENT
               | operacionL AND operacionL
               | ID AND ID 
               | NOT operacionL
               | NOT ID
               | parte DOT is LPARENT up RPARENT
               | parte DOT is LPARENT down RPARENT
               | parte DOT is LPARENT block RPARENT
    '''
    if len(prod) == 4:
        if prod[1] == '(':
            prod[0] = ('grupo', prod[2])
        elif prod[2] == 'AND':
            prod[0] = ('operacionL_AND', prod[1], prod[3])
        else:
            prod[0] = ('operacionL', prod[1], prod[2], prod[3])
    elif len(prod) == 3:
        prod[0] = prod[2]

#partes de la mano
def p_partesMano(prod):
    '''
    parte : fng1
          | fng2
          | fng3
          | fng4
          | fng5
          | arm
          | hand
          | linkage
    '''
    prod[0] = prod [1]
    
#instrucciones
def p_instruccion(prod):
    '''
    instruccion : parte DOT mov LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT mov LPARENT expression COMMA expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT force LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | wrist DOT rotate LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | wait LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT stop LPARENT RPARENT FIN_DE_INSTRUCCION
                | return FIN_DE_INSTRUCCION
                | return expression FIN_DE_INSTRUCCION 
                | import ID FIN_DE_INSTRUCCION
    '''
    if len(prod) == 8:
        prod[0] = prod[5]
    elif prod[1] == 'wait':
        prod[0] = prod[3]
    elif len(prod) == 4:
        prod[0] = prod[2]
    elif len(prod) == 10:
        prod[0] = ('instruccion_mov', prod[5], prod[7])

#llamada de funciones
def p_llamada(prod):
    '''
    llamada : ID LPARENT RPARENT FIN_DE_INSTRUCCION
            | ID DOT ID LPARENT RPARENT FIN_DE_INSTRUCCION
            | ID LPARENT expression RPARENT FIN_DE_INSTRUCCION
            | ID DOT ID LPARENT expression RPARENT FIN_DE_INSTRUCCION
    '''
    if len(prod) == 5:
        prod[0] = prod[1]
    elif len(prod) == 7 | len(prod) == 6:
        prod[0] = ('llamada_punto', prod[1], prod[3])
    elif len(prod) == 8:
        prod[0] = ('llamada_pp', prod[1], prod[3], prod[5])

#asignacion
def p_asignacion(prod):
    '''
    asignacion : tipo ID ASSIGN expression FIN_DE_INSTRUCCION
               | tipo ID FIN_DE_INSTRUCCION
               | ID ASSIGN expression FIN_DE_INSTRUCCION
    '''
    if len(prod) == 6:
        prod[0] = ('asignacion_tipo', prod[1], prod[2], prod[4])
    elif len(prod) == 5:
        prod[0] = ('asignacion_notipo', prod[1], prod[3])
    elif len(prod) == 4:
        prod[0] = ('inicialización', prod[1], prod[2])

#tipos de dato
def p_tipoDato(prod):
    '''
    tipo : degree 
         | int 
         | float 
         | bool
         | sensor
         | ID
    '''
    prod[0] = prod [1]

#gramatica auxiliar. Símbolo de apoyo para ciclos
def p_aux(prod):
    '''
    aux : tipo ID
        | tipo ID ASSIGN expression
    '''
    if len(prod) == 3:
        prod[0] = prod[2]
    else:
        prod[0] = ('aux', prod[2], prod[4])

#gramatica para ciclos
def p_ciclos(prod):
    '''
    ciclo : while LPARENT operacionL RPARENT LKEY bloque RKEY
          | for LPARENT aux TWPOINT operacionL TWPOINT operacionA RPARENT LKEY bloque RKEY
          | for LPARENT aux TWPOINT operacionL TWPOINT RPARENT LKEY bloque RKEY
          | for LPARENT TWPOINT operacionL TWPOINT operacionA RPARENT LKEY bloque RKEY
          | for LPARENT TWPOINT operacionL TWPOINT RPARENT LKEY bloque RKEY
    '''
    if prod[1] == 'while':
        prod[0] = ('ciclo_while', prod[3], prod[6])
    elif len(prod) == 12:
        prod[0] = ('ciclo_for', prod[3], prod[5], prod[7], prod[10])
    elif len(prod) == 11:
        if prod[3] == ':':
            prod[0] = ('ciclo_for1', prod[4], prod[6], prod[9])
        else:
            prod[0] = ('ciclo_for2', prod[3], prod[5], prod[9])
    elif len(prod) == 10:
        prod[0] = ('ciclo_for3', prod[4], prod[8])

#gramatica para condicionales
def p_condicion(prod):
    '''
    condicion : if LPARENT operacionL RPARENT then LKEY bloque RKEY
              | if LPARENT operacionL RPARENT then bloque else LKEY bloque RKEY
    '''
    if len(prod) == 9:
        prod[0] = ('condicion_then', prod[3], prod[7])
    else:
        prod[0] = ('condicion_else', prod[3], prod[7], prod[10])

#gramatica para objetos
def p_objetos(prod):
    '''
    objeto : mbm ID LKEY bloque RKEY
           | mbm ID LKEY bloque funcion RKEY
           | export ASSIGN objeto
    '''
    if len(prod) == 6:
        prod[0] = ('objeto', prod[2], prod[4])
    elif len(prod) == 7:
        prod[0] = ('objeto_funcion', prod[2], prod[4], prod[5])
    elif len(prod) == 4:
        prod[0] = ('objeto_export', prod[3])

#gramatica para metodos
def p_metodos(prod):
    '''
    funcion : method ID LPARENT RPARENT LKEY bloque RKEY
            | method ID LPARENT tipo ID RPARENT LKEY bloque RKEY
    '''
    if len(prod) == 8:
        prod[0] = ('funcion', prod[2], prod[6])
    else:
        prod[0] = NodoMethod(prod[2], prod[4], prod[5], prod[8])

#método para devolver errores
def p_error(prod):
    if prod:
        print(f"Error sintactico: '{prod.value}', en línea '{prod.lineno}'")
    else:
        print("Error sintactico: expresión indefinida")
#endregion métodos para gramaticas

#arboles binarios
class NodoMethod:
    #constructor de la clase
    def __init__(self, idMethod, tipo, idParam, bloque):
        self.idMethod = idMethod
        self.tipo = tipo
        self.idParam = idParam 
        self.bloque = bloque
    #toString 
    def __str__(self):
        return f"method {self.idMethod} {self.tipo} {self.idParam} {{\n{self.bloque}\n}}"
#endregion arboles de la barranca (binarios)

#Método para imprimir en consola el árbol sintactico
def print_tree(nodo, nivel=0):
    if isinstance(nodo, tuple):
        print("  " * nivel + nodo[0])
        for child in nodo[1:]:
            print_tree(child, nivel + 1)
    elif isinstance(nodo, NodoMethod):
        print("  " * nivel + "method")
        print_tree(nodo.variable, nivel + 1)
        print_tree(nodo.inicio, nivel + 1)
        print_tree(nodo.condicion, nivel + 1)
        print_tree(nodo.actualizacion, nivel + 1)
        print_tree(nodo.cuerpo, nivel + 1)
    else:
        print("  " * nivel + str(nodo))

#leer código desde un archivo

#file = open("test/test.ht")#toma como base la dirección del programa ejecutandose
#codigo = file.read()#cargar el contenido en una variable
#file.close()

#instancia del analizador sintactico
parser = yacc.yacc()

#Evitar la impresión de advertencias de token no utilizado
yacc.errorlog = yacc.NullLogger()

#método para probar el código
def analisisSintactico(src):
    resultado = parser.parse(src)
    print_tree(resultado)

#analisisSintactico(codigo)

def llamaSintactico(input):
    return parser.parse(input)
