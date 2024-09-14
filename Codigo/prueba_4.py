import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Crear datos de ejemplo: eventos a diferentes horas del día
data = pd.DataFrame({
    'hora': ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'],
    'eventos': [5, 15, 30, 25, 10, 20, 15, 10],
    'informacion': ['Info A', 'Info B', 'Info C', 'Info D', 'Info E', 'Info F', 'Info G', 'Info H']
})

# Convertir las horas a formato de 24 horas para el gráfico
data['hora'] = pd.to_datetime(data['hora'], format='%H:%M').dt.hour + pd.to_datetime(data['hora'], format='%H:%M').dt.minute / 60

# Configurar el gráfico
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

# Convertir los datos de horas a radianes
theta = np.deg2rad(data['hora'] * 15)  # Convertir a radianes (360 grados / 24 horas = 15 grados por hora)

# Dibujar el gráfico de reloj
bars = ax.bar(theta, data['eventos'], width=0.1, color='b', edgecolor='k', alpha=0.7)

# Añadir información a cada parte del reloj
for bar, angle, info in zip(bars, theta, data['informacion']):
    # Ajustar el ángulo de la etiqueta para que sea legible
    angle_deg = np.rad2deg(angle)
    if angle_deg < 0:
        angle_deg += 360
    
    # Ajustar la posición de la etiqueta
    x = angle
    y = bar.get_height() + 2  # Ajustar la distancia de la etiqueta desde la barra
    
    ax.text(x, y, info, fontsize=12, ha='center', va='bottom', rotation=np.rad2deg(angle) - 90, rotation_mode='anchor')

# Configurar el gráfico
ax.set_yticklabels([])
ax.set_xticks(np.deg2rad(np.linspace(0, 360, 24, endpoint=False)))
ax.set_xticklabels([f'{h:02d}:00' for h in range(24)], rotation=45)

plt.title('Distribución de Eventos a lo Largo del Día')
plt.show()