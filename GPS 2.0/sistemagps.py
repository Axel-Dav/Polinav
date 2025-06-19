# ==============================================================================
#                             Navegacion por GPS
# ==============================================================================
# Desarrollado por: Monroy Pastrana Leonardo, Rodríguez Mercado Axel David, Cayetano de la Cruz Axel Gustavo
# Proyecto: Navegación GPS
# Descripción: Aplicación interactiva hecha con pythonn POO para simular rutas 
# en una ciudad usando grafos dirigidos/no dirigidos, con simulación de tráfico 
# y visualización gráfica.
# ==============================================================================
# ==============================================================================
#                                 LIBRERIAS
# ==============================================================================
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
import random
import json
import os
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

class GrafoFlexible:
    def __init__(self):
        self.adyacencia = {}
        self.G = nx.DiGraph()
        self.posiciones = {}

    def agregarVertice(self, vertice, posicion=None):
        if vertice not in self.adyacencia:
            self.adyacencia[vertice] = ListaEnlazada()
            self.G.add_node(vertice)
            if posicion:
                self.posiciones[vertice] = tuple(posicion)

    def agregarArista(self, v1, v2, peso=1, bidireccional=False):
        self.agregarVertice(v1)
        self.agregarVertice(v2)
        if not self.adyacencia[v1].buscar(v2):
            self.adyacencia[v1].insertar(v2)
            self.G.add_edge(v1, v2, weight=peso)
        if bidireccional:
            if not self.adyacencia[v2].buscar(v1):
                self.adyacencia[v2].insertar(v1)
                self.G.add_edge(v2, v1, weight=peso)

    def mostrar(self, ruta_resaltada=None):
        pos = self.posiciones if self.posiciones else nx.spring_layout(self.G, seed=42)
        nx.draw(self.G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, arrows=True)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        if ruta_resaltada:
            edges = list(zip(ruta_resaltada, ruta_resaltada[1:]))
            nx.draw_networkx_edges(self.G, pos, edgelist=edges, edge_color='red', width=2)
        plt.title("Mapa de tráfico urbano")
        plt.show()

    def cargarDesdeJson(self, archivo):
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)

                for nodo in datos["nodos"]:
                    nombre = nodo["nombre"]
                    posicion = nodo.get("posicion")
                    self.agregarVertice(nombre, posicion)

                for arista in datos["calles"]:
                    origen = arista["origen"]
                    destino = arista["destino"]
                    peso = arista["peso"]
                    doble = arista["doble_sentido"]
                    self.agregarArista(origen, destino, peso, bidireccional=doble)
        except Exception as e:
            messagebox.showerror("Error al cargar mapa", str(e))

class SistemaGPS:
    def __init__(self, grafo):
        self.calle = grafo
        ruta = os.path.join(os.path.dirname(__file__), "mapa.json")
        self.calle.cargarDesdeJson(ruta)

    def buscarRuta(self, origen, destino):
        if origen not in self.calle.G.nodes or destino not in self.calle.G.nodes:
            messagebox.showerror("Error", "Puntos del mapa no encontrados.")
            return

        try:
            ruta = nx.shortest_path(self.calle.G, source=origen, target=destino, weight='weight')
            tiempo_total = 0
            for i in range(len(ruta) - 1):
                u = ruta[i]
                v = ruta[i + 1]
                tiempo_total += self.calle.G[u][v]['weight']

            mensaje = (
                f"Ruta más corta:\n{' ➝ '.join(ruta)}"
                f"\n\nTiempo estimado: {tiempo_total} minutos"
            )
            messagebox.showinfo("Ruta más corta", mensaje)
            self.calle.mostrar(ruta_resaltada=ruta)

        except nx.NetworkXNoPath:
            messagebox.showerror("Sin ruta", "No hay ruta entre esos puntos.")

    def simularTrafico(self):
        for u, v in self.calle.G.edges:
            self.calle.G[u][v]['weight'] = random.randint(1, 10)
        messagebox.showinfo("Tráfico actualizado", "Se ha simulado nuevo tráfico.")
        self.calle.mostrar()

class InterfazGPS:
    def __init__(self, ventana):
        self.grafo = GrafoFlexible()
        self.sistema = SistemaGPS(self.grafo)

        self.ventana = ventana
        self.ventana.title("Sistema GPS Urbano")
        self.ventana.geometry("400x300")

        tk.Label(ventana, text="Seleccione punto de origen:").pack(pady=5)
        self.origen = ttk.Combobox(ventana, values=list(sorted(self.grafo.G.nodes)))
        self.origen.pack()

        tk.Label(ventana, text="Seleccione punto de destino:").pack(pady=5)
        self.destino = ttk.Combobox(ventana, values=list(sorted(self.grafo.G.nodes)))
        self.destino.pack()

        tk.Button(ventana, text="Buscar ruta más corta", command=self.buscarRuta).pack(pady=10)
        tk.Button(ventana, text="Ver mapa actual", command=self.verMapa).pack()
        tk.Button(ventana, text="Simular tráfico", command=self.sistema.simularTrafico).pack(pady=10)
        tk.Button(ventana, text="Acerca de", command=self.mostrarInfo).pack(pady=5)
        tk.Button(ventana, text="Salir", command=self.ventana.quit).pack(pady=5)

    def buscarRuta(self):
        self.sistema.buscarRuta(self.origen.get().strip(), self.destino.get().strip())

    def verMapa(self):
        self.grafo.mostrar()

    def mostrarInfo(self):
        messagebox.showinfo("Acerca de", "Programa desarrollado por: Monroy Pastrana Leonardo \nRodríguez Mercado Axel David")
# ==============================================================================
#                               BLOQUE PRINCIPAL
# ==============================================================================
if __name__ == '__main__':
    ventana = tk.Tk()
    sistema = InterfazGPS(ventana)
    ventana.mainloop()
