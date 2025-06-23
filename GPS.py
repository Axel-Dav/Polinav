import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
import threading
import time
import random
import json
import csv
import queue

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
        if bidireccional:
            if not self.adyacencia[v2].buscar(v1):
                self.adyacencia[v2].insertar(v1)
                self.grafo_nx.add_edge(v2, v1, weight=peso)

    def cargar_desde_json(self, ruta):
        with open(ruta, 'r') as f:
            datos = json.load(f)
        for nodo in datos["nodos"]:
            self.agregar_vertice(nodo["nombre"], nodo.get("posicion"))
        for calle in datos["calles"]:
            self.agregar_arista(calle["origen"], calle["destino"], calle["peso"], calle["doble_sentido"])

    def mostrar_mapa(self, ruta=None):
        def visualizar():
            plt.figure()
            pos = self.posiciones or nx.spring_layout(self.grafo_nx, seed=42)
            nx.draw(self.grafo_nx, pos, with_labels=True, node_color='skyblue', node_size=1500, arrows=True)
            etiquetas = nx.get_edge_attributes(self.grafo_nx, 'weight')
            nx.draw_networkx_edge_labels(self.grafo_nx, pos, edge_labels=etiquetas)
            if ruta:
                edges = list(zip(ruta, ruta[1:]))
                nx.draw_networkx_edges(self.grafo_nx, pos, edgelist=edges, edge_color='red', width=3)
                nx.draw_networkx_nodes(self.grafo_nx, pos, nodelist=ruta, node_color='orange')
            plt.title("Mapa de Rutas")
            plt.show()
        self._ejecutar_en_principal(visualizar)

    def _ejecutar_en_principal(self, funcion):
        self.funcion = funcion
        self.graficador = threading.Thread(target=self._esperar)
        self.graficador.start()

    def _esperar(self):
        time.sleep(0.1)
        self.funcion()

class SistemaGPS:
    def __init__(self, grafo):
        self.grafo = grafo

    def buscar_ruta(self, origen, destino):
        try:
            ruta = nx.shortest_path(self.grafo.grafo_nx, source=origen, target=destino, weight='weight')
            tiempo = sum(self.grafo.grafo_nx[ruta[i]][ruta[i+1]]['weight'] for i in range(len(ruta)-1))
            return ruta, tiempo
        except:
            return [], 0

    def simular_trafico(self):
        for u, v in self.grafo.grafo_nx.edges():
            self.grafo.grafo_nx[u][v]['weight'] = random.randint(1, 10)
            if random.random() < 0.3:
                if not self.grafo.grafo_nx.has_edge(v, u):
                    self.grafo.agregar_arista(v, u, peso=random.randint(1, 10), bidireccional=False)

class SimuladorRutas:
    def __init__(self, gps, registrar, actualizar, destinos):
        self.gps = gps
        self.registrar = registrar
        self.actualizar = actualizar
        self.destinos = destinos
        self.cola_clientes = queue.Queue()
        self.historial = []

    def iniciar_simulacion(self, clientes, destinos_camiones):
        for _ in range(clientes):
            destino = random.choice(self.destinos)
            self.cola_clientes.put(destino)

        for idx, destino in enumerate(destinos_camiones):
            hilo = threading.Thread(target=self.simular_camion, args=(idx+1, destino))
            hilo.start()

    def simular_camion(self, numero, destino):
        capacidad = 20
        vueltas = 0
        while not self.cola_clientes.empty():
            self.actualizar(numero, "viaje")
            pasajeros = []
            while not self.cola_clientes.empty() and len(pasajeros) < capacidad:
                pasajeros.append(self.cola_clientes.get())

            self.gps.simular_trafico()
            ruta, ida = self.gps.buscar_ruta("Central", destino)
            self.gps.grafo.mostrar_mapa(ruta)

            self.registrar(f"[Camión {numero}] Salió a {destino} con {len(pasajeros)} pasajeros.")
            time.sleep(ida * 0.1)

            ruta_vuelta, regreso = self.gps.buscar_ruta(destino, "Central")
            time.sleep(regreso * 0.1)

            self.registrar(f"[Camión {numero}] Regresó. Tiempo total: {ida + regreso} min.")
            self.actualizar(numero, "disponible")
            vueltas += 1

        self.historial.append([numero, destino, len(pasajeros), ida, regreso, vueltas])

