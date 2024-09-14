import matplotlib.pyplot as plt
import numpy as np

def draw_gauge(value, min_value=0, max_value=100, title="Gauge Chart"):
    # Crear el ángulo del gráfico (un semicírculo de 180 grados)
    theta = np.linspace(0, np.pi, 100)
    
    # Radio del semicírculo
    radius = 1
    
    # Coordenadas para el fondo del medidor
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={'aspect': 'equal'})

    # Dibujar la base del medidor
    ax.plot(x, y, color='black', lw=2)
    ax.fill_between(x, 0, y, color='lightgray')

    # Dibujar las marcas del medidor
    num_ticks = 10
    for i in range(num_ticks + 1):
        angle = np.pi * i / num_ticks
        x0, y0 = [0, np.cos(angle)], [0, np.sin(angle)]
        ax.plot(x0, y0, color='black')

    # Calcular el ángulo de la aguja
    angle = np.pi * (value - min_value) / (max_value - min_value)

    # Dibujar la aguja del medidor
    ax.arrow(0, 0, 0.9 * np.cos(angle), 0.9 * np.sin(angle), head_width=0.1, head_length=0.2, fc='red', ec='red')

    # Añadir texto para el valor actual
    ax.text(0, -0.1, f'{value}', fontsize=20, ha='center', va='center')

    # Añadir el título
    plt.title(title, fontsize=20, pad=20)
    
    # Ocultar ejes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.5, 1.1)

    plt.show()

# Ejemplo de uso
draw_gauge(value=75, min_value=0, max_value=100, title="Velocímetro")