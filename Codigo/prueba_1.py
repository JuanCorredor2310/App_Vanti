import tkinter as tk

def mostrar_datos():
    nombre = entrada_nombre.get()
    edad = entrada_edad.get()
    etiqueta_resultado.config(text=f"Hola {nombre}, tienes {edad} años.")

ventana = tk.Tk()
ventana.title("VANTI v1.0")

etiqueta_nombre = tk.Label(ventana, text="Nombre:")
etiqueta_nombre.pack()
entrada_nombre = tk.Entry(ventana)
entrada_nombre.pack()

etiqueta_edad = tk.Label(ventana, text="Edad:")
etiqueta_edad.pack()
entrada_edad = tk.Entry(ventana)
entrada_edad.pack()

boton_enviar = tk.Button(ventana, text="Enviar", command=mostrar_datos)
boton_enviar.pack()

etiqueta_resultado = tk.Label(ventana, text="")
etiqueta_resultado.pack()

ventana.mainloop()