import ply.lex as lex
import difflib

tabla_errores = []
tabla_simbolos = {}

#Funcion apra reiniciar la lista de errores y los contadores del analizador
def reiniciar_analizador_lexico(lexer):
    global tabla_errores
    tabla_errores = []
    lexer.lineno = 1
    lexer.lexpos = 0

#Funcion para obtener los errores
def obtener_errores_lexicos():
    global tabla_errores
    return tabla_errores


def agregar_error_lexico(error_index,error_type,error_description,value,line,column):
    tabla_errores.append({
        'Indice':error_index,
        'Tipo': error_type,
        'Descripción': error_description,
        'Valor': value,
        'Linea': line,
        'Columna': column
    })
    
#Funcion para ecnotrar la coliman del token en la linea
def find_column_lex(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr<0:
        last_cr = 0
    column = (token.lexpos - last_cr)
    if column == 0:
        return 1
    return column
    
#Manejo de errores para identifacodres mal formados.
def t_error_IDENTIFICADOR(t):
    r'\d+[a-zA-Z][a-zA-Z0-9]*'
    agregar_error_lexico(12,'Léxico','Identificador inválido',t.value,t.lineno,find_column_lex(t.lexer.lexdata,t))
    t.lexer.skip(len(t.value))

def t_error_NUMERO_ENTERO(t):
    r'[+-]{2,}\d+'
    agregar_error_lexico(13,'Léxico','Formato de número entero invalido',t.value,t.lineno,find_column_lex(t.lexer.lexdata, t))
    t.lexer.skip(len(t.value))
    
def t_error_NUMERO_DECIMAL(t):
    r'\d+([\.]{2,}\d+[\.|\d]*)+ | \d+\.\d+(\.+\d+)+ | \.+\d+(\.|\d)* | (\d?\.\.\d)+ | \d+\.(?!\d)'
    agregar_error_lexico(13,'Léxico','Formato de número decimal invalido',t.value,t.lineno,find_column_lex(t.lexer.lexdata, t))
    t.lexer.skip(len(t.value))
    
#Manejo de errores para cualquier caracter no reconocido
def t_error(t):
    agregar_error_lexico(13,'Léxico','Cáracter no reconocido',t.value[0],t.lineno,find_column_lex(t.lexer.lexdata, t))
    t.lexer.skip(1)



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
    'empty',
    'open',
    'close',
    'start'
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
    'AND':'AND',
    'NOT':'NOT',
    'open':'open',
    'close':'close',
    'start':'start'
}

# Lista de subcadenas de palabras reservadas
partial_reserved = {word[:i] for word in reserved for i in range(2, len(word))}

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
    'AND': 'Y lógico',
    'NOT': 'Negación lógica',
    'open': 'Palabra reservada que es utilizada para abrir la mano',
    'close': 'Palabra reservada que es utilizada para cerrar la mano',
    'start': 'Palabra reservada que es utilizada para regresar el brazo a la posición inicial'
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
t_AND = r'AND'
t_NOT = r'NOT'

t_ignore = ' \t'
t_ignore_NEWLINE = r'\n'

#Expresión para actualiar la linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    tabla_simbolos[t.value] = {
        'Tipo': 'DECIMAL',
        'Valor': t.value,
        'Linea': t.lineno,
        'Columna': find_column_lex(t.lexer.lexdata, t)
    }
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    tabla_simbolos[t.value] = {
        'Tipo': 'ENTERO',
        'Valor': t.value,
        'Linea': t.lineno,
        'Columna': find_column_lex(t.lexer.lexdata, t)
    }
    return t

def t_BOOL(t):
    r'[Vv]alor|[Ff]also'
    t.value = True if t.value.lower() == 'valor' else False
    tabla_simbolos[t.value] = {
        'Tipo': 'BOOL',
        'Valor': t.value,
        'Linea': t.lineno,
        'Columna': find_column_lex(t.lexer.lexdata, t)
    }
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


# Modificación en t_ID para manejar palabras reservadas incompletas
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        if t.value in reserved:
            t.type = reserved[t.value]
        else:
            closest_match = difflib.get_close_matches(t.value, reserved.keys(), n=1)
            if closest_match and closest_match[0].startswith(t.value):
                suggestion = closest_match[0]
                agregar_error_lexico(14, 'Léxico', f'Palabra reservada incompleta: {t.value}, prueba con {suggestion}', t.value, t.lineno, find_column_lex(t.lexer.lexdata, t))
                t.lexer.skip(len(t.value))
                return None
            if t.value not in tabla_simbolos:
                tabla_simbolos[t.value] = {
                    'Tipo': 'identificador',
                    'Valor': t.value,
                    'Descripción': 'Identificador'
                }
    return t
        
lexer = lex.lex()

# codigo = """
# method run(){
#    ;Aquí mandas a llamar los métodos que llegues a crear
#    fng1 = 30$
#    degree a = 33.5$
#    sensor sensor1 = true$
#    hand.open()$
# }

# """

# lexer.input(codigo)


# for tok in lexer:
#     if isinstance(tok.value, tuple):
#         print(f"Token: {tok.type}, Valor: {tok.value[0]}, Descripción: {tok.value[1]}")
#     else:
#         if tok.type in symbols_descriptions:
#             print(f"Token: {tok.type}, Valor: {tok.value}, Descripción: {symbols_descriptions[tok.type]}")
#         else:
#             print(f"Token: {tok.type}, Valor: {tok.value}")

lexer.lineno = 1
