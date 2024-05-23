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
def p_programa(prod):
    '''
    programa : main
             | objeto
             | main objeto
             | objeto main
             | programa funcion
             | funcion programa
    '''
    if len(prod) == 3:
        prod[0] = ('programa', prod[1], prod[2])
    else:
        prod[0] = ('programa', prod[1])
    
#gramatica para método principal
def p_main(prod):
    '''
    main : method run LPARENT RPARENT bloque
    '''
    prod[0] = prod[5]

#auxiliar para gramatica de bloque
def p_auxBloque(prod):
    '''
    auxB : instruccion
         | asignacion
         | ciclo
         | condicion
         | llamada
    '''
    prod[0] = prod[1]

#lista de instrucciones
def p_listaInstrucciones(prod):
    '''
    listaInstruccion : listaInstruccion auxB 
                     | auxB
    '''
    if len(prod) == 3:
        prod[0] = prod[1] + [prod[2]]
    else:
        prod[0] = [prod[1]]

#bloque de código
def p_bloque(prod):
    '''
    bloque : LKEY listaInstruccion RKEY 
    '''
    prod[0] = ('bloque', prod[2])

#expression
def p_expression(prod):
    '''
    expression : valor
               | ID DOT ID
               | operacionA
               | operacionL
    '''
    if len(prod) == 4:
        prod[0] = ('expression', prod[1], prod[3])
    else:
        prod[0] = prod[1]

#valores (auxiliar para expression)
def p_valor(prod):
    '''
    valor : ID 
          | NUMBER 
          | BOOL 
          | DECIMAL
          | true
          | false
    '''
    prod[0] = prod[1]

#operadores aritmeticas
def p_operadoresAritmeticos(prod):
    '''
    operadorA : PLUS 
                | MINUS 
                | TIMES 
                | DIVIDE
    '''
    prod[0] = prod[1]

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
    prod[0] = prod[1]

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
            prod[0] = ('operacion', prod[1], prod[2], prod[3])
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
            prod[0] = ('operacion', prod[1], prod[2], prod[3])
    elif len(prod) == 3:
        prod[0] = ('Operacion_NOT', prod[2])

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
        prod[0] = ('llamada4', prod[1], prod[3], prod[5])

#asignacion
def p_asignacion(prod):
    '''
    asignacion : tipo ID ASSIGN expression FIN_DE_INSTRUCCION
               | tipo ID FIN_DE_INSTRUCCION
               | ID ASSIGN expression FIN_DE_INSTRUCCION
    '''
    if len(prod) == 6:
        prod[0] = ('asignacion', prod[1], prod[2], prod[4])
    elif len(prod) == 5:
        prod[0] = ('asignacion_noTipo', prod[1], prod[3])
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
    prod[0] = prod[1]

#gramatica auxiliar. Símbolo de apoyo para ciclos
def p_aux(prod):
    '''
    aux : tipo ID
        | tipo ID ASSIGN expression
    '''
    if len(prod) == 3:
        prod[0] = prod[2]
    else:
        prod[0] = (prod[2], prod[4])

#gramatica para ciclos
def p_ciclos(prod):
    '''
    ciclo : while LPARENT operacionL RPARENT bloque 
          | for LPARENT aux TWPOINT operacionL TWPOINT operacionA RPARENT bloque 
          | for LPARENT aux TWPOINT operacionL TWPOINT RPARENT bloque 
          | for LPARENT TWPOINT operacionL TWPOINT operacionA RPARENT bloque 
          | for LPARENT TWPOINT operacionL TWPOINT RPARENT bloque 
    '''
    if prod[1] == 'while':
        prod[0] = ('ciclo_while', prod[3], prod[5])
    elif len(prod) == 10:
        prod[0] = ('ciclo_for1', prod[3], prod[5], prod[7], prod[9])
    elif len(prod) == 9:
        if prod[3] == ':':
            prod[0] = ('ciclo_for2', prod[4], prod[6], prod[8])
        else:
            prod[0] = ('ciclo_for3', prod[3], prod[5], prod[8])
    elif len(prod) == 8:
        prod[0] = ('ciclo_for4', prod[4], prod[7])

