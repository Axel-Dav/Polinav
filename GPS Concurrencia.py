# ==============================================================================
#                            SIMULADOR GPS CON CARGA Y CONCURRENCIA
# Alumno: Monroy Pastrana Leonardo
# Descripción: Sistema GPS urbano con simulación concurrente de camiones, registro
# y exportación de datos de viajes, empleando grafos con NetworkX y Tkinter.
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
import random
import json
import threading
import time
import csv

# ------------------------------ Clases de Estructura ------------------------------
class Nodo:
    def _init_(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def _init_(self):
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

# ---------------------------- Grafo y Funciones GPS ----------------------------
class GrafoFlexible:
    def _init_(self):
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
        if bidireccional and not self.adyacencia[v2].buscar(v1):
            self.adyacencia[v2].insertar(v1)
            self.grafo_nx.add_edge(v2, v1, weight=peso)

    def cargar_json(self, ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            for nodo in datos['nodos']:
                self.agregar_vertice(nodo['nombre'], nodo['posicion'])
            for calle in datos['calles']:
                self.agregar_arista(calle['origen'], calle['destino'], calle['peso'], calle['doble_sentido'])

    def mostrar(self):
        pos = self.posiciones if self.posiciones else nx.spring_layout(self.grafo_nx, seed=42)
        nx.draw(self.grafo_nx, pos, with_labels=True, node_size=2000, node_color='skyblue')
        etiquetas = nx.get_edge_attributes(self.grafo_nx, 'weight')
        nx.draw_networkx_edge_labels(self.grafo_nx, pos, edge_labels=etiquetas)
        plt.show()

class SistemaGPS:
    def _init_(self, grafo):
        self.grafo = grafo

    def buscar_ruta(self, origen, destino):
        try:
            ruta = nx.shortest_path(self.grafo.grafo_nx, source=origen, target=destino, weight='weight')
            tiempo = sum(self.grafo.grafo_nx[ruta[i]][ruta[i+1]]['weight'] for i in range(len(ruta)-1))
            return ruta, tiempo
        except:
            return [], 0

    def simular_trafico(self):
        for u, v in self.grafo.grafo_nx.edges:
            self.grafo.grafo_nx[u][v]['weight'] = random.randint(1, 10)
            if random.choice([True, False]):
                if not self.grafo.grafo_nx.has_edge(v, u):
                    self.grafo.grafo_nx.add_edge(v, u, weight=random.randint(1, 10))

# ----------------------------- Central de Camiones -----------------------------
class CentralCamiones:
    def _init_(self, gps, log_func, actualizar_estado):
        self.gps = gps
        self.log = log_func
        self.actualizar = actualizar_estado
        self.historial = []
        self.clientes_por_destino = {}

    def asignar_clientes(self, destinos, total_clientes):
        self.clientes_por_destino = {d: 0 for d in destinos}
        for _ in range(total_clientes):
            destino = random.choice(destinos)
            self.clientes_por_destino[destino] += 1

    def lanzar_camiones(self, cantidad, destinos):
        for i in range(1, cantidad+1):
            destino = destinos[i-1]
            threading.Thread(target=self.viajar, args=(i, destino)).start()

    def viajar(self, numero, destino):
        pasajeros_total = self.clientes_por_destino[destino]
        vueltas = 0
        while pasajeros_total > 0:
            self.actualizar(numero, "viaje", f"{destino}")
            self.gps.simular_trafico()
            pasajeros = min(20, pasajeros_total)
            ruta, tiempo = self.gps.buscar_ruta("Central", destino)
            self.log(f"[Camión {numero}] Sale con {pasajeros} pasajeros hacia {destino}")
            time.sleep(tiempo * 0.1)
            self.log(f"[Camión {numero}] Llegó a {destino}")

            self.actualizar(numero, "regresando", f"{destino}")
            ruta_back, t_back = self.gps.buscar_ruta(destino, "Central")
            time.sleep(t_back * 0.1)
            self.log(f"[Camión {numero}] Regresó a Central")
            vueltas += 1
            pasajeros_total -= pasajeros
            self.historial.append([numero, destino, pasajeros, tiempo, t_back, vueltas])

        self.actualizar(numero, "disponible", "Central")

    def exportar_csv(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".csv")
        if not archivo:
            return
        with open(archivo, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Camión", "Destino", "Pasajeros", "Tiempo Ida", "Tiempo Regreso", "Vueltas"])
            writer.writerows(self.historial)
        messagebox.showinfo("Exportación", "Datos exportados correctamente")

# ----------------------------- Interfaz Principal -----------------------------
class InterfazGPS:
    def _init_(self, ventana):
        self.ventana = ventana
        self.ventana.title("Simulador GPS - Monroy Pastrana Leonardo")
        self.ventana.geometry("800x600")

        self.grafo = GrafoFlexible()
        self.sistema = SistemaGPS(self.grafo)
        self.area_log = None

        self._crear_menu()
        self._crear_widgets()

    def _crear_menu(self):
        barra = tk.Menu(self.ventana)
        menu = tk.Menu(barra, tearoff=0)
        menu.add_command(label="Importar Mapa", command=self.importar_mapa)
        menu.add_command(label="Mostrar Mapa", command=self.grafo.mostrar)
        menu.add_separator()
        menu.add_command(label="Exportar CSV", command=lambda: self.central.exportar_csv())
        menu.add_separator()
        menu.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Menú", menu=menu)
        barra.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Autor", "Monroy Pastrana Leonardo"))
        self.ventana.config(menu=barra)

    def _crear_widgets(self):
        marco = tk.Frame(self.ventana)
        marco.pack(pady=10)

        tk.Label(marco, text="Clientes a llegar:").grid(row=0, column=0)
        self.entrada_clientes = tk.Entry(marco, width=5)
        self.entrada_clientes.grid(row=0, column=1)

        tk.Label(marco, text="Número de camiones:").grid(row=1, column=0)
        self.combo_camiones = ttk.Combobox(marco, values=[1, 2, 3, 4, 5], width=3)
        self.combo_camiones.grid(row=1, column=1)

        tk.Button(marco, text="Insertar Camiones", command=self.insertar_camiones).grid(row=1, column=2, padx=10)

        self.frame_destinos = tk.Frame(self.ventana)
        self.frame_destinos.pack()

        self.bot_simular = tk.Button(self.ventana, text="Iniciar Simulación", state="disabled", command=self.simular)
        self.bot_simular.pack(pady=5)

        self.area_log = tk.Text(self.ventana, height=12)
        self.area_log.pack(pady=5)

        self.marco_estado = tk.LabelFrame(self.ventana, text="Estado Camiones")
        self.marco_estado.pack(pady=5)
        self.labels_estado = {}

    def importar_mapa(self):
        archivo = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if archivo:
            self.grafo.cargar_json(archivo)
            messagebox.showinfo("Importado", "Mapa cargado")
            self.bot_simular.config(state="normal")

    def insertar_camiones(self):
        for widget in self.frame_destinos.winfo_children():
            widget.destroy()
        self.labels_estado.clear()

        cantidad = int(self.combo_camiones.get())
        nodos = [n for n in self.grafo.grafo_nx.nodes if n != "Central"]
        self.combo_destinos = []

        for i in range(cantidad):
            tk.Label(self.frame_destinos, text=f"Destino Camión {i+1}:").grid(row=i, column=0)
            combo = ttk.Combobox(self.frame_destinos, values=nodos)
            combo.grid(row=i, column=1)
            self.combo_destinos.append(combo)

            estado = tk.Label(self.marco_estado, text=f"Camión {i+1}: Disponible | Nodo: Central", bg="lightgreen")
            estado.pack(padx=2, pady=2, fill="x")
            self.labels_estado[i+1] = estado

    def simular(self):
        total_clientes = int(self.entrada_clientes.get())
        destinos = [c.get() for c in self.combo_destinos]
        self.central = CentralCamiones(self.sistema, self.log, self.actualizar_estado)
        self.central.asignar_clientes(destinos, total_clientes)
        self.central.lanzar_camiones(len(destinos), destinos)

    def log(self, texto):
        self.area_log.insert(tk.END, texto + "\n")
        self.area_log.see(tk.END)

    def actualizar_estado(self, num, estado, nodo):
        colores = {"viaje": "red", "regresando": "yellow", "disponible": "lightgreen"}
        textos = {"viaje": "En viaje", "regresando": "Regresando", "disponible": "Disponible"}
        if num in self.labels_estado:
            self.labels_estado[num].config(text=f"Camión {num}: {textos[estado]} | Nodo: {nodo}", bg=colores[estado])

# ------------------------------ Lanzamiento ------------------------------
if _name_ == '_main_':
    root = tk.Tk()
    app = InterfazGPS(root)
    root.mainloop()