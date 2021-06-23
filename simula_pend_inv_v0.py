###########################################################       
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from tkinter import *
from functools import partial
import ctypes
###########################################################
real_T = ctypes.c_double
uint32_T = ctypes.c_uint
time_T = ctypes.c_double
SimTimeStep = ctypes.c_double

# Ancho máximo de la ventana a graficar
Tmax = 10 # segundos
# Fixed-step size (fundamental sample time) - Simulink
fixed_step = 0.0005 # segundos
# Período de muestreo de la gráfica
TsG = 0.05 # segundos
# Valores INICIALES:
dt = []
dFx = []
dfi = []
dx = []

# El código C original almacena los valores de entrada y salida en estructura de
# datos tipo: struct ExtU_p_inv_T para las entradas y struct ExtY_p_inv_T para 
# las salidas.
# Luego define 2 variables "p_inv_U" e "p_inv_Y" de los tipos anteriores donde 
# se almacenan la entrada y las salidas respectivamente.   
# El código Python usa la clase "ctypes.Structure" para crear estructuras que 
# reflejan las estructuras del código C. 
# Para crear un objeto Python que represente la estructura C, se crea una clase 
# que se derive de la "struct" originales. El atributo _fields_ de la clase debe 
# establecerse en una lista de tuplas de nombres y valores de campo. 
# Tenga en cuenta el operador POINTER que crea un puntero a partir de cualquier 
# tipo de ctypes. 
class ExtU_p_inv_T(ctypes.Structure):
    _fields_=[("Fx",real_T),
    ]
class ExtY_p_inv_T(ctypes.Structure):
    _fields_=[
        ("Fi",real_T), 
        ("x",real_T),
    ]
class P_p_inv_T_(ctypes.Structure):
    _fields_=[
        ("BrR",real_T), 
        ("BrT",real_T),
        ("Fi0",real_T),
        ("L",real_T),
        ("M",real_T),
        ("m",real_T),
        ("x0",real_T),
    ]

class Timing(ctypes.Structure):
    fields_=[
        ("clockTick0",uint32_T),
        ("stepSize0", time_T),     
        ("clockTick1",uint32_T),     
        ("simTimeStep",SimTimeStep),     
    ]
class tag_RTM_p_inv_T(ctypes.Structure):
    fields_=[
        ("Timing",Timing),
    ]




# Tenga en cuenta que en caso de que necesite hacer referencia a una estructura 
# antes de que esté completamente definida, primero puede declararla con "pass" 
# y luego especificar el contenido del campo:
# class ExtU_p_inv_T(Structure):
#     pass
# ExtU_p_inv_T._fields_=[("Fx",real_T)]
# class ExtY_p_inv_T(Structure):
#     pass
# ExtY_p_inv_T._fields_=[("Fi",real_T), ("x",real_T)]

# Podemos llamar directamente a nuestra biblioteca de la siguiente 
# manera:
pend_inv = ctypes.CDLL('/Users/mpg/Documents/MATLAB/Pend_Invertido/p_inv.dylib')
entrada = ExtU_p_inv_T.in_dll(pend_inv, "p_inv_U")
salida = ExtY_p_inv_T.in_dll(pend_inv, "p_inv_Y")
barra = P_p_inv_T_.in_dll(pend_inv, "p_inv_P")

puntero = ctypes.POINTER(tag_RTM_p_inv_T).in_dll(pend_inv,"p_inv_M")

print(puntero.contents.Timing())

# Funciones de punto de entrada del modelo
pend_inv.p_inv_initialize()

###########################################################
def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def conf_serie():
    pass
    
def animate(frame, lnFi, lnx):
    global ax, pend_inv, entrada, salida, barra, fixed_step, TsG 

    if frame == 0:
        x = barra.x0
        Fi = barra.Fi0
    else:
        for i in range(int(TsG//fixed_step)):
            pend_inv.p_inv_step()
        x = salida.x
        Fi = salida.Fi    
    Fx = entrada.Fx
    try:
        dt.append(frame * TsG)
        if (dt[-1] > Tmax):
            dFx.append(Fx)
            dfi.append(Fi)
            dx.append(x)
            dFx.pop(0)
            dfi.pop(0)
            dx.pop(0)
            dt.pop(0)
            ax.set_xlim(xmin=round(dt[0],2), xmax=round(dt[-1],2))        
        else:
            dFx.append(Fx)
            dfi.append(Fi)
            dx.append(x)
    except:
        print("Ocurrió un error")    
    lnx.set_data(dt, dx)
    lnFi.set_data(dt, dfi)
    return lnFi, lnx
###########################################################
############## INTERFASE GRAFICA GUI ######################
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
frame2.place(relx = 0.2, rely = 0, relwidth = 0.6, relheight = 0.10)
# BackGround color       
frame2.config(bg=rgbtohex(128,128,128))

# Creo Label en frame 2
Label(frame2, text = "CONFIGURACIÓN",font=("Helvetica", 14, "bold"),
bg=rgbtohex(128,128,128)).place(relx=0.35,rely=0.05)

# Creo Botón de Configuración PUERTO SERIE en frame 2
btnPS = Button(frame2,text="Parámetros",width=12,command=conf_serie)
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
ax.set_xlim(0, Tmax)
ax.set_ylim(-3.5, 3.5)
plt.grid()
lnFi, = plt.plot([], [], ',-', lw=1)
lnx, = plt.plot([], [], ',-', lw=1)
# creating the Tkinter canvas in frame 4 containing the Matplotlib figure
canvasF = FigureCanvasTkAgg(fig, master=frame4)
# canvasF.draw()
# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvasF, frame4, pack_toolbar=False)
toolbar.update()
# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
toolbar.place(relx=0.1,rely=0.9, relwidth = 0.5, relheight = 0.1)
canvasF.get_tk_widget().place(relx=0, rely=0, relwidth = 0.7, relheight = 0.9)

# Note:
# You must store the created Animation in a variable that lives as long as the 
# animation should run. Otherwise, the Animation object will be garbage-collected 
# and the animation stops. 
ani = FuncAnimation(fig, animate, fargs = (lnFi, lnx), blit = True)
# plt.show()

# Funciones de punto de entrada del modelo
pend_inv.p_inv_terminate()

# Llamo a método mainloop(), que es un bucle infinito
# siempre debe estar al final del archivo
raiz.mainloop()