#gramatica para condicionales
def p_condicion(prod):
    '''
    condicion : if LPARENT operacionL RPARENT then bloque 
              | if LPARENT operacionL RPARENT then bloque else bloque 
    '''
    if len(prod) == 7:
        prod[0] = ('condicion_then', prod[3], prod[6])
    else:
        prod[0] = ('condicion_else', prod[3], prod[6], prod[8])

#gramatica para objetos
def p_objetos(prod):
    '''
    objeto : mbm ID bloque
           | export ASSIGN objeto FIN_DE_INSTRUCCION
    '''
    if len(prod) == 4:
        prod[0] = ('objeto', prod[2], prod[3])
    else:
        prod[0] = ('exportacion', prod[3])

#gramatica para metodos
def p_metodos(prod):
    '''
    funcion : method ID LPARENT RPARENT bloque 
            | method ID LPARENT tipo ID RPARENT bloque 
    '''
    if len(prod) == 6:
        prod[0] = ('funcion', prod[2], prod[5])
    else:
        prod[0] = ('funcion_parametrizada', prod[2], prod[4], prod[5], prod[7])

#gramaticas para el manejo de errores
#error en la definicón del programa
def p_errorPrograma1(prod):
    '''
    programa : error
             | error main
    '''
    #agregar error sintactico: estructura incorrecta prod[1] 1 es la posicion del simbolo error
    prod[0] = "Error al cargar el programa"

def p_errorPrograma2(prod):
    '''
    programa : main error
    '''
    #agregar error sintactico: estructura incorrecta después de la función principal
    prod[0] = "Error al cargar el programa"
def p_errorPrograma3(prod):
    '''
    programa : main error objeto
             | objeto error main
    '''
    #agregar error sintactico: estructura incorrecta entre la función principal y la declaración de objeto
    prod[0] = "Error al cargar el programa"
#endregion: error en la definicón del programa
#error al definir el método principal (run)
def p_errorMain1(prod):
    '''
    main : error run LPARENT RPARENT bloque
    '''
    #agregar error sintactico: Falta la palabra method al inicio
    prod[0] = "Error al construir la función principal"
def p_errorMain2(prod):
    '''
    main : method error LPARENT RPARENT bloque
    '''
    #agregar error sintactico: Falta la palabra run antes de ()
    prod[0] = "Error al construir la función principal"
def p_errorMain3(prod):
    '''
    main : method run error RPARENT bloque
    '''
    #agregar error sintactico: Falta parentesis de incio (
    prod[0] = "Error al construir la función principal"
def p_errorMain4(prod):
    '''
    main : method run LPARENT error bloque
    '''
    #agregar error sintactico: Falta parentesis de fin )
    prod[0] = "Error al construir la función principal"
def p_errorMain5(prod):
    '''
    main : method run LPARENT RPARENT error
    '''
    #agregar error sintactico: No se pudo construir el bloque
    prod[0] = "Error al construir la función principal"

#endregion: error al definir el método principal (run) 

#error al definir un objeto
def p_errorObjeto1(prod):
    '''
    objeto : error ID bloque
    '''
    #agregar error sintactico: Falta la palabra mbm
    prod[0] = "Error al construir un objeto"
def p_errorObjeto2(prod):
    '''
    objeto : mbm error bloque
    '''
    #agregar error sintactico: Se espera un identificador después de mbm
    prod[0] = "Error al construir un objeto"
def p_errorObjeto3(prod):
    '''
    objeto : mbm ID error
    '''
    #agregar error sintactico: No se pudo construir el bloque 
    prod[0] = "Error al construir un objeto"

def p_errorObjeto4(prod):
    '''
    objeto : error ASSIGN objeto FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Falta la palabra export
    prod[0] = "Error al construir un objeto"
def p_errorObjeto5(prod):
    '''
    objeto : export error objeto FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Se espera '=' cerca de export
    prod[0] = "Error al construir un objeto"