class InterfazGPS:
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Simulador GPS con Camiones")
        self.ventana.geometry("750x600")

        self.grafo = GrafoFlexible()
        self.gps = SistemaGPS(self.grafo)
        self.simulador = None

        self.crear_interfaz()

    def crear_interfaz(self):
        barra = tk.Menu(self.ventana)
        archivo = tk.Menu(barra, tearoff=0)
        archivo.add_command(label="Importar mapa", command=self.importar_mapa)
        archivo.add_command(label="Exportar CSV", command=self.exportar_csv)
        archivo.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Menú", menu=archivo)
        barra.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Autor", "Monroy Pastrana Leonardo"))
        self.ventana.config(menu=barra)

        frame = tk.Frame(self.ventana)
        frame.pack(pady=10)

        tk.Label(frame, text="Clientes:").grid(row=0, column=0)
        self.entrada_clientes = tk.Entry(frame, width=5)
        self.entrada_clientes.grid(row=0, column=1)

        tk.Label(frame, text="Camiones (1-5):").grid(row=1, column=0)
        self.combo_camiones = ttk.Combobox(frame, values=[1, 2, 3, 4, 5], width=3)
        self.combo_camiones.grid(row=1, column=1)

        self.boton_insertar = tk.Button(frame, text="Insertar Camiones", command=self.insertar_camiones)
        self.boton_insertar.grid(row=1, column=2)

        self.marco_destinos = tk.LabelFrame(self.ventana, text="Destinos por camión")
        self.marco_destinos.pack(padx=10, pady=5)

        self.boton_simular = tk.Button(self.ventana, text="Iniciar Simulación", command=self.simular)
        self.boton_simular.pack(pady=5)

        self.area_eventos = tk.Text(self.ventana, height=20, width=90)
        self.area_eventos.pack(padx=10, pady=10)

        self.labels_estado = {}
        frame_estado = tk.Frame(self.ventana)
        frame_estado.pack(pady=5)
        for i in range(1, 6):
            lbl = tk.Label(frame_estado, text=f"Camión {i}: Disponible", bg="lightgreen", width=20)
            lbl.pack(side="left", padx=5)
            self.labels_estado[i] = lbl

    def insertar_camiones(self):
        for widget in self.marco_destinos.winfo_children():
            widget.destroy()
        try:
            cantidad = int(self.combo_camiones.get())
        except:
            messagebox.showerror("Error", "Selecciona número de camiones")
            return

        nodos = [n for n in self.grafo.grafo_nx.nodes if n != "Central"]
        self.combos_destino = []
        for i in range(cantidad):
            tk.Label(self.marco_destinos, text=f"Destino Camión {i+1}:").grid(row=i, column=0)
            cb = ttk.Combobox(self.marco_destinos, values=nodos)
            cb.grid(row=i, column=1)
            self.combos_destino.append(cb)

    def importar_mapa(self):
        archivo = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if archivo:
            self.grafo.cargar_desde_json(archivo)
            messagebox.showinfo("Cargado", "Mapa importado exitosamente.")

    def exportar_csv(self):
        if not self.simulador or not self.simulador.historial:
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        with open(archivo, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Camión", "Destino", "Pasajeros", "Tiempo Ida", "Tiempo Regreso", "Vueltas"])
            writer.writerows(self.simulador.historial)
        messagebox.showinfo("Exportado", "Datos guardados correctamente.")

    def registrar_evento(self, texto):
        self.area_eventos.insert(tk.END, texto + "\n")
        self.area_eventos.see(tk.END)

    def actualizar_estado(self, camion, estado):
        colores = {"viaje": "red", "disponible": "lightgreen"}
        textos = {"viaje": "En viaje", "disponible": "Disponible"}
        self.labels_estado[camion].config(bg=colores[estado], text=f"Camión {camion}: {textos[estado]}")

    def simular(self):
        try:
            clientes = int(self.entrada_clientes.get())
        except:
            messagebox.showerror("Error", "Clientes inválidos")
            return

        destinos = []
        for cb in self.combos_destino:
            destino = cb.get()
            if not destino:
                messagebox.showerror("Error", "Selecciona todos los destinos.")
                return
            destinos.append(destino)

        self.simulador = SimuladorRutas(self.gps, self.registrar_evento, self.actualizar_estado, destinos)
        self.simulador.iniciar_simulacion(clientes, destinos)

# ------------------------------ EJECUCIÓN PRINCIPAL ------------------------------
if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazGPS(ventana)
    ventana.mainloop()
