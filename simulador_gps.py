
# =================== Simulador GPS con Concurrencia ===================
# Desarrollado por: Monroy Pastrana Leonardo
# Descripción: Simulador de transporte con camiones concurrentes en una ciudad.
# Incluye importación/exportación de datos y seguimiento de estado.

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
        nuevo_nodo = Nodo(dato)
        if not self.inicio:
            self.inicio = nuevo_nodo
        else:
            actual = self.inicio
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

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

    def agregar_arista(self, v1, v2, peso=1, bidireccional=False):
        self.agregar_vertice(v1)
        self.agregar_vertice(v2)
        if not self.adyacencia[v1].buscar(v2):
            self.adyacencia[v1].insertar(v2)
            self.grafo_nx.add_edge(v1, v2, weight=peso)
        if bidireccional:
            if not self.adyacencia[v2].buscar(v1):
                self.adyacencia[v2].insertar(v1)
                self.grafo_nx.add_edge(v2, v1, weight=peso)

    def mostrar(self):
        pos = self.posiciones if self.posiciones else nx.spring_layout(self.grafo_nx, seed=42)
        nx.draw(self.grafo_nx, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, arrows=True)
        etiquetas_aristas = nx.get_edge_attributes(self.grafo_nx, 'weight')
        nx.draw_networkx_edge_labels(self.grafo_nx, pos, edge_labels=etiquetas_aristas)
        plt.title("Mapa de tráfico urbano")
        plt.show()

    def cargar_desde_json(self, archivo):
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
                for nodo in datos["nodos"]:
                    nombre = nodo["nombre"]
                    posicion = nodo.get("posicion")
                    self.agregar_vertice(nombre, posicion)
                for arista in datos["calles"]:
                    origen = arista["origen"]
                    destino = arista["destino"]
                    peso = arista["peso"]
                    doble = arista["doble_sentido"]
                    self.agregar_arista(origen, destino, peso, bidireccional=doble)
        except Exception as e:
            messagebox.showerror("Error al cargar mapa", str(e))

class SistemaGPS:
    def __init__(self, grafo):
        self.calle = grafo

    def buscar_ruta(self, origen, destino):
        try:
            ruta = nx.shortest_path(self.calle.grafo_nx, source=origen, target=destino, weight='weight')
            tiempo_total = sum(self.calle.grafo_nx[ruta[i]][ruta[i+1]]['weight'] for i in range(len(ruta)-1))
            return ruta, tiempo_total
        except nx.NetworkXNoPath:
            return [], None

    def simular_trafico(self):
        for u, v in self.calle.grafo_nx.edges:
            self.calle.grafo_nx[u][v]['weight'] = random.randint(1, 10)

# El resto del código se agregará en el siguiente paso por límite de longitud