def p_errorObjeto6(prod):
    '''
    objeto : export ASSIGN error FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Objeto no definido
    prod[0] = "Error al construir un objeto"
def p_errorObjeto7(prod):
    '''
    objeto : export ASSIGN objeto error
    '''
    #agregar error sintactico: Oh! sentinela ($) como te extraño
    prod[0] = "Error al construir un objeto"

#endregion: error al definir un objeto 

#error al definir una función
def p_errorFuncion1(prod):
    '''
    funcion : error ID LPARENT RPARENT bloque 
            | error ID LPARENT tipo ID RPARENT bloque 
    '''
    #agregar error sintactico: Falta la palabra method al inicio
    prod[0] = "Error al construir una función"
def p_errorFuncion2(prod):
    '''
    funcion : method error LPARENT RPARENT bloque 
            | method error LPARENT tipo ID RPARENT bloque 
    '''
    #agregar error sintactico: Se espera un identificador valido después de 'method'
    prod[0] = "Error al construir una función"
def p_errorFuncion3(prod):
    '''
    funcion : method ID error RPARENT bloque 
            | method ID error tipo ID RPARENT bloque  
    '''
    #agregar error sintactico: Falta parentesis de inicio (
    prod[0] = "Error al construir una función"
def p_errorFuncion4(prod):
    '''
    funcion : method ID LPARENT error bloque 
            | method ID LPARENT tipo ID error bloque  
    '''
    #agregar error sintactico: Falta parentesis de fin )
    prod[0] = "Error al construir una función"
def p_errorFuncion5(prod):
    '''
    funcion : method ID LPARENT RPARENT error 
            | method ID LPARENT tipo ID RPARENT error  
    '''
    #agregar error sintactico: Imposible construir el bloque
    prod[0] = "Error al construir una función"
def p_errorFuncion6(prod):
    '''
    funcion : method ID LPARENT error ID RPARENT bloque   
    '''
    #agregar error sintactico: Se espera un tipo de dato entre parentesis
    prod[0] = "Error al construir una función"
def p_errorFuncion7(prod):
    '''
    funcion : method ID LPARENT tipo error RPARENT bloque   
    '''
    #agregar error sintactico: Se espera un identificador válido entre parentesis
    prod[0] = "Error al construir una función"

#endregion: error al definir una función
#error al definir un bloque de código
def p_errorBloque1(prod):
    '''
    bloque : error listaInstruccion RKEY
    '''
    #agregar error sintactico: falta llave de inicio {
    prod[0] = "Error en el bloque de código"
def p_errorBloque2(prod):
    '''
    bloque : LKEY listaInstruccion error
    '''
    #agregar error sintactico: falta llave de fin }
    prod[0] = "Error en el bloque de código"
def p_errorBloque3(prod):
    '''
    bloque : LKEY error RKEY
    '''
    #agregar error sintactico: Construcción del bloque incorrecta
    prod[0] = "Error en el bloque de código"
def p_errorBloque4(prod):
    '''
    bloque : LKEY error 
    '''
    #agregar error sintactico: Falta llave de fin }
    prod[0] = "Error en el bloque de código"
def p_errorBloque5(prod):
    '''
    bloque : error RKEY 
    '''
    #agregar error sintactico: Falta llave de inicio {
    prod[0] = "Error en el bloque de código"
#endregion: error al definir un bloque de código

#error en instrucciones
def p_errorInstruccion1(prod):
    '''
    instruccion : error DOT mov LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | error DOT mov LPARENT expression COMMA expression RPARENT FIN_DE_INSTRUCCION
                | error DOT force LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | error DOT stop LPARENT RPARENT FIN_DE_INSTRUCCION
                | error DOT rotate LPARENT expression RPARENT FIN_DE_INSTRUCCION
    '''
                
    #agregar error sintactico: Caracter incorrecto antes del punto, se espera fng1, wrist, etc.
    prod[0] = "Error al escribir la instrucción"
def p_errorInstruccion2(prod):
    '''
    instruccion : parte DOT error LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT error LPARENT expression COMMA expression RPARENT FIN_DE_INSTRUCCION
                | wrist DOT error LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT error LPARENT RPARENT FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Caracter incorrecto despues del punto, se espera mov, stop, etc.
    prod[0] = "Error al escribir la instrucción"
