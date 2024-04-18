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
#gramatica para método principal
def p_main(produccion):
    '''
    main : method run LPARENT RPARENT LKEY bloque RKEY
    '''
    print("main")

#bloque de código
def p_bloque(produccion):
    '''
    bloque : expression 
           | bloque expression
           | asignacion
           | bloque asignacion
           | bloque ciclo
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
               | LPARENT expression operadorL expression RPARENT
               | operacionL AND operacionL
               | NOT operacionL
    '''
    print("operaciones lógicas")

#instrucciones


#asignacion
def p_asignacion(produccion):
    '''
    asignacion : tipo ID ASSIGN expression FIN_DE_INSTRUCCION
               | tipo ID FIN_DE_INSTRUCCION
               | ID ASSIGN expression FIN_DE_INSTRUCCION
    '''
    print("asignación")

#tipos de dato
def p_tipoDato(proudccion):
    '''
    tipo : degree 
         | int 
         | float 
         | bool
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