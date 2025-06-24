# ==============================================================================
#                                   ENCABEZADO
# ==============================================================================
# Integrantes: Monroy Pastrana Leonardo, Rodríguez Mercado Axel David, 
#              Cayetano de la Cruz Axel Gustavo
# Proyecto: PoliNav - Simulador de Camiones con GPS y Concurrencia
# Descripción: Simulador interactivo que utiliza grafos para representar rutas 
# urbanas y coordina concurrentemente el recorrido de camiones que transportan pasajeros 
# desde una central a múltiples destinos. Permite simular tráfico, importar mapas 
# en formato JSON, exportar registros en CSV, y gestionar visualmente el estado 
# de cada camión en tiempo real.
# ==============================================================================

# ==============================================================================
#                                   LIBRERÍAS
# ==============================================================================
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import random
import json
import csv
import networkx as nx
import matplotlib.pyplot as plt

# ==============================================================================
#                            CLASES Y FUNCIONES
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
        if bidireccional and not self.adyacencia[v2].buscar(v1):
            self.adyacencia[v2].insertar(v1)
            self.grafo_nx.add_edge(v2, v1, weight=peso)

    def mostrar(self):
        plt.clf()
        pos = self.posiciones if self.posiciones else nx.spring_layout(self.grafo_nx, seed=42)
        nx.draw(self.grafo_nx, pos, with_labels=True, node_size=2000, node_color='lightblue', arrows=True)
        etiquetas = nx.get_edge_attributes(self.grafo_nx, 'weight')
        nx.draw_networkx_edge_labels(self.grafo_nx, pos, edge_labels=etiquetas)
        plt.title("Mapa Urbano")
        plt.show()

    def cargar_json(self, archivo):
        with open(archivo, "r") as f:
            datos = json.load(f)
            for nodo in datos["nodos"]:
                self.agregar_vertice(nodo["nombre"], nodo.get("posicion"))
            for arista in datos["calles"]:
                self.agregar_arista(arista["origen"], arista["destino"], arista["peso"], arista["doble_sentido"])

class SistemaGPS:
    def __init__(self, grafo):
        self.grafo = grafo

    def buscar_ruta(self, origen, destino):
        try:
            ruta = nx.shortest_path(self.grafo.grafo_nx, source=origen, target=destino, weight='weight')
            tiempo = sum(self.grafo.grafo_nx[ruta[i]][ruta[i+1]]["weight"] for i in range(len(ruta)-1))
            return ruta, tiempo
        except:
            return [], None

    def simular_trafico(self):
        for u, v in self.grafo.grafo_nx.edges:
            self.grafo.grafo_nx[u][v]["weight"] = random.randint(1, 10)
            if random.choice([True, False]):
                if not self.grafo.grafo_nx.has_edge(v, u):
                    self.grafo.agregar_arista(v, u, random.randint(1, 10))