def p_errorInstruccion3(prod):
    '''
    instruccion : parte error mov LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | parte error mov LPARENT expression COMMA expression RPARENT FIN_DE_INSTRUCCION
                | parte error force LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | wrist error rotate LPARENT expression RPARENT FIN_DE_INSTRUCCION
                | parte error stop LPARENT RPARENT FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: A donde se habrá ido el punto
    prod[0] = "Error al escribir la instrucción"
def p_errorInstruccion4(prod):
    '''
    instruccion : parte DOT mov LPARENT expression RPARENT error
                | parte DOT mov LPARENT expression COMMA expression RPARENT error
                | parte DOT force LPARENT expression RPARENT error
                | wrist DOT rotate LPARENT expression RPARENT error
                | wait LPARENT expression RPARENT error
                | parte DOT stop LPARENT RPARENT error
                | return error
                | return expression error 
                | import ID error
    '''
    #consulte la gramatica original para consultar la posición exacta del error
    #agregar error sintactico: Me pregunto que será del sentinela ($)
    prod[0] = "Error al escribir la instrucción"
def p_errorInstruccion5(prod):
    '''
    instruccion : parte DOT mov error expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT mov error expression COMMA expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT force error expression RPARENT FIN_DE_INSTRUCCION
                | wrist DOT rotate error expression RPARENT FIN_DE_INSTRUCCION
                | wait error expression RPARENT FIN_DE_INSTRUCCION
                | parte DOT stop error RPARENT FIN_DE_INSTRUCCION
    '''
    #consulte la gramatica original para consultar la posición exacta del error
    #agregar error sintactico: Falta parentesis de inicio (
    prod[0] = "Error al escribir la instrucción"
def p_errorInstruccion6(prod):
    '''
    instruccion : parte DOT mov LPARENT expression error FIN_DE_INSTRUCCION
                | parte DOT mov LPARENT expression COMMA expression error FIN_DE_INSTRUCCION
                | parte DOT force LPARENT expression error FIN_DE_INSTRUCCION
                | wrist DOT rotate LPARENT expression error FIN_DE_INSTRUCCION
                | wait LPARENT expression error FIN_DE_INSTRUCCION
                | parte DOT stop LPARENT error FIN_DE_INSTRUCCION
    '''
    #consulte la gramatica original para consultar la posición exacta del error
    #agregar error sintactico: Falta parentesis de fin )
    prod[0] = "Error al escribir la instrucción"
def p_errorInstruccion7(prod):
    '''
    instruccion : parte DOT mov LPARENT error RPARENT FIN_DE_INSTRUCCION
                | parte DOT mov LPARENT error COMMA error RPARENT FIN_DE_INSTRUCCION
                | parte DOT force LPARENT error RPARENT FIN_DE_INSTRUCCION
                | wrist DOT rotate LPARENT error RPARENT FIN_DE_INSTRUCCION
                | wait LPARENT error RPARENT FIN_DE_INSTRUCCION
    '''
    #consulte la gramatica original para consultar la posición exacta del error
    #agregar error sintactico: Se espera un valor adecuado entre parentesis
    prod[0] = "Error al escribir la instrucción"
def p_errorInstruccion8(prod):
    '''
    instruccion : return error FIN_DE_INSTRUCCION 
                | import error FIN_DE_INSTRUCCION
    '''
    #consulte la gramatica original para consultar la posición exacta del error
    #agregar error sintactico: Valor incorrecto cerca de import/return
    prod[0] = "Error al escribir la instrucción"
def p_errorInstruccion9(prod):
    '''
    instruccion : error LPARENT expression RPARENT FIN_DE_INSTRUCCION
    '''
    #consulte la gramatica original para consultar la posición exacta del error
    #agregar error sintactico: Se espera 'wait' cerca de ()
    prod[0] = "Error al escribir la instrucción"
    
#endregion: error en instrucciones

#error en asignacion
def p_errorAsginacion1(prod):
    '''
    asignacion : tipo ID ASSIGN expression error
               | tipo ID error
               | ID ASSIGN expression error
    '''
    #agregar error sintactico: Vuelve sentinela ($) nos haces falta
    prod[0] = "Error al escribir una declaración"
def p_errorAsginacion2(prod):
    '''
    asignacion : error ID ASSIGN expression FIN_DE_INSTRUCCION
               | error ID FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Tipo dato requerido
    prod[0] = "Error al escribir una declaración"
