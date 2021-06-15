import serial
import time
import numpy as np        
import matplotlib.pyplot as plt
from multiprocessing import Process, Lock, Array
from matplotlib.animation import FuncAnimation

muestras = 60
xdata = []
ydata = []
for _ in range(muestras):
    xdata.append(_)
    ydata.append(0.0)

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
ax.set_xlim(0, muestras)
ax.set_ylim(-0.2, 1.2)
##################################################################################
try:
   serialArduino = serial.Serial("/dev/tty.usbmodem11101",9600,timeout=1.0)
   #timeout (1 segundo) o tiempo máximo de espera para una lectura.
except:
   print("Cannot conect to the port")
time.sleep(1) # espera 1 seg, para dar tiempo a conectarse

# Función que se va a ejecutar en otro thread
# y que guardará los datos del serial en 'ydata'
def getData(y_out, lock):
    global serialArduino, muestras
    while True:
        cad = serialArduino.readline().decode('ascii').strip()
        try:
            aux = y_out[:] 
            aux.append(float(cad))
            if (len(aux) > muestras):
                aux.pop(0)
            with lock:
                y_out[:] = aux[:]
        except:
            print("Error en la función getData()")
        # finally:
        #     time.sleep(0.005)    

def graf_real_time(ln_aux, dx, dy, lock):
    global fig 
    # Función que actualizará los datos de la gráfica
    # Se llama periódicamente desde el 'FuncAnimation'
    def update(frame, ln_aux, dx, dy):    
        dx = np.array(dx)
        with lock:
            dy = np.array(dy)
            ln_aux.set_data(dx,dy)
        return ln_aux,
##################################################################################
# Configuramos la función que "animará" nuestra gráfica
# class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, 
# fargs=None, save_count=None, *, cache_frame_data=True, **kwargs)
##################################################################################
    ani = FuncAnimation(fig, update, fargs = (ln_aux, dx, dy), interval=100, blit=False)
# To save the animation, use e.g.
# ani.save("movie.mp4")
# or
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)
##################################################################################
    # Pintamos la linea
    plt.show()

# Lanzamos el multiptoceso encargado de leer datos del serial
if __name__ == '__main__':

    # create a lock
    lock = Lock()

    # Array(type, value): Create a ctypes array with elements of type type. 
    # Access the values with [].
    ydata = np.array(ydata)
    array_com = Array('f', ydata)
    # cola = Queue()

    # create processes and asign a function for each process
    pro_GD = Process(target = getData, args=(array_com, lock))
    pro_ani = Process(target = graf_real_time, args=(ln, xdata, array_com, lock))
    
    # Start a process
    pro_GD.start()
    pro_ani.start()
    # con process.join () el programa debe esperar a que este proceso 
    # se complete antes de continuar con el resto del código.
    pro_GD.join()
    pro_ani.join()

