#Analizador sintáctico para HandTech (.ht)

#imports
import ply.yacc as yacc

from lexico import tokens

precedence = (
    ('right','ASSIGN'),
    ('left','NE'),
    ('left', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LPARENT', 'RPARENT'),
)

#métodos para validar cada una de las gramaticas que componen el lenguaje
#gramatica base
def p_programa(produccion):
    '''
    programa : main
             | objeto
             | main objeto
             | programa funcion
    '''
    print("programa fuente")
    
#gramatica para método principal
def p_main(produccion):
    '''
    main : method run LPARENT RPARENT LKEY bloque RKEY
    '''
    print("main")

#bloque de código
def p_bloque(produccion):
    '''
    bloque : instruccion 
           | bloque instruccion
           | asignacion
           | bloque asignacion
           | ciclo
           | bloque ciclo
           | condicion
           | bloque condicion
    '''
    print("bloque")
    
#expression
def p_expression(produccion):
    '''
    expression : ID 
                | NUMBER 
                | BOOL 
                | DECIMAL 
                | ID DOT ID
    '''
    print("expresión")

#operadores aritmeticas
def p_operadoresAritmeticos(produccion):
    '''
    operadorA : PLUS 
                | MINUS 
                | TIMES 
                | DIVIDE
    '''
    print("operadores aritmeticos")

#operadores logicas
def p_operadoresLogicos(produccion):
    '''
    operadorL : GT 
                | LT 
                | GTE 
                | LTE 
                | EQUALS 
                | NE
    '''
    print("operadores logicos")

#operaciones aritmeticas
def p_operacionesAritmeticas(produccion):
    '''
    operacionA : expression operadorA expression 
               | LPARENT operacionA RPARENT
               | ID INCRE
               | ID DECRE
    '''
    print("operacion anchorage (aritmetica)")

#operaciones lógicas
def p_operacionesLogicas(produccion):
    '''
    operacionL : expression operadorL expression
               | LPARENT operacionL RPARENT
               | operacionL AND operacionL
               | NOT operacionL
               | parte DOT is LPARENT up RPARENT
               | parte DOT is LPARENT down RPARENT
               | parte DOT is LPARENT block RPARENT
    '''
    print("operaciones lógicas")

#partes de la mano
def p_partesMano(produccion):
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
    print("parte de la mano")
    
#instrucciones
def p_instruccion(produccion):
    '''
    instruccion : parte DOT mov LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT mov LPARENT expression COMMA expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT force LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | wrist DOT rotate LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | wait LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT stop LPARENT RPARENT FIN_DE_INSTRUCCION
                | return FIN_DE_INSTRUCCION
                | return expression FIN_DE_INSTRUCCION 
    '''
    print("instruccion")

#asignacion
def p_asignacion(produccion):
    '''
    asignacion : tipo ID ASSIGN expression FIN_DE_INSTRUCCION
               | tipo ID FIN_DE_INSTRUCCION
               | ID ASSIGN expression FIN_DE_INSTRUCCION
               | bool ID ASSIGN false FIN_DE_INSTRUCCION
               | bool ID ASSIGN true FIN_DE_INSTRUCCION
               | ID ASSIGN false FIN_DE_INSTRUCCION
               | ID ASSIGN true FIN_DE_INSTRUCCION
    '''
    print("asignación")

#tipos de dato
def p_tipoDato(proudccion):
    '''
    tipo : degree 
         | int 
         | float 
         | bool
         | sensor
    '''
    print("tipo de dato")

#gramatica para ciclos
def p_ciclos(produccion):
    '''
    ciclo : while LPARENT operacionL RPARENT LKEY bloque RKEY
          | for LPARENT asignacion TWPOINT operacionL TWPOINT operacionA RPARENT LKEY bloque RKEY
          | for LPARENT asignacion TWPOINT operacionL TWPOINT RPARENT LKEY bloque RKEY
          | for LPARENT TWPOINT operacionL TWPOINT operacionA RPARENT LKEY bloque RKEY
          | for LPARENT TWPOINT operacionL TWPOINT RPARENT LKEY bloque RKEY
    '''
    print("ciclo")

#gramatica para condicionales
def p_condicion(produccion):
    '''
    condicion : if LPARENT operacionL RPARENT then LKEY bloque RKEY
              | if LPARENT operacionL RPARENT then bloque else LKEY bloque RKEY
    '''
    print("condición")

#gramatica para objetos
def p_objetos(produccion):
    '''
    objeto : mbm ID LKEY bloque RKEY
           | mbm ID LKEY bloque funcion RKEY
           | export ASSIGN objeto
    '''
    print("objetos (clases)")

#gramatica para metodos
def p_metodos(produccion):
    '''
    funcion : method ID LPARENT RPARENT LKEY bloque RKEY
            | method ID LPARENT tipo ID RPARENT LKEY bloque RKEY
    '''
    print("métodos")

#método para devolver errores
def p_error(produccion):
    if produccion:
        print(f"Error sintactico: '{produccion.value}', en línea '{produccion.lineno}'")
    else:
        print("Error sintactico: expresión indefinida")
#endregion métodos para gramaticas

#leer código desde un archivo
file = open("test/test.ht")#toma como base la dirección del programa ejecutandose
codigo = file.read()#cargar el contenido en una variable
file.close()

#instancia del analizador sintactico
parser = yacc.yacc()

#Evitar la impresión de advertencias de token no utilizado
yacc.errorlog = yacc.NullLogger()

#método para probar el código
def analisisSintactico(src):
    resultado = parser.parse(src)
    print(resultado)

analisisSintactico(codigo)