def p_errorAsginacion3(prod):
    '''
    asignacion : tipo error ASSIGN expression FIN_DE_INSTRUCCION
               | tipo error FIN_DE_INSTRUCCION
               | error ASSIGN expression FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Escriba un identificador válido
    prod[0] = "Error al escribir una declaración"
def p_errorAsginacion4(prod):
    '''
    asignacion : tipo ID error expression FIN_DE_INSTRUCCION
               | ID error expression FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Falta '=' cerca de identificador
    prod[0] = "Error al escribir una declaración"
def p_errorAsginacion5(prod):
    '''
    asignacion : tipo ID ASSIGN error FIN_DE_INSTRUCCION
               | ID ASSIGN error FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Falta el valor correspondiente a la variable
    prod[0] = "Error al escribir una declaración"

#endregion: error en asignacion

#error en llamada
def p_errorLlamada1(prod):
    '''
    llamada : ID LPARENT RPARENT error
            | ID DOT ID LPARENT RPARENT error
            | ID LPARENT expression RPARENT error
            | ID DOT ID LPARENT expression RPARENT error
    '''
    #agregar error sintactico: Quisiera, que me hiceras mucha falta$
    prod[0] = "Error al escribir una instruccion"
def p_errorLlamada2(prod):
    '''
    llamada : error LPARENT RPARENT FIN_DE_INSTRUCCION
            | error DOT ID LPARENT RPARENT FIN_DE_INSTRUCCION
            | error LPARENT expression RPARENT FIN_DE_INSTRUCCION
            | error DOT ID LPARENT expression RPARENT FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Falta un identificador válido al incio
    prod[0] = "Error al escribir una instruccion"
def p_errorLlamada3(prod):
    '''
    llamada : ID error ID LPARENT RPARENT FIN_DE_INSTRUCCION
            | ID error ID LPARENT expression RPARENT FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Se espera un punto entre identificadores
    prod[0] = "Error al escribir una instruccion"
def p_errorLlamada4(prod):
    '''
    llamada : ID DOT error LPARENT RPARENT FIN_DE_INSTRUCCION
            | ID DOT error LPARENT expression RPARENT FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Falta un identificador válido después del punto
    prod[0] = "Error al escribir una instruccion"
def p_errorLlamada5(prod):
    '''
    llamada : ID error RPARENT FIN_DE_INSTRUCCION
            | ID DOT ID error RPARENT FIN_DE_INSTRUCCION
            | ID error expression RPARENT FIN_DE_INSTRUCCION
            | ID DOT ID error expression RPARENT FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Falta parentesis de inicio (
    prod[0] = "Error al escribir una instruccion"
def p_errorLlamada6(prod):
    '''
    llamada : ID LPARENT error FIN_DE_INSTRUCCION
            | ID DOT ID LPARENT error FIN_DE_INSTRUCCION
            | ID LPARENT expression error FIN_DE_INSTRUCCION
            | ID DOT ID LPARENT expression error FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Falta parentesis de fin )
    prod[0] = "Error al escribir una instruccion"
def p_errorLlamada7(prod):
    '''
    llamada : ID LPARENT error RPARENT FIN_DE_INSTRUCCION
            | ID DOT ID LPARENT error RPARENT FIN_DE_INSTRUCCION
    '''
    #agregar error sintactico: Se espera un valor adecuado
    prod[0] = "Error al escribir una instruccion"

#endregion: error en llamada

#error en condición
def p_errorCondicion1(prod):
    '''
    condicion : error LPARENT operacionL RPARENT then bloque 
              | error LPARENT operacionL RPARENT then bloque else bloque
    '''
    #agregar error sintactico: La palabara 'if' debe ir al inicio
    prod[0] = "Error en la estructura de la condición"
def p_errorCondicion2(prod):
    '''
    condicion : if error operacionL RPARENT then bloque 
              | if error operacionL RPARENT then bloque else bloque
    '''
    #agregar error sintactico: Falta parentesis de incio (
    prod[0] = "Error en la estructura de la condición"
