#imports

import ply.lex as lex
#import re
#import codecs
#import os
#import sys

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
]


#Se Reestructuro el código de t_ID para evitar el uso de if-else
#Se utiliza un diccionario de terminos para facilitar el creciemiento de las palabras reservadas.
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
}


#Expresiones regulares para Tokens Simples
t_PLUS = r'\+'
t_INCRE = r'\+\+' #Igual a discuSION
t_DECRE = r'\-\-' #Tenemos que discutir como solucionar el decremento
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
#Expresiones regulares para operadores de comparación y lógicos
t_NE = r'<>'
t_ASSIGN = r'='
t_LTE = r'<='
t_GTE = r'>='
t_AND = r'AND'
t_NOT = r'NOT'
#t_EQUALS = r'\+\=\+'


#Ignora espacios en blanco y tabulaciones
t_ignore = ' \t'

#Expresión Regular para Números decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

#Expresión Regular para Números Enteros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

#Expresión Regular para Booleanos
def t_BOOL(t):
    r'[Vv]alor|[Ff]also'
    t.value = True if t.value.lower() == 'valor' else False
    return t

#Expresión Regular para identificadores (nombres de variables, funciones, etc.).
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


# Lista para almacenar los comentarios junto con su posición de inicio
comments = []

#Expresión Regular para comentarios
def t_COMENTARIOS(t):
    r'\;.*'
    comments.append((t.value, t.lexer.lineno, t.lexpos))
    return t

# Lista para almacenar los comentarios junto con su posición de inicio
commentsML = []
#Expresión regular para comentarios de multiple linea
def t_COMENTARIOS_MULTILINEA(t):
    r'<\-(?:[^-]|-(?!>))*\->'  # Comentarios de múltiples líneas entre <- y ->
    t.lexer.lineno += t.value.count('\n')
    commentsML.append((t.value, t.lexer.lineno, t.lexpos))
    return t

#Expresión para ignorar saltos de linea
t_ignore_NEWLINE = r'\n'

#Expresión para actualiar la linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Expresión Regular para fin de linea
def t_FIN_DE_INSTRUCCION(t):
    r'\$'
    return t

# Manejo de errores
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno} at column {t.lexpos}")
    t.lexer.skip(1)

# Evitar la impresión de advertencias sobre tokens no utilizados
lex.errorlog = lex.NullLogger()

# Construcción del analizador léxico
lexer = lex.lex()

codigo = """
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
# Evitar la impresión de advertencias sobre tokens no utilizados
lex.errorlog = lex.NullLogger()

# Pasar el código al analizador léxico
lexer.input(codigo)

# Tokenizar e imprimir los tokens
for tok in lexer:
    print(tok)  