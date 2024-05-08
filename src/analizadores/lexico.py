import ply.lex as lex

tokens = [
    'if',
    'then',
    'else',
    'for',
    'while',
    'stop',
    'method',
    'run',
    'return',
    'console',
    'export',
    'import',
    'mbm',
    'arm',
    'hand',
    'rotate',
    'fng1',
    'fng2',
    'fng3',
    'fng4',
    'fng5',
    'is',
    'mov',
    'force',
    'sensor',
    'weight',
    'block',
    'up',
    'down',
    'linkage',
    'wrist',
    'piRad',
    'degree',
    'wait',
    'ID',
    'NUMBER',
    'DECIMAL',
    'BOOL',
    'PLUS',
    'INCRE',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LT',
    'GT',
    'LPARENT',
    'RPARENT',
    'LKEY',
    'RKEY',
    'SBLKEY',
    'SBRKEY',
    'SEMICOLON',
    'TWPOINT',
    'COMMA',
    'DOT',
    'NE',
    'ASSIGN',
    'LTE',
    'GTE',
    'AND',
    'NOT',
    'COMENTARIOS',
    'COMENTARIOS_MULTILINEA',
    'FIN_DE_INSTRUCCION',
    'DECRE',
    'EQUALS',
    'false',
    'true',
    'int',
    'float',
    'bool',
    'none',
    'empty'
]

reserved = {
    'if': 'if',
    'then': 'then',
    'else': 'else',
    'for': 'for',
    'while': 'while',
    'stop': 'stop',
    'method': 'method',
    'run': 'run',
    'return': 'return',
    'console': 'console',
    'export': 'export',
    'import': 'import',
    'mbm': 'mbm',
    'arm': 'arm',
    'hand': 'hand',
    'rotate': 'rotate',
    'fng1': 'fng1',
    'fng2': 'fng2',
    'fng3': 'fng3',
    'fng4': 'fng4',
    'fng5': 'fng5',
    'is': 'is',
    'mov': 'mov',
    'force': 'force',
    'sensor': 'sensor',
    'weight': 'weight',
    'block': 'block',
    'up': 'up',
    'down': 'down',
    'linkage': 'linkage',
    'wrist': 'wrist',
    'piRad': 'piRad',
    'degree': 'degree',
    'wait': 'wait',
    'false':'false',
    'true':'true',
    'int':'int',
    'float':'float',
    'bool':'bool',
    'none':'none',
    'empty':'empty',
    'and':'and',
    'not':'not'
}

# Diccionario de descripciones para palabras reservadas
descriptions = {
    'if': 'Condición de control para la ejecución condicional de instrucciones',
    'then': 'Indica el bloque de instrucciones que se ejecutará si la condición del if es verdadera',
    'else': 'Indica el bloque de instrucciones que se ejecutará si la condición del if es falsa',
    'for': 'Condicion de ciclo para la ejecucion de un bucle for',
    'while': 'ondicion de ciclo para la ejecucion de un bucle while',
    'stop': 'Utilizda para detener la ejecición de los ciclos',
    'method': 'Utilizada para definir un bloque de codigo como una función o método',
    'run': 'Indica el contenido principal del programa',
    'return': 'Palabra reservada que nos permite devolver el valor de una función o método',
    'console': 'Utilizada para imprimir mensajes en consola',
    'export': 'Utilizada para exportar funcion y/o variables de un archivo a otro',
    'import': 'Utilizada para importar arcivos o instrucciones precargadas',
    'mbm': 'Utilizada para definir un objeto que se asemeja a una parte del cuerpo',
    'arm': 'Utiizada para hacer referencia al brazo',
    'hand': 'Utilizada para hacer referencia a la mano completa',
    'rotate': 'Método utilizado para rotar la muñeca X cantidad de grados.',
    'fng1': 'Utilizada para hacer referencia al dedo índice',
    'fng2': 'Utilizada para hacer referencia al dedo anular',
    'fng3': 'Utilizada para hacer referencia al dedo medio',
    'fng4': 'Utilizada para hacer referencia al dedo meñique',
    'fng5': 'Utilizada para hacer referencia al dedo pulgar',
    'is': 'Utilizada para devolver el valor de una variable Booleana',
    'mov': 'Utilizada para mover X cantidad de grados la muñeca',
    'force': 'Utilizada para aplicar X cantidad de fuerza(libras) a un objeto',
    'sensor': 'Palabra reservada utilizada para instancear un sensor',
    'weight': 'Utilizada para devolver el peso de un objeto sostenido en libras',
    'block': 'Utilizada para devolver una variable Booleana',
    'up': 'Utilizada para levantar una parte del brazo',
    'down': 'Utilizda para bajar una parte del brazo',
    'linkage': 'Palabra reservada para hacer referencia a las articulaciones',
    'wrist': 'Utilizda para hacer referencia a la muñeca',
    'piRad': 'Palabra reservada que devuelve el valor de pi radianes',
    'degree': 'Palabra reservada que indica cuantos grados se puede mover un componente de la protesis',
    'wait': 'Utilizada para estabilizar el delay entre operaciones',
    'false':'Utilizada para representar el valor booleano: falso',
    'true':'Utilizada para representar el valor booleano: verdadero',
    'int':'Utilizada para declarar un tipo de dato como entero',
    'float':'Utilizada para declarar un tipo de dato como decimal',
    'bool':'Utilizada para respresentar valores Booleanos',
    'none':'Utilizada para representar la ausencia de valor',
    'empty':'Utilizada para retornar un valor vacio',
    'and':'Utilizada para usar el valor booleano AND',
    'not':'Utilizada para usar el valor booleano NOT'
}

