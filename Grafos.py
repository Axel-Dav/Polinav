# ==============================================================================
#                                  GRAFOS
# ==============================================================================
# Desarrollado por: Monroy Pastrana Leonardo, Rodríguez Mercado Axel David,Cayetano de la Cruz Axel Gustavo
# Proyecto: Navegación GPS
# Descripción: 
# ==============================================================================
# ==============================================================================
#                                 LIBRERIAS
# ==============================================================================
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
# ==============================================================================
#                              CLASES Y FUNCIONES
# ==============================================================================
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.inicio = None

    def insertar(self, dato):
        nuevo = Nodo(dato)
        if not self.inicio:
            self.inicio = nuevo
        else:
            actual = self.inicio
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def buscar(self, dato):
        actual = self.inicio
        while actual:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def obtener_todos(self):
        actual = self.inicio
        datos = []
        while actual:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos

class Grafo:
    def __init__(self, dirigido=False, ponderado=False):
        self.dirigido = dirigido
        self.ponderado = ponderado
        self.adyacencia = {}
        self.G = nx.DiGraph() if dirigido else nx.Graph()

    def agregarVertice(self, vertice):
        if vertice not in self.adyacencia:
            self.adyacencia[vertice] = ListaEnlazada()
            self.G.add_node(vertice)

    def agregarArista(self, v1, v2, peso=1):
        self.agregarVertice(v1)
        self.agregarVertice(v2)
        if not self.adyacencia[v1].buscar(v2):
            self.adyacencia[v1].insertar(v2)
            self.G.add_edge(v1, v2, weight=peso)
        if not self.dirigido and not self.adyacencia[v2].buscar(v1):
            self.adyacencia[v2].insertar(v1)
            self.G.add_edge(v2, v1, weight=peso)

    def mostrar(self):
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, arrows=self.dirigido)
        if self.ponderado:
            labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        plt.title("Grafo Dirigido" if self.dirigido else "Grafo No Dirigido")
        plt.show()

class InterfazGrafo:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Constructor de Grafos")
        self.grafo = None

        self.dirigido = tk.BooleanVar()
        self.ponderado = tk.BooleanVar()

        ttk.Label(ventana, text="Configuración del grafo:").pack()
        ttk.Checkbutton(ventana, text="Grafo dirigido", variable=self.dirigido).pack()
        ttk.Checkbutton(ventana, text="Conexiones ponderadas", variable=self.ponderado).pack()
        ttk.Button(ventana, text="Crear grafo", command=self.GenerarGrafo).pack(pady=5)

        self.entrada = ttk.Frame(ventana)
        self.entrada.pack()

        ttk.Label(self.entrada, text="Nodo 1:").grid(row=0, column=0)
        ttk.Label(self.entrada, text="Nodo 2:").grid(row=1, column=0)
        ttk.Label(self.entrada, text="Peso:").grid(row=2, column=0)

        self.nodo1 = ttk.Entry(self.entrada)
        self.nodo2 = ttk.Entry(self.entrada)
        self.peso = ttk.Entry(self.entrada)

        self.nodo1.grid(row=0, column=1)
        self.nodo2.grid(row=1, column=1)
        self.peso.grid(row=2, column=1)

        ttk.Button(self.entrada, text="Agregar conexión", command=self.GenerarArista).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(ventana, text="Mostrar grafo", command=self.mostrar_grafo).pack(pady=5)

    def GenerarGrafo(self):
        self.grafo = Grafo(dirigido=self.dirigido.get(), ponderado=self.ponderado.get())
        messagebox.showinfo("Info", "Grafo creado correctamente")

    def GenerarArista(self):
        if not self.grafo:
            messagebox.showerror("Error", "Primero crea el grafo")
            return
        v1 = self.nodo1.get().strip()
        v2 = self.nodo2.get().strip()
        if not v1 or not v2:
            messagebox.showerror("Error", "Debe ingresar ambos nodos")
            return
        peso = 1
        if self.ponderado.get():
            try:
                peso = int(self.peso.get())
            except ValueError:
                messagebox.showerror("Error", "Peso inválido")
                return
        self.grafo.agregarArista(v1, v2, peso)
        messagebox.showinfo("Éxito", f"Conexión {v1} -> {v2} agregada")

    def mostrar_grafo(self):
        if self.grafo:
            self.grafo.mostrar()
        else:
            messagebox.showwarning("Advertencia", "Primero debe crear el grafo")
# ==============================================================================
#                               BLOQUE PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    inicio = tk.Tk()
    app = InterfazGrafo(inicio)
    inicio.mainloop()
