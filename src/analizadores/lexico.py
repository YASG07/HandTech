#imports

import ply.lex as lex
import re
import codecs
import os
import sys
tokens = {
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
}

#Expresiones regulares para Tokens Simples
t_PLUS = r'\+'
t_INCRE = r'\++'
#t_DECRE = r'\--' #Posiblemente no jale
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
    if t.value == 'if':
        t.type == 'if'
    elif t.value == 'then':
        t.type == 'then'
    elif t.value == 'else':
        t.type == 'else'
    elif t.value == 'for':
        t.type == 'for'
    elif t.value == 'while':
        t.type == 'while'
    elif t.value == 'stop':
        t.type == 'stop'
    elif t.value == 'method':
        t.type == 'method'
    elif t.value == 'run':
        t.type == 'run'
    elif t.value == 'return':
        t.type == 'return'
    elif t.value == 'console':
        t.type == 'console'
    elif t.value == 'export':
        t.type == 'export'
    elif t.value == 'import':
        t.type == 'import'
    elif t.value == 'mbm':
        t.type == 'mbm'
    elif t.value == 'arm':
        t.type == 'arm'
    elif t.value == 'hand':
        t.type == 'hand'
    elif t.value == 'rotate':
        t.type == 'rotate'
    elif t.value == 'fng1':
        t.type == 'fng1'
    elif t.value == 'fng2':
        t.type == 'fng2'
    elif t.value == 'fng3':
        t.type == 'fng3'
    elif t.value == 'fng4':
        t.type == 'fng4'
    elif t.value == 'fng5':
        t.type == 'fng5'
    elif t.value == 'is':
        t.type == 'is'
    elif t.value == 'mov':
        t.type == 'mov'
    elif t.value == 'force':
        t.type == 'force'
    elif t.value == 'sensor':
        t.type == 'sensor'
    elif t.value == 'weight':
        t.type == 'weight'
    elif t.value == 'block':
        t.type == 'block'
    elif t.value == 'up':
        t.type == 'up'
    elif t.value == 'down':
        t.type == 'down'
    elif t.value == 'linkage':
        t.type == 'linkage'
    elif t.value == 'wrist':
        t.type == 'wrist'
    elif t.value == 'piRad':
        t.type == 'piRad'
    elif t.value == 'degree':
        t.type == 'degree'
    elif t.value == 'wait':
        t.type == 'wait'
    elif t.value == 'ID':
        t.type == 'NUMBER'
    elif t.value == 'DECIMAL':
        t.type == 'DECIMAL'
    elif t.value == 'BOOL':
        t.type == 'BOOL'
    #elif t.value == 'PLUS': No se si van lo de las operaciones o ne
       # t.type == 'PLUS' Tampoco se si va lo que serian los signos de agrupacion,
    # Comas y todas esas vainas, queda por ver
    elif t.value == 'AND':
        t.type == 'AND'
    elif t.value == 'NOT':
        t.type == 'NOT'
    return t

#Expresión Regular para comentarios
def t_COMENTARIOS(t):
    r'\;.*'
    pass

#Ignora espacios en blanco y tabulaciones
t_ignore = '\t'

# Manejo de errores
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Evitar la impresión de advertencias sobre tokens no utilizados
lex.errorlog = lex.NullLogger()

# Construcción del analizador léxico
lexer = lex.lex()

codigo = """

"""

# Pasar el código al analizador léxico
lexer.input(codigo)

# Tokenizar e imprimir los tokens
for tok in lexer:
    print(tok)