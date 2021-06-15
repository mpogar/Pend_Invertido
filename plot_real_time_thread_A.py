########################  FUNCIONA BIEN  #########################################

import serial
import time
import threading
import numpy as np        
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

muestras = 6
xdata = []
ydata = []
for i in range(muestras):
    xdata.append(i)
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
ln, = plt.plot([], [], 'b')
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

try:
   serialArduino = serial.Serial("/dev/tty.usbmodem11101",9600,timeout=1.0)
   #timeout (1 segundo) o tiempo máximo de espera para una lectura.
except:
   print("Cannot conect to the port")
time.sleep(1) # espera 1 seg, para dar tiempo a conectarse

# Función que actualizará los datos de la gráfica
# Se llama periódicamente desde el 'FuncAnimation'
def update(frame, ln_aux, dx, dy):
    dx = np.array(dx)
    dy = np.array(dy)
    ln_aux.set_data(dx,dy)
    return ln_aux,

# Función que se va a ejecutar en otro thread
# y que guardará los datos del serial en 'ydata'
def getData(y_out):
    while True:
        cad = serialArduino.readline().decode('ascii').strip()
        try:
            y_out.append(float(cad))
            if (len(y_out) > muestras):
                y_out.pop(0)
        except:
            print("Error en la función getData()")

# Configuramos y lanzamos el hilo encargado de leer datos del serial
# serialArduino.reset_input_buffer()
colectorDatos = threading.Thread(target = getData, args=(ydata,))
colectorDatos.start()

##################################################################################
# Configuramos la función que "animará" nuestra gráfica
# class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, 
# fargs=None, save_count=None, *, cache_frame_data=True, **kwargs)
##################################################################################
ani = FuncAnimation(fig, update, fargs = (ln, xdata, ydata), interval=1, blit=True)
# To save the animation, use e.g.
# ani.save("movie.mp4")
# or
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)
##################################################################################

# Pintamos la linea
plt.show()

# Unimos el hilo principal y el hijo para que cuando muera uno, muera el otro
colectorDatos.join()
