#Analizador sintáctico para HandTech (.ht)

#imports
import ply.yacc as yacc
#import os
#import codecs

from lexico import tokens
from sys import stdin

precedence = (
    ('right','ASSIGN'),
    ('left','NE'),
    ('left', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LPARENT', 'RPARENT'),
)

#métodos para validar cada una de las gramaticas que componen el lenguaje
#gramática base
def p_programa(produccion):
    '''
    program : section
    '''
    print("programa")
    #produccion[0] = program(produccion[1], "program") #pendiente a terminar

#gramatica de expresión
def p_expresion(produccion):
    '''
    expression : ID
                |   NUMBER
                |   DECIMAL
                |   BOOL      
    '''
    print("expresión")

#gramatica para método principal
def p_run(produccion):
    '''
    section : method run LPARENT expression RPARENT LKEY section RKEY
    '''
    print("método principal")

#gramatica para métodos
def p_metodo(produccion):
    '''
    section : method ID LPARENT expression RPARENT
    '''
    print("metodo")

#gramatica para objetos
def p_objetos(produccion):
    '''
    section : mbm ID LKEY section RKEY
    '''
    print("objeto")

#gramatica para comentarios
def p_comentarios(produccion):
    '''
    expression : COMENTARIOS expression
                |   COMENTARIOS_MULTILINEA expression COMENTARIOS_MULTILINEA
    '''
    print("comentario")

#gramatica para declarar variables
def p_declararacion(produccion):
    '''
    declare : degree ID ASSIGN DECIMAL FIN_DE_INSTRUCCION
    '''
    print("declaración")

#gramatica de asignación
def p_asignar(produccion):
    '''
    expression : ID ASSIGN expression FIN_DE_INSTRUCCION 
    '''
    print("asignación")

#gramatica de operaciones aritmeticas
def p_operaciones(produccion):
    '''
    expression : expression PLUS expression
                |   expression MINUS expression
                |   expression TIMES expression
                |   expression DIVIDE expression
                |   ID INCRE
                |   ID DECRE 
    '''
    print("operaciones")

#gramatica de agrupacion
def p_agrupacion(produccion):
    '''
    expression : LPARENT expression RPARENT
                |   LKEY expression RKEY
                |   SBLKEY expression SBRKEY
    '''
    print("agrupacion")

#gramatica de operaciones logicas
def p_logicas(produccion):
    '''
    expression : expression LT expression
                |   expression GT expression
                |   expression LTE expression
                |   expression GTE expression
                |   expression NE expression
                |   LPARENT expression RPARENT LT LPARENT expression RPARENT
                |   LPARENT expression RPARENT GT LPARENT expression RPARENT
                |   LPARENT expression RPARENT GTE LPARENT expression RPARENT
                |   LPARENT expression RPARENT LTE LPARENT expression RPARENT
                |   LPARENT expression RPARENT NE LPARENT expression RPARENT
    '''
    print("logicas")

#gramatica para expresiones booleanas
def p_booleanos(produccion):
    '''
    expression : expression AND expression
                |   NOT expression
                |   LPARENT expression RPARENT AND LPARENT expression RPARENT
                |   NOT LPARENT expression RPARENT
    '''
    print("booleanos")

def p_error(produccion):
    if produccion:
        print(f"Error sintactico: '{produccion.value}', en línea '{produccion.lineno}'")
    else:
        print("Error sintactico: expresión indefinida")

#cargar código desde un archivo
file = open("test/test.ht")#abrir el archivo toma como base la dirección del programa ejecutandose
codigo = file.read()#cargar el contenido en una variable
file.close()#cierra el archivo

#instancia del analizador sintactico
parser = yacc.yacc()

#Evitar la impresión de advertencias de token no utilizado
yacc.errorlog = yacc.NullLogger()

#método para probar el código
def analisisSintactico(src):
    resultado = parser.parse(src)
    print(resultado)

analisisSintactico(codigo)

"""
código ejemplo para pruebas (esto funciona como comentarios multilinea en python)
archivo test.ht -> HandTech/src/analizadores/test
method run(){
   ;Aquí mandas a llamar los métodos que llegues a crear
   ;fng1 = 30$
   AgarrarSoltar()$
}

method AgarrarSoltar(){
   sensor sn = false$
   telefono tireloProfe = telefono$
   if(NOT sn) then{
      wrist.rotate(90)$ ;Cantidad de grados que rotará la muñeca
      wait(2000)$ ;Espera una cantidad de 2 segundos
      arm.mov(10)$ ;Cantidad de cm que se moverá la mano con respecto a X
      wait(2000)$
      hand.mov(tireloProfe.ancho)$ <- Cierra la mano en un valor de grados que indica el
                                                        parámetro del objeto ->
      sn = true$
   } else {
      hand.mov(-tireloProfe.ancho)$ ;Abre la mano
      wait(2000)$
      arm.mov(-10)$
      wait(2000)$
      wrist.rotate(-90)$  ;Cantidad de grados que rotará la muñeca en -X
      sn = false$
   }
}

mbm telefono {
         int ancho = 15$ ;Cantidad en cm del ancho del obj
         int alto = 27$ ;Cantidad en cm del alto del obj
} ;Objeto teléfono nos ayudará a establecer los límites de dicho objeto
"""