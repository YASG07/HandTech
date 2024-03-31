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

#Retomar en el minuto 20:30 del vídeo Analizador léxico en python