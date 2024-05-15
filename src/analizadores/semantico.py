txt = ""
cont = 0
def incrementarContador():
    global cont
    cont + 1
    return "%d" %cont

class Nodo():
    pass
class programa(Nodo):
    def __init__(self,son1,name):
        self.name = name
        self.name = son1
        
    def imprimir(self,ident):
        self.son1.imprimir("" + ident) #Para controlar las identaciones
        
        print(ident + "Nodo: "+self.name)
        
    def traducir(self, ident):
        global txt
        id = incrementarContador()
        son1 = self.son1.traducir()
        
        txt += ident +"[Label= "+self.name+"]"+"\n\t"
        txt += id +"->"+son1+"\n\t"
        
        return "reun {\n\t"+txt+"}"
   
#gramatica para método principal
class main(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
        
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#bloque de código
class bloque(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
        
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
   
#expression
class expression(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
   
#valores (auxiliar para expression)
class valor(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#operadores aritmeticas
class operadoresAritmeticos(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#operadores logicas
class operadoresLogicos(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#operaciones aritmeticas
class operacionesAritmeticas(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#operaciones lógicas
class operacionesLogicas(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#partes de la mano
class partesMano(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#instrucciones
class instruccion(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#llamada de funciones
class llamada(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#asignacion
class asignacion(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#tipos de dato
class tipoDato(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#gramatica auxiliar. Símbolo de apoyo para ciclos
class aux(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#gramatica para ciclos
class ciclos(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#gramatica para condicionales
class condicion(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#gramatica para objetos
class objetos(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#gramatica para metodos
class metodos(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
#método para devolver errores
class error(Nodo):
    def __init__(self,name):
        self.name = name

    def imprimir(ident):
        pass
    def traducir(self):
        global txt
        id = incrementarContador()

        return id
    
