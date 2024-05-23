#Analizador semántico para HandTech (.ht)

#imports
import sintactico
import lexico

#variable tablaSimbolos y lista de errores
tablaSimbolos = {}
errores = []

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
   int d$
   int t = d$
   t = 0$
}
'''
resultado = analizar(src)
print(resultado)
#test(src)