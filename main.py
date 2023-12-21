import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.widgets import Button, Slider

V_SOUND = 343
L_X = 1
L_Y = 1
p = 10
q = 10

#r mode not represented in this visual
#assume Z dimension of cavity is much smaller than the X and Y dimensions
fig = plt.figure()
ax = fig.add_subplot(3,1, (1,2), projection="3d")
ax.set_title("Plot of a Standing Sound Wave in Cubic Cavity (1m x 1m x Xm)")
ax.set_xlabel("X Dimension")
ax.set_ylabel("Y Dimension")
ax.set_zlabel("Pressure Amplitude")
X,Y = np.mgrid[0:L_X:500j, 0:L_Y:500j]

def standing_wave(x, y, p, q):
    return np.cos(p * np.pi * x)*np.cos((q * np.pi * y) / 2) 

def resonate_frequency(p, q):
    resF = V_SOUND/2 * np.sqrt((p / L_X)**2 + (q / L_Y)**2)
    truncated_resF = math.trunc(resF)
    str_trf = str(truncated_resF)
    return str_trf + " Hz"
    
Z = standing_wave(X, Y, p, q)
l = ax.plot_surface(X, Y, Z, cmap="cividis_r", lw=0.5, rstride=1, cstride=1)

allowed_pq = np.linspace(0, 10, 11)

#create slider objects/ axes for sliders
ax1 = fig.add_axes([0.14, 0.26, 0.77, 0.05])
ax2 = fig.add_axes([0.14, 0.22, 0.77, 0.05])

slider_p = Slider(ax1, label = "p Slider", valmin = allowed_pq[0], valmax = allowed_pq[allowed_pq.size-1],
                valstep=1, orientation="horizontal", valinit=allowed_pq[allowed_pq.size-1]) 

slider_q = Slider(ax2,label = "q Slider", valmin = allowed_pq[0], valmax = allowed_pq[allowed_pq.size-1], 
                valstep=1, orientation="horizontal", valinit=allowed_pq[allowed_pq.size-1])

ax_reset = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(ax_reset,'Reset', hovercolor='0.5')

fig.text(.14, .1, "Frequency: ")
f_text = fig.text(.28, .1, resonate_frequency(p,q))

#reset button
def reset(event):
    slider_q.reset()
    slider_p.reset() 
button.on_clicked(reset)

def update(val):
    p = slider_p.val
    q = slider_q.val
    reset_plot()
    Z = standing_wave(X, Y, p, q)
    l = ax.plot_surface(X, Y, Z, cmap="cividis_r", lw=0.5, rstride=1, cstride=1)
    reset_text(p, q)
    fig.canvas.draw_idle()

def reset_plot():
    ax.cla()
    ax.set_title("Plot of a Standing Sound Wave in Cubic Cavity (1m x 1m x Xm)")
    ax.set_xlabel("X Dimension")
    ax.set_ylabel("Y Dimension")
    ax.set_zlabel("Pressure Amplitude")

def reset_text(p, q):
    del fig.texts[-1]
    f_text = fig.text(.28, .1, resonate_frequency(p,q))
    
slider_q.on_changed(update)
slider_p.on_changed(update)

plt.show()
