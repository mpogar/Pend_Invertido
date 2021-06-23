###########################################################
import serial        
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from threading import Thread, Lock
from tkinter import *
# from functools import partial

###########################################################
# Período de muestreo de la grafica en ms
Tsample = 100
# Cantidad de muestreo de la grafica graficadas
muestras = 50
# Valores INICIALES
distancia = 0.00
xdata = []
ydata = []
ani = []
###########################################################
def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

def conf_serie():
    pass

# getData lee puerto serie y guarda el dato en la variable global float 'distancia'
# Está función se ejecuta en el thread "colectorDatos"
def get_data(lock):
    global distancia

    try:
        serialArduino = serial.Serial("/dev/tty.usbmodem11101",9600,timeout=1.0)
    except:
        print("No es posible conectar al puerto")
    time.sleep(1) # espera 1 seg, para dar tiempo a conectarse
    while True:
        try:
            #serialArduino.reset_input_buffer()
            # lock the state and unlock the state
            with lock:
                distancia = float(serialArduino.readline().decode('ascii').strip())
                # Poner un FILTRO a distancia
                print(distancia)
        except:
            print("Error lectura puerto SERIE")

# main_graf function is created for plotting a graph on tkinter window
def main_graf(lock):
    global ani, fig, ax, xdata, ydata

    ax.set_xlim(0, (muestras-1))
    ax.set_ylim(-0.2, 1.2)
    plt.grid()
    # Pyplot's plotting methods can be applied to either the Pyplot root 
    # (pyplot.plot()) or an axes object (axes.plot()).
    # Calling a plotting function directly on the Pyplot library (pyplot.plot()) 
    # creates a default subplot (figure and axes). Calling it on an axes object 
    # (axes.plot()) requires that you to have created your own axes object already 
    # and puts the graph onto that customized plotting space.
    # While pyplot.plot() is easy to use, you have more control over your space 
    # (and better able to understand interaction with other libraries) if you create 
    # an axes object axes.plot().
    # Axes.plot() returns an axes object. Every axes object has a parent figure object. 
    # The axes object contains the methods for plotting, as well as most customization 
    # options, while the figure object stores all of the figure-level attributes and 
    # allow the plot to output as an image.
    # If you use pyplot.plot() method and want to start customizing your axes, you can 
    # find out the name of the default axes object it created by calling pyplot.gca() 
    # to "get current axes."
    # ax.plot([0, 1, 2, 3, 4, 5], [1, 0.5, 0.8, 0.9, 0.1, 0.7])
    # plt.plot([0, 1, 2, 3, 4, 5], [1, 0.5, 0.8, 0.9, 0.1, 0.7])

    # plot returns a list of Line2D objects. 
    # In the code below we will suppose that we have only 
    # one line so that the list returned is of length 1. 
    # We use tuple unpacking with line, to get the first 
    # element of that list:
    ln, = plt.plot([], [], ',-', lw=2)
    # Note:
    # You must store the created Animation in a variable that lives as long as the 
    # animation should run. Otherwise, the Animation object will be garbage-collected 
    # and the animation stops.
    ani = FuncAnimation(fig, animate, fargs = (ln, xdata, ydata, lock), 
                        interval = Tsample, blit = False)
    # Show the plot
    # plt.show()
    
def animate(frame, ln_aux, dx, dy, lock):
    global distancia, ax, event
    try:
        # Use the lock as a context manager
        # lock the state and unlock the state
        with lock:
            dy.append(distancia)
        if (len(dy) == muestras + 1):
            dx.append(frame)
            dx.pop(0)
            ax.set_xlim(dx[0], dx[-1])        
            dy.pop(0)
        else:
            dx.append(frame)
    except:
        print("Ocurrió un error.")
    dx = np.array(dx)
    dy = np.array(dy)
    ln_aux.set_data(dx,dy)
    return ln_aux,



    # thisx = [0, x1[i], x2[i]]
    # thisy = [0, y1[i], y2[i]]

    # if i == 0:
    #     history_x.clear()
    #     history_y.clear()

    # history_x.appendleft(thisx[2])
    # history_y.appendleft(thisy[2])

    # line.set_data(thisx, thisy)
    # trace.set_data(history_x, history_y)
    # time_text.set_text(time_template % (i*dt))
    # return line, trace, time_text


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





# ax.set_xlim(0, (muestras-1))
# ax.set_ylim(-0.2, 1.2)
# plt.grid()
# ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
# plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
# ln, = ax.plot([1, 2, 3, 4], [1, 4, 2, 3], 'o-', lw=2)
# ani = FuncAnimation(fig, animate, fargs = (ln, xdata, ydata, lock), 
#                         interval = Tsample, blit = False)
# Pintamos la linea
# plt.show()





# Configuramos y lanzamos los hilos encargados de:
# leer datos del serial,
# graficar los datos obtenidos.
if __name__ == "__main__":

    # create a lock
    # Cuando más de un hilo está bloqueado en acquire() esperando 
    # que el estado sea abierto, sólo un hilo procederá cuando una 
    # llamada a release() restablezca el estado a abierto; cuál de 
    # los hilos en espera procederá no está definido, y puede 
    # variar a través de las implementaciones.
    lock = Lock()

    # create a Threads
    colectorDatos = Thread(target = get_data, args=(lock,))
    # graficoDatos =  Thread(target = main_plot, args=(ax, lock))

    # init Threads
    colectorDatos.start()
    # graficoDatos.start()

    # Espera a que el hilo termine. Esto bloquea el hilo llamador 
    # hasta que el hilo cuyo método join() es llamado finalice – ya 
    # sea normalmente o a través de una excepción no gestionada – o 
    # hasta que el tiempo de espera opcional caduque.
    # colectorDatos.join()
    # graficoDatos.join()


main_graf(lock) 

# ax.set_xlim(0, (muestras-1))
# ax.set_ylim(-0.2, 1.2)
# plt.grid()
# ax.plot([0, 1, 2, 3, 4, 5], [1, 0.5, 0.8, 0.9, 0.1, 0.7])
# plt.plot([0, 1, 2, 3, 4, 5], [1, 0.5, 0.8, 0.9, 0.1, 0.7])
# ln, = ax.plot([], [], 'o-', lw=2)
# ani = FuncAnimation(fig, animate, fargs = (ln, xdata, ydata, lock), 
#                         interval = Tsample, blit = False)
# Pintamos la linea
# plt.show()

# Llamo a método mainloop(), que es un bucle infinito
# siempre debe estar al final del archivo
raiz.mainloop()
###########################################################

