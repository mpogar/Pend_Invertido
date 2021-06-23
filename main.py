import serial        
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

from tkinter import *
from functools import partial

# INTERFASES GRAFICAS GUI
# Librería: Tkinter, viene instalada por defecto
# ESTRUCTURA DE UNA VENTANA:
# Raiz(Tk) --> Frame --> Widgets

# Creo la raiz
raiz = Tk()
# Título Ventana:
raiz.title("Péndulo Invertido")
# Tamaño Ventana raiz
raiz.geometry("800x600")
# Deshabilito cambio en el tamaño de la ventana raiz
raiz.resizable(False,False)

###########################################################
def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def conf_serie():
    pass

# plot function is created for plotting the graph tkinter window
def plot():
    # Create a figure containing a single axes.
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = frame4)  
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(relx=0,rely=0, relwidth = 0.7, relheight = 0.9)
    # creating the Matplotlib toolbar
    """ toolbar = NavigationToolbar2Tk(canvas, frame4)
    toolbar.update() """
    # placing the toolbar on the Tkinter window
    """ canvas.get_tk_widget().pack() """

###########################################################

# Creo frame 1
frame1 = Frame(raiz)
# Empaqueto el frame en la raiz:
# MÉTODO 1
frame1.place(x = 0, y = 0, relwidth = 0.2, relheight = 0.1)
# MÉTODO 2
""" frame1.pack(fill="x", expand=False) 
frame1.config(height="60") """
# BackGround color       
frame1.config(bg=rgbtohex(128,128,128))

# Creo Label en frame 1
Label(frame1, text = "PÉNDULO INVERTIDO\n v1.0",font=("Helvetica", 12, "bold"),
bg=rgbtohex(128,128,128)).place(relx=0.03,rely=0.20)

# Creo frame 2
frame2 = Frame(raiz)
# Empaqueto el frame en la raiz:
# MÉTODO 1
frame2.place(relx = 0.2, rely = 0, relwidth = 0.6, relheight = 0.1)
# BackGround color       
frame2.config(bg=rgbtohex(128,128,128))

# Creo Label en frame 2
Label(frame2, text = "CONFIGURACIÓN",font=("Helvetica", 14, "bold"),
bg=rgbtohex(128,128,128)).place(relx=0.35,rely=0.05)

# Creo Botón de Configuración PUERTO SERIE en frame 2
btnPS = Button(frame2,text="Puerto Serie",width=12,command=conf_serie)
btnPS.place(relx=0,rely=0.5)

# Creo Botón de Configuración PUERTO SERIE en frame 2
btnA = Button(frame2,text="Arduino",width=12,command=conf_serie)
btnA.place(relx=0.25,rely=0.5)

# Creo Botón de Configuración PUERTO SERIE en frame 2
btnS = Button(frame2,text="Sensores",width=12,command=conf_serie)
btnS.place(relx=0.50,rely=0.5)

# Creo Botón de Configuración PUERTO SERIE en frame 2
btnM = Button(frame2,text="Motor",width=12,command=conf_serie)
btnM.place(relx=0.75,rely=0.5)

# Creo frame 3
frame3 = Frame(raiz)
# Empaqueto el frame en la raiz:
# MÉTODO 1
frame3.place(relx = 0.8, rely = 0, relwidth = 0.2, relheight = 0.1)
# BackGround color       
frame3.config(bg=rgbtohex(128,128,128))

# Creo Canvas en frame 3 --> Coloco imagen (.png o .gif)
canvasC = Canvas(frame3) 
canvasC.pack(fill="both",expand=True)     
canvasC.config(bg=rgbtohex(128,128,128))
img = PhotoImage(file="/Users/mpg/Documents/Python/Pend_Invertido/figuras/conectado.png")
# To display a graphics image on a canvas C, use:
# id = C.create_image(x, y, option, ...)
# This constructor returns the integer ID number of the image object for that canvas.
# The image is positioned relative to point (x, y).            
canvasC.create_image(80,50, anchor=S, image=img)

# Creo frame 4
frame4 = Frame(raiz)
# Empaqueto el frame en la raiz:
# MÉTODO 1
frame4.place(relx = 0, rely = 0.1, relwidth = 1, relheight = 0.9)
# MÉTODO 2
""" frame4.pack(fill="both",expand=True) 
frame4.config(height = "540") """
# BackGround color       
frame4.config(bg=rgbtohex(255,255,255))

# Create a figure containing a single axes to put in canvasF
fig, ax = plt.subplots()
# creating the Tkinter canvas in frame 4 containing the Matplotlib figure
canvasF = FigureCanvasTkAgg(fig, master=frame4)
canvasF.draw()  
# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvasF, frame4, pack_toolbar=False)
toolbar.update()
# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
toolbar.place(relx=0.1,rely=0.9, relwidth = 0.5, relheight = 0.1)
canvasF.get_tk_widget().place(relx=0, rely=0, relwidth = 0.7, relheight = 0.9)

ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

# Llamo a método mainloop(), que es un bucle infinito
# siempre debe estar al final del archivo
raiz.mainloop()