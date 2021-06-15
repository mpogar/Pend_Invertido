import serial
import time
import numpy as np        
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread, Lock

muestras = 6
distancia = ""

# getData lee puerto serie y guarda el dato en la variable global float 'distancia'
# Está función se ejecuta en el thread "colectorDatos"
def getData(lock):
    global distancia
    try:
        serialArduino = serial.Serial("/dev/tty.usbmodem11101",9600,timeout=1.0)
        #timeout (1 segundo) o tiempo máximo de espera para una lectura.
    except:
        print("No se puede conectar al puerto")
    time.sleep(1) # espera 1 seg, para dar tiempo a conectarse
    while True:
        try:
            #serialArduino.reset_input_buffer()
            # lock the state 
            lock.acquire()
            distancia = serialArduino.readline().decode('ascii').strip()
            # unlock the state 
            lock.release()
            print(distancia)
        except:
            print("Error lectura puerto SERIE")

# aniGraf realiza una gráfica animada de los datos recibidos en la variable global 
# float 'distancia'.
# Está función se ejecuta en el thread "graficoDatos"
def aniGraf(lock):
    global muestras, distancia 
    xdata = []
    ydata = []
    ############################  MATPLOTLIB  ########################################
    # Create an empty figure with no Axes
    # fig = plt.figure()  
    # Create a figure containing a single axes.
    fig, ax = plt.subplots()
    # Create a figure with a 2x2 grid of Axes
    # fig, axs = plt.subplots(2, 2)
    # Plot some data on the axes.
    # ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    # Tambien se puede hcer una Matplotlib plot.
    # plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
    # INTERACTIVE MODE
    # The next instruction will pop up a plot window 
    # but your terminal prompt will remain active
    # plt.ion()
    # plt.plot([1.6, 2.7])
    # NON INTERACTIVE MODE
    # plt.ioff()
    # plt.plot([1.6, 2.7])
    # CONTROLLING LINE PROPERTIES
    # Lines have many attributes that you can set: 
    # linewidth, dash style, antialiased, etc.
    # There are several ways to set line properties:
    # * Use keyword args:
    # plt.plot(x, y, linewidth=2.0)
    # * Use the setter methods of a Line2D instance. 
    # plot returns a list of Line2D objects. 
    # In the code below we will suppose that we have only 
    # one line so that the list returned is of length 1. 
    # We use tuple unpacking with line, to get the first 
    # element of that list: 
    ln, = plt.plot([], [], 'blue')
    # line.set_antialiased(False) # turn off antialiasing
    # * Use setp. The example below uses a MATLAB-style function 
    # to set multiple properties on a list of lines. setp works 
    # transparently with a list of objects or a single object. 
    # You can either use python keyword arguments or MATLAB-style 
    # string/value pairs:
    # lines = plt.plot(x1, y1, x2, y2)
    # use keyword args
    # plt.setp(lines, color='r', linewidth=2.0)
    # or MATLAB style string value pairs
    # plt.setp(lines, 'color', 'r', 'linewidth', 2.0)
    ax.set_xlim(0, muestras-1)
    ax.set_ylim(-0.2, 1.2)
    ##################################################################################
    
    ##################################################################################
    # Configuramos la función que "animará" nuestra gráfica
    # class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, 
    # fargs=None, save_count=None, *, cache_frame_data=True, **kwargs)
    ##################################################################################
    ani = FuncAnimation(fig, update, fargs = (ln, xdata, ydata, ax, lock, distancia), interval=100, blit=False)
    # Pintamos la linea
    plt.show()

# Función que actualizará los datos de la gráfica
# Se llama periódicamente desde la 'FuncAnimation'
def update(frame, ln_aux, dx, dy, ax, lock, aux):
    print('Martin')
    try:
        # Use the lock as a context manager
        with lock:
            dy.append(float(aux))
        if (len(dy) == muestras + 1):
            dx.append(frame)
            dx.pop(0)
            ax.set_xlim(dx[0], dx[-1])        
            dy.pop(0)
        else:
            dx.append(frame)
    except:
        pass
    dx = np.array(dx)
    dy = np.array(dy)
    ln_aux.set_data(dx,dy)
    return ln_aux,


# Configuramos y lanzamos los hilos encargados de:
# leer datos del serial,
# graficar los datos obtenidos.
if __name__ == "__main__":
    # create a lock
    lock = Lock()
    # create a Threads
    colectorDatos = Thread(target = getData, args=(lock,))
    graficoDatos =  Thread(target = aniGraf, args=(lock,))
    # init Threads
    colectorDatos.start()
    graficoDatos.start()

    colectorDatos.join()
    graficoDatos.join()


