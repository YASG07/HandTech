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
}

# Diccionario de descripciones para palabras reservadas
descriptions = {
    'if': 'Condición de control para la ejecución condicional de instrucciones',
    'then': 'Indica el bloque de instrucciones que se ejecutará si la condición del if es verdadera',
    'else': 'Indica el bloque de instrucciones que se ejecutará si la condición del if es falsa',
    # Aquí puedes agregar más descripciones para otras palabras reservadas
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
t_AND = r'AND'
t_NOT = r'NOT'
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
        t.value = (t.value, descriptions.get(t.value, ''))
    return t

def t_COMENTARIOS(t):
    r'\;.*'
    return t

def t_COMENTARIOS_MULTILINEA(t):
    r'<\-(?:[^-]|-(?!>))*\->'
    return t

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
        print(f"Token: {tok.type}, Valor: {tok.value}")
