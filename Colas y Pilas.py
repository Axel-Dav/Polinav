# ==============================================================================
#                              Colas y Pilas
# ==============================================================================
# Desarrollado por: Monroy Pastrana Leonardo, Rodríguez Mercado Axel David, Cayetano de la Cruz Axel Gustavo
# Proyecto: 
# Descripción: 
# ==============================================================================
# ==============================================================================
#                                 LIBRERIAS
# ==============================================================================
import tkinter as tk
from tkinter import messagebox
# ==============================================================================
#                              CLASES Y FUNCIONES
# ==============================================================================
class Cola:
    def __init__(self):
        self._cola = []

    def insertar(self, elemento):
        self._cola.append(elemento)

    def extraer(self):
        if self._cola:
            return self._cola.pop(0)
        return "La cola está vacía."

    def ver(self):
        if self._cola:
            return "\n".join(self._cola)
        return "La cola está vacía."

    def tamanio(self):
        return len(self._cola)

class Pila:
    def __init__(self):
        self._pila = []

    def insertar(self, elemento):
        self._pila.append(elemento)

    def extraer(self):
        if self._pila:
            return self._pila.pop()
        return "La pila está vacía."

    def ver(self):
        if self._pila:
            return "\n".join(self._pila)
        return "La pila está vacía."

    def tamanio(self):
        return len(self._pila)

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cola y Pila con Tkinter")
        self.geometry("450x350")
        self.cola = Cola()
        self.pila = Pila()
        self.crear_menu()

    def crear_menu(self):
        menu_principal = tk.Menu(self)

        menu_opciones = tk.Menu(menu_principal, tearoff=0)
        menu_opciones.add_command(label="Cola", command=self.ventana_cola)
        menu_opciones.add_command(label="Pila", command=self.ventana_pila)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Salir", command=self.quit)

        menu_archivo = tk.Menu(menu_principal, tearoff=0)
        menu_archivo.add_command(label="Acerca de", command=self.mostrar_info)

        menu_principal.add_cascade(label="Menú", menu=menu_opciones)
        menu_principal.add_cascade(label="Archivo", menu=menu_archivo)

        self.config(menu=menu_principal)

    def mostrar_info(self):
        messagebox.showinfo("Acerca de", "Monroy Pastrana Leonardo")


    def ventana_cola(self):
        ventana_cola = tk.Toplevel(self)
        ventana_cola.title("Operaciones con Cola")
        ventana_cola.geometry("450x400")

        tk.Label(ventana_cola, text="Elemento a insertar:").pack(pady=5)
        entrada = tk.Entry(ventana_cola, width=30)
        entrada.pack(pady=5)

        def insertar():
            elemento = entrada.get().strip()
            if elemento:
                self.cola.insertar(elemento)
                messagebox.showinfo("Éxito", f"Elemento '{elemento}' insertado en la cola.")
                entrada.delete(0, tk.END)
            else:
                messagebox.showwarning("Error", "Ingrese un elemento válido.")

        def ver():
            elementos = self.cola.ver()
            messagebox.showinfo("Elementos de la Cola", f"Cola:\n{elementos}")

        def total():
            total = self.cola.tamanio()
            messagebox.showinfo("Total de elementos", f"Total en cola: {total}")

        def extraer():
            elemento = self.cola.extraer()
            messagebox.showinfo("Elemento extraído", f"Elemento extraído: {elemento}")

        
        btn_insertar = tk.Button(ventana_cola, text="Insertar", command=insertar, width=20)
        btn_insertar.pack(pady=5)

        btn_ver = tk.Button(ventana_cola, text="Ver Cola", command=ver, width=20)
        btn_ver.pack(pady=5)

        btn_total = tk.Button(ventana_cola, text="Ver Total", command=total, width=20)
        btn_total.pack(pady=5)

        btn_extraer = tk.Button(ventana_cola, text="Extraer", command=extraer, width=20)
        btn_extraer.pack(pady=5)

    
    def ventana_pila(self):
        ventana_pila = tk.Toplevel(self)
        ventana_pila.title("Operaciones con Pila")
        ventana_pila.geometry("450x400")

        tk.Label(ventana_pila, text="Elemento a insertar:").pack(pady=5)
        entrada = tk.Entry(ventana_pila, width=30)
        entrada.pack(pady=5)

        def insertar():
            elemento = entrada.get().strip()
            if elemento:
                self.pila.insertar(elemento)
                messagebox.showinfo("Éxito", f"Elemento '{elemento}' insertado en la pila.")
                entrada.delete(0, tk.END)
            else:
                messagebox.showwarning("Error", "Ingrese un elemento válido.")

        def ver():
            elementos = self.pila.ver()
            messagebox.showinfo("Elementos de la Pila", f"Pila:\n{elementos}")

        def total():
            total = self.pila.tamanio()
            messagebox.showinfo("Total de elementos", f"Total en pila: {total}")

        def extraer():
            elemento = self.pila.extraer()
            messagebox.showinfo("Elemento extraído", f"Elemento extraído: {elemento}")

        boton_insertar = tk.Button(ventana_pila, text="Insertar", command=insertar, width=20)
        boton_insertar.pack(pady=5)

        boton_ver = tk.Button(ventana_pila, text="Ver Pila", command=ver, width=20)
        boton_ver.pack(pady=5)

        boton_total = tk.Button(ventana_pila, text="Ver Total", command=total, width=20)
        boton_total.pack(pady=5)

        boton_extraer = tk.Button(ventana_pila, text="Extraer", command=extraer, width=20)
        boton_extraer.pack(pady=5)
# ==============================================================================
#                               BLOQUE PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