class CentralAutobuses:
    def __init__(self, gps, registrar, actualizar):
        self.gps = gps
        self.registrar = registrar
        self.actualizar = actualizar
        self.clientes = []
        self.datos = {}
        self.archivo_csv = None

    def agregar_clientes(self, total, destinos):
        for _ in range(total):
            self.clientes.append(random.choice(destinos))

    def lanzar_camiones(self, destinos):
        for idx, destino in enumerate(destinos, 1):
            threading.Thread(target=self.simular_camion, args=(idx, destino)).start()

    def simular_camion(self, numero, destino):
        CAPACIDAD = 20
        vueltas = 0
        total_pasajeros = 0
        total_ida = 0
        total_regreso = 0

        while destino in self.clientes:
            self.actualizar(numero, "viaje", destino)
            self.gps.simular_trafico()
            ruta, ida = self.gps.buscar_ruta("Central", destino)
            if not ruta:
                self.registrar(f"[Camión-{numero}] Ruta no disponible hacia {destino}.")
                return
            pasajeros = min(CAPACIDAD, self.clientes.count(destino))
            for _ in range(pasajeros):
                self.clientes.remove(destino)
            self.registrar(f"[Camión-{numero}] {pasajeros} pasajeros hacia {destino}. Tiempo: {ida}min")
            time.sleep(ida * 0.1)
            self.actualizar(numero, "regresando", destino)
            _, regreso = self.gps.buscar_ruta(destino, "Central")
            time.sleep(regreso * 0.1)

            total_pasajeros += pasajeros
            total_ida += ida
            total_regreso += regreso
            vueltas += 1

        self.actualizar(numero, "disponible", "-")
        tiempo_total = total_ida + total_regreso
        self.registrar(f"[Camión-{numero}] Finalizó. Total pasajeros: {total_pasajeros} | Vueltas: {vueltas}")
        self.datos[(numero, destino)] = [numero, destino, total_pasajeros, total_ida, total_regreso, vueltas, tiempo_total]

        if not self.clientes:
            self.registrar("Todos los clientes han sido atendidos.")

    def exportar_csv(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".csv")
        if archivo:
            with open(archivo, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Camión", "Destino", "Pasajeros", "Tiempo Ida", "Tiempo Regreso", "Vueltas", "Tiempo Total"])
                for fila in self.datos.values():
                    w.writerow(fila)
            messagebox.showinfo("Éxito", "Datos exportados correctamente.")

    def importar_csv(self):
        archivo = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if archivo:
            self.archivo_csv = archivo
            with open(archivo, "r") as f:
                lector = csv.reader(f)
                next(lector)
                for fila in lector:
                    self.registrar(" | ".join(fila))
            return True
        return False

    def insertar_datos_en_csv(self):
        if not self.archivo_csv:
            messagebox.showwarning("Sin archivo", "Primero importa un archivo CSV.")
            return
        with open(self.archivo_csv, "a", newline="") as f:
            w = csv.writer(f)
            for fila in self.datos.values():
                w.writerow(fila)
        messagebox.showinfo("Datos agregados", "Nuevos datos insertados correctamente.")

class InterfazGPS:
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("POLINAV - Simulador de Camiones")
        self.grafo = GrafoFlexible()
        self.sistema = SistemaGPS(self.grafo)
        self.central = CentralAutobuses(self.sistema, self.registrar, self.actualizar)

        self.marco = tk.Frame(root)
        self.marco.pack(padx=10, pady=10)

        self.crear_menu()
        self.crear_controles()
        self.crear_estado()
        self.crear_eventos()

    def crear_menu(self):
        barra = tk.Menu(self.ventana)

        menu_archivo = tk.Menu(barra, tearoff=0)
        menu_archivo.add_command(label="Importar CSV", command=self.importar_csv)
        menu_archivo.add_command(label="Exportar CSV", command=self.central.exportar_csv)
        menu_archivo.add_command(label="Insertar datos", command=self.central.insertar_datos_en_csv, state="disabled")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Menú", menu=menu_archivo)
        self.menu_insertar = menu_archivo

        menu_mapa = tk.Menu(barra, tearoff=0)
        menu_mapa.add_command(label="Cargar mapa", command=self.importar_mapa)
        menu_mapa.add_command(label="Ver mapa", command=self.grafo.mostrar)
        menu_mapa.add_command(label="Simular tráfico", command=self.sistema.simular_trafico)
        barra.add_cascade(label="Mapa", menu=menu_mapa)

        barra.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Autores", "Monroy Pastrana Leonardo" "\nRodríguez Mercado Axel David" "\n Cayetano de la Cruz Axel Gustavo"))
        self.ventana.config(menu=barra)

    def crear_controles(self):
        tk.Label(self.marco, text="Clientes:").grid(row=0, column=0)
        self.entrada_clientes = tk.Entry(self.marco, width=5)
        self.entrada_clientes.grid(row=0, column=1)

        tk.Label(self.marco, text="Camiones:").grid(row=0, column=2)
        self.combo_camiones = ttk.Combobox(self.marco, values=[1,2,3,4,5], width=5)
        self.combo_camiones.grid(row=0, column=3)

        self.btn_generar = tk.Button(self.marco, text="Insertar camiones", command=self.insertar_camiones)
        self.btn_generar.grid(row=0, column=4, padx=5)

        self.opciones_destinos = []

    def insertar_camiones(self):
        for widget in self.opciones_destinos:
            widget.destroy()
        self.opciones_destinos.clear()

        num = int(self.combo_camiones.get())
        nodos = [n for n in self.grafo.grafo_nx.nodes if n != "Central"]
        self.camion_destinos = []

        for i in range(num):
            tk.Label(self.marco, text=f"Destino Camión {i+1}:").grid(row=i+1, column=0)
            var = tk.StringVar()
            combo = ttk.Combobox(self.marco, textvariable=var, values=nodos, width=10)
            combo.grid(row=i+1, column=1)
            self.opciones_destinos.append(combo)
            self.camion_destinos.append(var)

        tk.Button(self.marco, text="Iniciar", command=self.iniciar).grid(row=num+1, column=0)

    def crear_estado(self):
        self.estado = tk.LabelFrame(self.ventana, text="Estado")
        self.estado.pack(pady=10)
        self.labels_estado = {}
        for i in range(1, 6):
            lbl = tk.Label(self.estado, text=f"Camión {i}: Libre - Nodo: -", bg="lightgreen", width=25)
            lbl.pack(side="left", padx=5)
            self.labels_estado[i] = lbl

    def crear_eventos(self):
        self.area = tk.Text(self.ventana, height=10, width=90)
        self.area.pack()

    def registrar(self, texto):
        self.area.insert(tk.END, texto + "\n")
        self.area.yview_moveto(1)

    def actualizar(self, num, estado, nodo):
        colores = {"viaje":"red", "regresando":"orange", "disponible":"lightgreen"}
        texto = {"viaje":"En viaje", "regresando":"Regresando", "disponible":"Disponible"}
        self.labels_estado[num].config(text=f"Camión {num}: {texto[estado]} - Nodo: {nodo}", bg=colores[estado])

    def importar_mapa(self):
        archivo = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if archivo:
            self.grafo.cargar_json(archivo)
            messagebox.showinfo("Importado", "Mapa cargado exitosamente.")

    def importar_csv(self):
        if self.central.importar_csv():
            self.menu_insertar.entryconfig("Insertar datos", state="normal")

    def iniciar(self):
        total = int(self.entrada_clientes.get())
        destinos = [v.get() for v in self.camion_destinos]
        if len(set(destinos)) != len(destinos):
            messagebox.showerror("Error", "Destinos deben ser únicos.")
            return
        self.central.clientes.clear()
        self.central.agregar_clientes(total, destinos)
        self.central.lanzar_camiones(destinos)

# ==============================================================================
#                              BLOQUE PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazGPS(ventana)
    ventana.mainloop()
