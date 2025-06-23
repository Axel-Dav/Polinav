
# =============================== SIMULADOR GPS CON CARGA ===============================
# Alumno: Monroy Pastrana Leonardo
# Descripción: Sistema GPS con visualización de rutas y simulación concurrente de camiones
# =======================================================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
import random
import json
import os
import threading
import time
import csv

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

class GrafoFlexible:
    def __init__(self):
        self.adyacencia = {}
        self.grafo_nx = nx.DiGraph()
        self.posiciones = {}

    def agregar_vertice(self, vertice, posicion=None):
        if vertice not in self.adyacencia:
            self.adyacencia[vertice] = ListaEnlazada()
            self.grafo_nx.add_node(vertice)
            if posicion:
                self.posiciones[vertice] = tuple(posicion)

    def agregar_arista(self, origen, destino, peso=1, bidireccional=False):
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        if not self.adyacencia[origen].buscar(destino):
            self.adyacencia[origen].insertar(destino)
            self.grafo_nx.add_edge(origen, destino, weight=peso)
        if bidireccional:
            if not self.adyacencia[destino].buscar(origen):
                self.adyacencia[destino].insertar(origen)
                self.grafo_nx.add_edge(destino, origen, weight=peso)

    def mostrar(self):
        pos = self.posiciones if self.posiciones else nx.spring_layout(self.grafo_nx, seed=42)
        nx.draw(self.grafo_nx, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, arrows=True)
        etiquetas = nx.get_edge_attributes(self.grafo_nx, 'weight')
        nx.draw_networkx_edge_labels(self.grafo_nx, pos, edge_labels=etiquetas)
        plt.title("Mapa de tráfico urbano")
        plt.show()

    def cargar_desde_json(self, archivo):
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
                for nodo in datos["nodos"]:
                    self.agregar_vertice(nodo["nombre"], nodo.get("posicion"))
                for arista in datos["calles"]:
                    self.agregar_arista(arista["origen"], arista["destino"], arista["peso"], arista["doble_sentido"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el mapa: {str(e)}")

class SistemaGPS:
    def __init__(self, grafo):
        self.grafo = grafo

    def buscar_ruta(self, origen, destino):
        try:
            ruta = nx.shortest_path(self.grafo.grafo_nx, source=origen, target=destino, weight='weight')
            tiempo_total = sum(self.grafo.grafo_nx[ruta[i]][ruta[i+1]]['weight'] for i in range(len(ruta)-1))
            return ruta, tiempo_total
        except nx.NetworkXNoPath:
            return [], None

    def simular_trafico(self):
        for u, v in self.grafo.grafo_nx.edges:
            self.grafo.grafo_nx[u][v]['weight'] = random.randint(1, 10)

class InterfazGPS:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Simulador GPS Concurrente")
        self.ventana.geometry("600x500")

        self.grafo = GrafoFlexible()
        self.sistema = SistemaGPS(self.grafo)
        self.historial = []

        self._crear_menu()
        self._crear_interfaz()

    def _crear_menu(self):
        barra = tk.Menu(self.ventana)
        menu_archivo = tk.Menu(barra, tearoff=0)
        menu_archivo.add_command(label="Importar mapa", command=self.importar_mapa)
        menu_archivo.add_command(label="Mostrar mapa", command=self.grafo.mostrar)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Menú", menu=menu_archivo)

        barra.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Autor", "Monroy Pastrana Leonardo"))
        self.ventana.config(menu=barra)

    def _crear_interfaz(self):
        frame = tk.Frame(self.ventana)
        frame.pack(pady=10)

        tk.Label(frame, text="Origen:").grid(row=0, column=0)
        self.combo_origen = ttk.Combobox(frame)
        self.combo_origen.grid(row=0, column=1)

        tk.Label(frame, text="Destino:").grid(row=1, column=0)
        self.combo_destino = ttk.Combobox(frame)
        self.combo_destino.grid(row=1, column=1)

        tk.Button(frame, text="Buscar Ruta", command=self.buscar_ruta).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Simular tráfico", command=self.simular_trafico).grid(row=3, column=0, columnspan=2)

    def importar_mapa(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if archivo:
            self.grafo.cargar_desde_json(archivo)
            nodos = list(self.grafo.grafo_nx.nodes)
            self.combo_origen["values"] = nodos
            self.combo_destino["values"] = nodos
            messagebox.showinfo("Mapa cargado", "Mapa importado exitosamente.")

    def buscar_ruta(self):
        origen = self.combo_origen.get()
        destino = self.combo_destino.get()
        ruta, tiempo = self.sistema.buscar_ruta(origen, destino)
        if ruta:
            mensaje = f"Ruta: {' ➝ '.join(ruta)}
Tiempo estimado: {tiempo} min"
            messagebox.showinfo("Ruta encontrada", mensaje)
            self.grafo.mostrar()
        else:
            messagebox.showerror("Error", "No hay ruta entre esos puntos.")

    def simular_trafico(self):
        self.sistema.simular_trafico()
        messagebox.showinfo("Tráfico", "Tráfico simulado.")
        self.grafo.mostrar()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGPS(root)
    root.mainloop()
