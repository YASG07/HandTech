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

#recibe un arbol de sintaxis abstracta (resultado de yacc.parse)
def analisis(asa):
    print(asa)
    if not asa:
        return
    
    nodo = asa[0]

    if nodo == 'programa':
        print(nodo)
        analisis(asa[1])
    elif nodo == 'objeto':
        print(nodo)
        analisis(asa[2])
    elif nodo == 'funcion':
        print(nodo)
        analisis(asa[2])
    elif nodo == 'bloque':
        print(nodo)
        for instruccion in asa[1]:
            analisis(instruccion)
    elif nodo == 'asignacion':
        print(nodo)
        tipoDato = asa[1]
        print(tipoDato)
        identificador = asa[2]
        print(identificador)
        valor = asa[3]
        print(valor)
        if identificador in tablaSimbolos:
            errores.append(f"Error: variable '{identificador}' ya existe.")
        else:
            if identificador == valor:
                errores.append(f"Errores: variable '{identificador}' ya existe")
                return
            else:
                tablaSimbolos[identificador] = tipoDato
        if type(valor) == str:
            if valor not in tablaSimbolos:
                errores.append(f"Errores: variable '{valor}' no existe")
            elif tipoDato != tablaSimbolos[valor]:
                errores.append(f"Errores: '{valor}' no puede ser convertido a '{tipoDato}'")
        elif type(valor).__name__ != tipoDato:
            errores.append(f"Errores: '{valor}' no puede ser convertido a '{tipoDato}'")
    elif nodo == 'inicialización':
        print(nodo)
        tipoDato = asa[1]
        print(tipoDato)
        identificador = asa[2]
        print(identificador)
        if identificador in tablaSimbolos:
            errores.append(f"Error: variable '{identificador}' ya existe.")
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
            errores.append(f"Error: variable '{identificador}' no existe.")
        if type(valor) == str:
            if valor not in tablaSimbolos:
                errores.append(f"Error: variable '{valor}' no existe.")
            elif tipoDato != tablaSimbolos[valor]:
                errores.append(f"Errores: '{valor}' no puede ser convertido a '{tipoDato}'")
        elif type(valor).__name__ != tipoDato:
            errores.append(f"Errores: '{valor}' no puede ser convertido a '{tipoDato}'")
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
   int t = t$
}
'''
resultado = analizar(src)
print(resultado)
#test(src)