def p_errorCondicion3(prod):
    '''
    condicion : if LPARENT error RPARENT then bloque 
              | if LPARENT error RPARENT then bloque else bloque
    '''
    #agregar error sintactico: Se espera una operación lógica entre parentesis
    prod[0] = "Error en la estructura de la condición"
def p_errorCondicion4(prod):
    '''
    condicion : if LPARENT operacionL error then bloque 
              | if LPARENT operacionL error then bloque else bloque
    '''
    #agregar error sintactico: Falta parentesis de fin )
    prod[0] = "Error en la estructura de la condición"
def p_errorCondicion5(prod):
    '''
    condicion : if LPARENT operacionL RPARENT error bloque 
              | if LPARENT operacionL RPARENT error bloque else bloque
    '''
    #agregar error sintactico: La palabra 'then' debe ir antes del primer bloque
    prod[0] = "Error en la estructura de la condición"
def p_errorCondicion6(prod):
    '''
    condicion : if LPARENT operacionL RPARENT then error 
              | if LPARENT operacionL RPARENT then error else bloque
    '''
    #agregar error sintactico: Imposible construir el primer bloque
    prod[0] = "Error en la estructura de la condición"
def p_errorCondicion7(prod):
    '''
    condicion : if LPARENT operacionL RPARENT then bloque error bloque
    '''
    #agregar error sintactico: La palabra 'else' debe entre ambos bloques
    prod[0] = "Error en la estructura de la condición"
def p_errorCondicion8(prod):
    '''
    condicion : if LPARENT operacionL RPARENT then bloque else error
    '''
    #agregar error sintactico: imposible construir el segundo bloque
    prod[0] = "Error en la estructura de la condición"
    
#endregion: error en condición

#error en ciclos
def p_errorCiclos1(prod):
    '''
    ciclo : error LPARENT operacionL RPARENT bloque 
          | error LPARENT aux TWPOINT operacionL TWPOINT operacionA RPARENT bloque 
          | error LPARENT aux TWPOINT operacionL TWPOINT RPARENT bloque 
          | error LPARENT TWPOINT operacionL TWPOINT operacionA RPARENT bloque 
          | error LPARENT TWPOINT operacionL TWPOINT RPARENT bloque
    '''
    #agregar error sintactico: Se espera 'while/for' al inicio
    prod[0] = "Error en la estructura del ciclo"
def p_errorCiclos2(prod):
    '''
    ciclo : while error operacionL RPARENT bloque 
          | for error aux TWPOINT operacionL TWPOINT operacionA RPARENT bloque 
          | for error aux TWPOINT operacionL TWPOINT RPARENT bloque 
          | for error TWPOINT operacionL TWPOINT operacionA RPARENT bloque 
          | for error TWPOINT operacionL TWPOINT RPARENT bloque
    '''
    #agregar error sintactico: Falta parentesis de inicio (
    prod[0] = "Error en la estructura del ciclo"
def p_errorCiclos3(prod):
    '''
    ciclo : while LPARENT operacionL error bloque 
          | for LPARENT aux TWPOINT operacionL TWPOINT operacionA error bloque 
          | for LPARENT aux TWPOINT operacionL TWPOINT error bloque 
          | for LPARENT TWPOINT operacionL TWPOINT operacionA error bloque 
          | for LPARENT TWPOINT operacionL TWPOINT error bloque
    '''
    #agregar error sintactico: Falta parentesis de fin )
    prod[0] = "Error en la estructura del ciclo"

#endregion: error en ciclos

#método para devolver errores
def p_error(prod):
    if not prod:
        print('Programa invalido deber comenzar con el método principal o un objeto')
        #Aquí debe de ir el método de agregar errores
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
        print_tree(nodo.idMethod, nivel + 1)
        print_tree(nodo.tipo, nivel + 1)
        print_tree(nodo.idParam, nivel + 1)
        print_tree(nodo.bloque, nivel + 1)
    else:
        print("  " * nivel + str(nodo))

#instancia del analizador sintactico
parser = yacc.yacc()

#Evitar la impresión de advertencias de token no utilizado
yacc.errorlog = yacc.NullLogger()

#método para probar el código
def analisisSintactico(src):
    resultado = parser.parse(src)
    print(resultado)