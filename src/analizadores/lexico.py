#imports

import ply.lex as lex
import re
import codecs
import os
import sys

tokens = ['ID', 'NUMBER', 'MINUS', 'TIMES', 'DIVIDE', 'ODD', 'ASSIGN', 'NE', 'LTE', 'GT', 'GTE', 'LPARENT',
          'RPARENT', 'COMMA', 'SEMICOLON', 'DOT', 'UPDATE']

reservadas = {
    'begin':'BEGIN',
    'end':'END',
    'if':'IF',
    'then':'THEN',
    'while':'WHILE',
    'do':'DO',
    'call':'CALL',
    'const':'CONST',
    'int':'INT',
    'procedure':'PROCEDURE',
    'out':'OUT',
    'in':'IN',
    'else':'ELSE',
}

tokens = tokens + list(reservadas.values())

t_ignore = '\t'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ODD = r'ODD'
t_ASSIGN = r'='
t_NE = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'>='
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'
t_UPDATE = r':='

def t_ID(token):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if token.value.upper() in reservadas:
        token.value = token.value.upper()
        token.type = token.value
    return token

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Retomar en el minuto 20:30 del vídeo Analizador léxico en python

def t_COMMENT(t):
    r'\;.*'
    pass

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value) #Linea que posiblemente eliminemos
    return t

def t_error(t):
    print("Caracter Ilegal '%s'"%t.value)
    t.lexer.skip(1)

def buscarFicheros(directorio):
    ficheros = []
    numArchivos = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)

    for file in files:
        print(str(cont)+". "+file)
        cont = cont+1

    while respuesta == False:
        numArchivos = input('\nNumero del test: ')
        for file in files:
            if file == files[int(numArchivos)-1]:
                respuesta = True
                break
    print("Has escogido \"%s\" \n" %files[int(numArchivos)-1])
    
    return files[int(numArchivos)-1]

directorio = 'C:/Compilador/HandTech/src/Test/'
archivo = buscarFicheros(directorio)
test = directorio+archivo
fp = codecs.open(test,"r","UTF-8")
cadena = fp.read()
fp.close()

analizador = lex.lex()

analizador.input(cadena)

while True:
    tok = analizador.token()
    if not tok : break
    print(tok)