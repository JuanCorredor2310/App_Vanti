"""import tkinter as tk
from tkinter import filedialog

# Crear una ventana raíz
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal

# Abrir el explorador de archivos y seleccionar un archivo
file_path = filedialog.askopenfilename()

# Mostrar la ruta del archivo seleccionado
print("Archivo seleccionado:", file_path)"""
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

categorias = ['Mar-2023', 'Abr-2023', 'Mayo-2023', 'Jun-2023','Mar-2024', 'Abr-2024', 'Mayo-2024', 'Jun-2024','Mar-2025', 'Abr-2025', 'Mayo-2025', 'Jun-2025']
valores = [130, 120, 110, 100,90, 80, 70, 60,50,40,30,20]
fig, ax = plt.subplots(figsize=(16, 10))
"""fig.patch.set_facecolor('#22405e')
ax.set_facecolor('#22405e')"""
bar = ax.bar(categorias,valores)
def gradientbars(bars,rotation=0):
    cmap = LinearSegmentedColormap.from_list("Hola", ["#924e8c","#c9a7c6"])
    grad = np.atleast_2d(np.linspace(0, 1, 256)).T
    grad = cmap(grad)
    ax = bars[0].axes
    lim = ax.get_xlim()+ax.get_ylim()
    for bar in bars:
        bar.set_zorder(1)
        bar.set_facecolor("none")
        x,y = bar.get_xy()
        w, h = bar.get_width(), bar.get_height()
        ax.imshow(grad, extent=[x,x+w,y,y+h], aspect="auto", zorder=0)
    ax.axis(lim)
    plt.xticks(rotation=rotation, size=20)
    plt.yticks(size=20)
gradientbars(bar, 45)
ax.set_title('Cantidad de usuarios Grupo Vanti', color='#14314a',fontsize=45)
ax.set_ylabel('Usuarios', color='#14314a',fontsize=28)
ax.tick_params(axis='x', colors='#14314a',size=0)
ax.tick_params(axis='y', colors='#14314a',size=0)
for spine in ax.spines.values():
    spine.set_visible(False)
plt.subplots_adjust(left=0.08, right=1.02, top=0.92, bottom=0.15)

plt.show()
#plt.savefig("i2.png")