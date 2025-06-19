# ==============================================================================
#                             Navegacion por GPS
# ==============================================================================
# Desarrollado por: Monroy Pastrana Leonardo, Rodríguez Mercado Axel David, Cayetano de la Cruz Axel Gustavo
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
import random
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
        nuevoNodo = Nodo(dato)
        if not self.inicio:
            self.inicio = nuevoNodo
        else:
            actual = self.inicio
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevoNodo

    def buscar(self, dato):
        actual = self.inicio
        while actual:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

class GrafoDirigido:
    def __init__(self):
        self.adyacencia = {}
        self.G = nx.DiGraph()

    def agregarVertice(self, vertice):
        if vertice not in self.adyacencia:
            self.adyacencia[vertice] = ListaEnlazada()
            self.G.add_node(vertice)

    def agregarAristaDirigida(self, v1, v2, peso=1):
        self.agregarVertice(v1)
        self.agregarVertice(v2)
        if not self.adyacencia[v1].buscar(v2):
            self.adyacencia[v1].insertar(v2)
            self.G.add_edge(v1, v2, weight=peso)

    def mostrar(self, ruta_resaltada=None):
        pos = nx.spring_layout(self.G, seed=42)
        nx.draw(self.G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, arrows=True)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        if ruta_resaltada:
            edges = list(zip(ruta_resaltada, ruta_resaltada[1:]))
            nx.draw_networkx_edges(self.G, pos, edgelist=edges, edge_color='red', width=2)
        plt.title("Mapa de tráfico urbano")
        plt.show()

class SistemaGPS:
    def __init__(self, grafo):
        self.calle = grafo

    def mapa(self):
        lugares = [
            ("Farmacia", "Cafe 1", 2), ("Cafe 1", "Plaza 1", 3), ("Plaza 1", "Casa 1", 2),
            ("Casa 1", "Casa 2", 4), ("Casa 2", "Oxxo 1", 1), ("Oxxo 1", "Hospital 1", 5),
            ("Farmacia", "Escuela", 3), ("Escuela", "Gimnasio", 4), ("Gimnasio", "Museo", 6),
            ("Museo", "Cafe 2", 2), ("Cafe 2", "Casa 3", 3), ("Casa 3", "Casa 4", 2),
            ("Casa 4", "Oxxo 2", 2), ("Oxxo 2", "Hospital 2", 1), ("Hospital 2", "Parque", 3),
            ("Parque", "Casa 5", 2), ("Casa 5", "Plaza 2", 3), ("Plaza 2", "Casa 6", 1),
            ("Casa 6", "Escuela", 4), ("Plaza 1", "Parque", 3)
        ]
        for origen, destino, peso in lugares:
            self.calle.agregarAristaDirigida(origen, destino, peso)

    def buscarRuta(self, origen, destino):
        if origen not in self.calle.G.nodes or destino not in self.calle.G.nodes:
            messagebox.showerror("Error", "Puntos del mapa no encontrados.")
            return

        try:
            ruta = nx.shortest_path(self.calle.G, source=origen, target=destino, weight='weight')
            messagebox.showinfo("Ruta más corta", f"{' ➝ '.join(ruta)}")
            self.calle.mostrar(ruta_resaltada=ruta)
        except nx.NetworkXNoPath:
            messagebox.showerror("Sin ruta", "No hay ruta entre esos puntos.")

    def simularTrafico(self):
        for u, v in self.calle.G.edges:
            self.calle.G[u][v]['weight'] = random.randint(1, 10)
        messagebox.showinfo("Tráfico actualizado", "Se ha simulado nuevo tráfico.")
        self.calle.mostrar()

class InterfazGPS:
    def __init__(self, root):
        self.grafo = GrafoDirigido()
        self.sistema = SistemaGPS(self.grafo)
        self.sistema.mapa()

        self.root = root
        self.root.title("Sistema GPS Urbano")
        self.root.geometry("400x300")

        tk.Label(root, text="Seleccione punto de origen:").pack(pady=5)
        self.origen = ttk.Combobox(root, values=list(sorted(self.grafo.G.nodes)))
        self.origen.pack()

        tk.Label(root, text="Seleccione punto de destino:").pack(pady=5)
        self.destino = ttk.Combobox(root, values=list(sorted(self.grafo.G.nodes)))
        self.destino.pack()

        tk.Button(root, text="Buscar ruta más corta", command=self.buscarRuta).pack(pady=10)
        tk.Button(root, text="Ver mapa actual", command=self.verMapa).pack()
        tk.Button(root, text="Simular tráfico", command=self.sistema.simularTrafico).pack(pady=10)
        tk.Button(root, text="Salir", command=self.root.quit).pack(pady=5)

    def buscarRuta(self):
        self.sistema.buscarRuta(self.origen.get().strip(), self.destino.get().strip())

    def verMapa(self):
        self.grafo.mostrar()
# ==============================================================================
#                               BLOQUE PRINCIPAL
# ==============================================================================
if __name__ == '__main__':
    ventana = tk.Tk()
    sistema = InterfazGPS(ventana)
    ventana.mainloop()