# Diccionario de descripciones para símbolos
symbols_descriptions = {
    'PLUS': 'Suma',
    'INCRE': 'Incremento',
    'MINUS': 'Resta',
    'TIMES': 'Multiplicación',
    'DIVIDE': 'División',
    'LT': 'Menor que',
    'GT': 'Mayor que',
    'LPARENT': 'Paréntesis izquierdo',
    'RPARENT': 'Paréntesis derecho',
    'LKEY': 'Llave izquierda',
    'RKEY': 'Llave derecha',
    'SBLKEY': 'Corchete izquierdo',
    'SBRKEY': 'Corchete derecho',
    'SEMICOLON': 'Punto y coma',
    'TWPOINT': 'Dos puntos',
    'COMMA': 'Coma',
    'DOT': 'Punto',
    'NE': 'No igual',
    'ASSIGN': 'Asignación',
    'LTE': 'Menor o igual que',
    'GTE': 'Mayor o igual que',
    'AND': 'Y lógico',
    'NOT': 'Negación lógica',
    'EQUALS': 'Igualdad'
}

t_PLUS = r'\+'
t_INCRE = r'\+\+'
t_DECRE = r'\-\-'
t_MINUS = r'\-'  
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_LKEY = r'\{'
t_RKEY = r'\}'
t_SBLKEY = r'\['
t_SBRKEY = r'\['
t_SEMICOLON = r';'
t_TWPOINT = r':'
t_COMMA = r','
t_DOT = r'\.'
t_NE = r'<>'
t_ASSIGN = r'='
t_LTE = r'<='
t_GTE = r'>='
t_EQUALS = r'\+\=\+'

t_ignore = ' \t'
t_ignore_NEWLINE = r'\n'

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'[Vv]alor|[Ff]also'
    t.value = True if t.value.lower() == 'valor' else False
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    if t.type != 'ID':
        t.value = (t.value, descriptions.get(t.value, 'Palabra/Simbolo Desconocido'))
    return t

def t_COMENTARIOS(t):
    r'\;.*'
    pass

def t_COMENTARIOS_MULTILINEA(t):
    r'<\-(?:[^-]|-(?!>))*\->'
    pass

def t_FIN_DE_INSTRUCCION(t):
    r'\$'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno} at column {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

codigo = """
method run(){
   ;Aquí mandas a llamar los métodos que llegues a crear
   ;fng1 = 30$
   degree = 33$
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
      --incremento$
      ++incremento$
      hola +=+ hi$
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

lexer.input(codigo)

for tok in lexer:
    if isinstance(tok.value, tuple):
        print(f"Token: {tok.type}, Valor: {tok.value[0]}, Descripción: {tok.value[1]}")
    else:
        if tok.type in symbols_descriptions:
            print(f"Token: {tok.type}, Valor: {tok.value}, Descripción: {symbols_descriptions[tok.type]}")
        else:
            print(f"Token: {tok.type}, Valor: {tok.value}")
