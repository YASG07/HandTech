#Analizador semántico para HandTech (.ht)

#imports
import sintactico
from lexico import tokens,obtener_errores_lexicos

#variable tablaSimbolos y lista de errores
tablaSimbolos = {}
errores = []

# manejo de errores
def agregar_error_semantico(id,error_type,error_description,value,line,column):
    errores.append({
        'Indice': id,
        'Tipo': error_type,
        'Descripcion': error_description,
        'Valor': str(value),
        'Linea': line,
        'Columna': column,
    })#agrega un error a la lista de errores

def obtener_errores_semanticos():
    global errores
    return errores #devuelve los errores encontrados

def find_column(input,token,n):
    last_cr = input.rfind('\n',0,token.lexpos(n))
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos(n) - last_cr)
    if column == 0:
        return 1
    return column #devuele la columna donde se encontró el error

def reiniciar_analizador_semantico(lexer):
    destructor()
    lexer.lineno = 1
    lexer.lexpos = 0
#endregion manejo de errores

#metodo para limpiar ambos parametros
def destructor():
    tablaSimbolos.clear()
    errores.clear()
    global longitud_asa
    global fase
    global asaCompleto
    longitud_asa = 0
    fase = 1
    asaCompleto = []

#variables de control de lectura de asa
longitud_asa = 0
fase = 1
asaCompleto = []
#recibe un arbol de sintaxis abstracta (resultado de yacc.parse)
def analisis(asa):
    print(asa)
    if not asa:
        return #cancela la operación si no recibe un asa (arbol de sintaxis abstracta)
    
    nodo = asa[0] #recupera el nombre del nodo

    if nodo == 'programa':
        print(nodo)
        global asaCompleto #convierte la variable en una global
        asaCompleto = asa #guarda el asa completo
        global longitud_asa
        longitud_asa = len(asa) #guarda la longitud del asa completo
        global fase
        analisis(asa[1]) #manda a ejecutar el método con el bloque como parametro
    elif nodo == 'objeto':
        print(nodo)
        analisis(asa[2]) #manda a ejecutar el método con el bloque como parametro
    elif nodo == 'funcion':
        print(nodo)
        analisis(asa[2]) #manda a ejecutar el método con el bloque como parametro
    elif nodo == 'bloque':
        print(nodo)
        for instruccion in asa[1]:
            analisis(instruccion) #ejcuta el método para analizar cada instrucción del bloque
        fase += 1 
        if fase < longitud_asa: 
            analisis(asaCompleto[fase]) #avanza al siguiente bloque si la fase no esta fuera de rango
    elif nodo == 'asignacion':
        print(nodo)
        tipoDato = asa[1]
        print(tipoDato)
        identificador = asa[2]
        print(identificador)
        valor = asa[3]
        print(valor)
        if identificador in tablaSimbolos:
            #agregar_error_semantico(15,'Semántico',"variable '{identificador}' ya existe.",identificador,)
            errores.append(f"Error Semántico: variable '{identificador}' ya existe.")
        else:
            if identificador == valor:
                #agregar_error_semantico(15,'Semántico',"variable '{identificador}' ya existe.",identificador,)
                errores.append(f"Error Semántico: variable '{identificador}' ya existe")
                return
            else:
                tablaSimbolos[identificador] = tipoDato
        if type(valor) == str:
            if valor not in tablaSimbolos:
                #agregar_error_semantico(16,'Semántico',"variable '{valor}' no existe.",valor,)
                errores.append(f"Error Semántico: variable '{valor}' no existe")
            elif tipoDato != tablaSimbolos[valor]:
                #agregar_error_semantico(17,'Semántico',"'{valor}' no puede ser convertido a '{tipoDato}'",valor,)
                errores.append(f"Error Semántico: '{valor}' no puede ser convertido a '{tipoDato}'")
        elif type(valor).__name__ != tipoDato:
            errores.append(f"Error Semántico: '{valor}' no puede ser convertido a '{tipoDato}'")
    elif nodo == 'inicialización':
        print(nodo)
        tipoDato = asa[1]
        print(tipoDato)
        identificador = asa[2]
        print(identificador)
        if identificador in tablaSimbolos:
            #agregar_error_semantico(15,'Semántico',"variable '{identificador}' ya existe.",identificador,)
            errores.append(f"Error Semántico: variable '{identificador}' ya existe.")
        else:
            tablaSimbolos[identificador] = tipoDato
    elif nodo == 'asignacion_noTipo':
        print(nodo)
        identificador = asa[1]
        print(identificador)
        valor = asa[2]
        print(valor)
        tipoDato = tablaSimbolos[identificador]
        print(tipoDato)
        if identificador not in tablaSimbolos:
            #agregar_error_semantico(16,'Semántico',"variable '{identificador}' no existe.",identificador,)
            errores.append(f"Error Semántico: variable '{identificador}' no existe.")
        if type(valor) == str:
            if valor not in tablaSimbolos:
                #agregar_error_semantico(16,'Semántico',"variable '{identificador}' no existe.",identificador,)
                errores.append(f"Error Semántico: variable '{valor}' no existe.")
            elif tipoDato != tablaSimbolos[valor]:
                errores.append(f"Error Semántico: '{valor}' no puede ser convertido a '{tipoDato}'")
        elif type(valor).__name__ != tipoDato:
            errores.append(f"Error Semántico: '{valor}' no puede ser convertido a '{tipoDato}'")
    elif nodo == 'operacion':
        print(nodo)
        izq = asa[1]
        print(izq)
        der = asa[3]
        print(der)
        analisis(izq)
        analisis(der)
    elif nodo == 'grupo':
        print(nodo)
        analisis(asa[1])
     
def analizar(src):
    destructor()
    asa = sintactico.parser.parse(src)
    analisis(asa)
    print(tablaSimbolos)
    if errores:
        return "Errores semánticos detectados en:\n" + "\n".join(errores)
    return "Análisis semántico completado sin errores."

def test(src):
    print(sintactico.parser.parse(src))

src = '''
method run(){
   int t = 0$
   int b = 5.15$
   t=a$
   int t$
}
mbm o {
    ;int t = 0$
}

method abc (){
    ;int a = 0$
}
method odb (){
    ;int a = 0$
}
'''
#resultado = analizar(src)
# print(resultado)
# test(src)