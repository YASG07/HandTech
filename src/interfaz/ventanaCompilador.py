#Ventana principal del compilador HandTech

#imports
from tkinter import *

#creación de la ventana
ventana = Tk()
frame1 = Frame(ventana, width=1024, height=640)
frame1.pack()
#atributos de la ventana
ventana.title('HandTech')
#ventana.geometry("1020x640")#dimensiones
ventana.config(bg="black")#color de fondo
#ventana.resizable(True, True)

#método para ejecutarse desde otro archivo
def exec():
    ventana.mainloop()