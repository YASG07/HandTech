#Analizador sintáctico versión pl0(.pl0) para HandTech

#imports
import ply.yacc as yacc
import os
import codecs
import re

from lexico import tokens
from sys import stdin

precedence = (
    ('right','ASSIGN'),
    ('right','UPDATE'),
    ('left','NE'),
    ('left', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('rigt', 'ODD'),
    ('left', 'LPARENT', 'RPARENT'),
)

#métodos para validar cada una de las gramaticas que componen el lenguaje
def prod_program(produccion):
    '''program = block'''
    print("program")
    #produccion[0] = program(produccion[1], "program") #pendiente a terminar

def prod_constDeclare(produccion):
    '''constDeclare = CONST constAssigmentList; '''
    print("CONST")
    #produccion[0] = constDeclare(produccion[2]) #pendiente a terminar

def prod_constDeclareEmpty(produccion):
    '''constDeclare = empty'''
    print("CONST Empty")
    #produccion[0] = Null() #pendiente a terminar

def prod_constAssignmentList1(produccion):
    '''constAssigmentList : ID = NUMBER'''
    print("constAssigmentList 1")

def prod_constAssignmentList2(produccion):
    '''constAssignmentList : constAssigmentList, ID = NUMBER'''
    print("constAssigmentList 2")

def prod_varDeclare1(produccion):
    '''varDeclare : VAR ID'''
    print("varDeclare")

def prod_varDeclareEmpty(produccion):
    '''varDeclare : empty'''
    print("varDeclare nulo")

def prod_identList1(produccion):
    '''identList : ID'''
    print("identList 1")

def prod_identList2(produccion):
    '''identList : identList, ID'''
    print("identList 2")

def prod_procDeclare1(produccion):
    '''procDeclare : procDeclare PROCEDURE ID ; block ;'''
    print("procDeclare 1")

def prod_procDeclareEmpty(produccion):
    '''procDeclare : empty'''
    print("procDeclare nulo")

def prod_statement1(produccion):
    '''statement : ID UPDATE expression'''
    print("statement 1")

def prod_statement2(produccion):
    '''statement : CALL ID'''
    print("statement 2")

def prod_statement3(produccion):
    '''statement : BEGIN statementList END'''
    print("statement 3")

def prod_statement4(produccion):
    '''statement : IF condition THEN statement'''
    print("statement 4")

def prod_statement5(produccion):
    '''statement : WHILE condition DO statement'''
    print("statement 5")

def prod_statementEmpty(produccion):
    '''statement : empty'''
    print("statement nulo")

def prod_statementList1(produccion):
    '''statementList : statement'''
    print("statementList 1")

def prod_statementList2(produccion):
    '''statementList : statementList ; statement'''
    print("statementList 2")

def prod_condition1(produccion):
    '''condition : ODD expression'''
    print("condition 1")

def prod_condition2(produccion):
    '''condition : expression relation expression'''
    print("condition 2")

def prod_relation1(produccion):
    '''relation : ASSIGN'''
    print("relation 1")

def prod_relation2(produccion):
    '''relation : NE'''
    print("relation 2")

def prod_relation3(produccion):
    '''relation : LT'''
    print("relation 3")

def prod_relation4(produccion):
    '''relation : GT'''
    print("relation 4")

def prod_relation5(produccion):
    '''relation : LTE'''
    print("relation 5")

def prod_relation6(produccion):
    '''relation : GTE'''
    print("relation 6")

def prod_expression1(produccion):
    '''expression : term'''
    print("expression 1")

def prod_expression2(produccion):
    '''expression : addingOperator term'''
    print("expression 2")

def prod_expression3(produccion):
    '''expression : expression addingOperator term'''
    print("expression 3")

def prod_term1(produccion):
    '''term : factor'''
    print("term 1")

def prod_term1(produccion):
    '''term : term multiplyingOperator factor'''
    print("term 1")

def prod_multiplyingOperator1(produccion):
    '''multiplyingOperator : TIMES'''
    print("multiplyingOperator 1")

def prod_multiplyingOperator2(produccion):
    '''multiplyingOperator : DIVIDE'''
    print("multiplyingOperator2")

def prod_factor1(produccion):
    '''factor : ID'''
    print("factor 1")

def prod_factor2(produccion):
    '''factor : NUMBER'''
    print("factor 2")

def prod_factor3(produccion):
    '''factor : LPARENT expression RPARENT'''
    print("prod_factor3")

def prod_empty(produccion):
    '''empty :'''
    pass

def prod_error(produccion):
    print("error de sintaxis ",produccion)
    print("error detectado en la línea: "+str(produccion.lineno))

def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)
    
    for file in files:
        print(str(cont) + ". "+file)
        cont = cont + 1

    while respuesta == False:
        numArchivo = input('\nNúmero del test: ')
        for file in files:
            if file == files[int(numArchivo)-1]:
                respuesta = True
                break
    print("Has escogido \"%s\" \n" %files[int(numArchivo)-1])
    return files[int(numArchivo) - 1]

#directorio LOCAL del archivo de pruebas
directorio = '/Users/Lenovo/Documents/TEC/Len. & Aut I/HandTech/src/Test/' 
archivo = buscarFicheros(directorio)
test = directorio + archivo
fp = codecs.open(test, "r", "utf-8")
codigo = fp.read()
fp.close()

parser = yacc.yacc()
result = parser.parse(codigo)

print(result)
#Retomar vídeo analizador sintactico en python minuto - 41:52