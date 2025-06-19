#====================================================================================
#                                   ENCABEZADO
#====================================================================================
# Autores: Monroy Pastrana Leonardo, Rodriguez Mercado Axel David, Cayetano de la Cruz Axel Gustavo
# Acividad: 
# Descripción del programa: 
#====================================================================================
#                                    LIBRERIAS
#====================================================================================
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import graphviz
from graphviz import Digraph
from PIL import Image
import os
import threading
from threading import Lock, Semaphore
import time
import random
from queue import Queue
#====================================================================================
#                                  CLASES Y FUNCIONES
#====================================================================================
class ContenedorInterfaz:
    def __init__(self, padre):
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Contenedores")
        self.ventana.geometry("400x350")
        self.etiqueta = tk.Label(self.ventana, text="", wraplength=380, font=("Arial", 10))
        self.etiqueta.pack(pady=10)
        tk.Button(self.ventana, text="Lista", command=self.mostrar_lista).pack(pady=5)
        tk.Button(self.ventana, text="Tupla", command=self.mostrar_tupla).pack(pady=5)
        tk.Button(self.ventana, text="Conjunto", command=self.mostrar_conjunto).pack(pady=5)
        tk.Button(self.ventana, text="Diccionario", command=self.mostrar_diccionario).pack(pady=5)
        tk.Button(self.ventana, text="Info", command=self.info).pack(pady=10)

    def mostrar_lista(self):
        ejemplo = [1, 2, 3, "hola"]
        mensaje = f"Lista de ejemplo: {ejemplo}\n\nUna lista es una colección ordenada y modificable. Permite elementos duplicados."
        self.etiqueta.config(text=mensaje)
        self.abrir_interactivo_lista()

    def mostrar_tupla(self):
        ejemplo = (1, 2, 3, "hola")
        mensaje = f"Tupla de ejemplo: {ejemplo}\n\nUna tupla es una colección ordenada e inmutable. Permite elementos duplicados."
        self.etiqueta.config(text=mensaje)
        self.abrir_interactivo_tupla()

    def mostrar_conjunto(self):
        ejemplo = {1, 2, 3, "hola"}
        mensaje = f"Conjunto de ejemplo: {ejemplo}\n\nUn conjunto es una colección no ordenada, sin elementos duplicados."
        self.etiqueta.config(text=mensaje)
        self.abrir_interactivo_conjunto()

    def mostrar_diccionario(self):
        ejemplo = {"nombre": "Leonardo", "edad": 20}
        mensaje = f"Diccionario de ejemplo: {ejemplo}\n\nUn diccionario almacena pares clave:valor. Es ordenado desde Python 3.7."
        self.etiqueta.config(text=mensaje)
        self.abrir_interactivo_diccionario()

    def info(self):
        messagebox.showinfo("Contenedores", "Los contenedores permiten almacenar colecciones de datos: listas, tuplas, conjuntos y diccionarios.")

    def abrir_interactivo_lista(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Ejercicio Interactivo - Lista")
        lista = []
        entrada = tk.Entry(ventana)
        entrada.pack()

        def agregar():
            lista.append(entrada.get())
            entrada.delete(0, tk.END)
            actualizar()

        def eliminar():
            try:
                lista.remove(entrada.get())
                entrada.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Elemento no encontrado")
            actualizar()

        def actualizar():
            texto.config(text=str(lista))

        tk.Button(ventana, text="Agregar", command=agregar).pack()
        tk.Button(ventana, text="Eliminar", command=eliminar).pack()
        texto = tk.Label(ventana, text="")
        texto.pack()

    def abrir_interactivo_tupla(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Ejercicio Interactivo - Tupla")
        elementos = []
        entrada = tk.Entry(ventana)
        entrada.pack()

        def agregar():
            elementos.append(entrada.get())
            entrada.delete(0, tk.END)
            texto.config(text=f"Tupla actual: {tuple(elementos)}")

        tk.Button(ventana, text="Agregar", command=agregar).pack()
        texto = tk.Label(ventana, text="Tupla actual: ()")
        texto.pack()

    def abrir_interactivo_conjunto(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Ejercicio Interactivo - Conjunto")
        conjunto = set()
        entrada = tk.Entry(ventana)
        entrada.pack()

        def agregar():
            conjunto.add(entrada.get())
            entrada.delete(0, tk.END)
            actualizar()

        def eliminar():
            conjunto.discard(entrada.get())
            entrada.delete(0, tk.END)
            actualizar()

        def actualizar():
            texto.config(text=f"Conjunto actual: {conjunto}")

        tk.Button(ventana, text="Agregar", command=agregar).pack()
        tk.Button(ventana, text="Eliminar", command=eliminar).pack()
        texto = tk.Label(ventana, text="Conjunto actual: set()")
        texto.pack()

    def abrir_interactivo_diccionario(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Ejercicio Interactivo - Diccionario")
        diccionario = {}

        clave = tk.Entry(ventana)
        valor = tk.Entry(ventana)
        clave.pack()
        valor.pack()

        def agregar():
            diccionario[clave.get()] = valor.get()
            clave.delete(0, tk.END)
            valor.delete(0, tk.END)
            actualizar()

        def eliminar():
            try:
                del diccionario[clave.get()]
                clave.delete(0, tk.END)
                actualizar()
            except KeyError:
                messagebox.showerror("Error", "Clave no encontrada")

        def actualizar():
            texto.config(text=f"Diccionario: {diccionario}")

        tk.Button(ventana, text="Agregar", command=agregar).pack()
        tk.Button(ventana, text="Eliminar", command=eliminar).pack()
        texto = tk.Label(ventana, text="Diccionario: {}")
        texto.pack()

class PilasColasInterfaz:
    def __init__(self, padre):
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Pilas y Colas")
        self.ventana.geometry("400x300")
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(expand=True, fill="both")
        self.pila = []
        self.cola = []
        self._crear_pestania("Pilas", self.pila, "LIFO: Último en entrar, primero en salir.")
        self._crear_pestania("Colas", self.cola, "FIFO: Primero en entrar, primero en salir.")

    def _crear_pestania(self, nombre, estructura, descripcion):
        marco = ttk.Frame(self.notebook)
        self.notebook.add(marco, text=nombre)
        entrada = tk.Entry(marco)
        entrada.pack(pady=5)

        def insertar():
            estructura.append(entrada.get())
            entrada.delete(0, tk.END)

        def extraer():
            if nombre == "Pilas":
                dato = estructura.pop() if estructura else None
            else:
                dato = estructura.pop(0) if estructura else None
            messagebox.showinfo("Extraído", f"{dato}" if dato else "Estructura vacía")

        def consultar():
            val = estructura[-1] if nombre == "Pilas" and estructura else (
                estructura[0] if estructura else None)
            messagebox.showinfo("Consultar", f"{val}" if val else "Estructura vacía")

        def estado():
            messagebox.showinfo("Estado", "Vacía" if not estructura else "Con elementos")

        def tamanio():
            messagebox.showinfo("Tamaño", str(len(estructura)))

        tk.Button(marco, text="Insertar", command=insertar).pack()
        tk.Button(marco, text="Extraer", command=extraer).pack()
        tk.Button(marco, text="Consultar", command=consultar).pack()
        tk.Button(marco, text="Estado", command=estado).pack()
        tk.Button(marco, text="Tamaño", command=tamanio).pack()
        tk.Button(marco, text="Info", command=lambda: messagebox.showinfo("Info", descripcion)).pack(pady=10)

class InfoListaDinamica:
    def __init__(self, padre):
        self.ventana_info = tk.Toplevel(padre)
        self.ventana_info.title("Listas Dinámicas")
        self.ventana_info.geometry("450x250")

        mensaje = ("\nA diferencia de las listas tradicionales (como las listas en Python), "
                   "\nlas listas dinámicas utilizan nodos enlazados para almacenar los elementos.\n"
                   "\nEsto permite que su tamaño crezca o disminuya fácilmente durante la ejecución.\n"
                   "\nNo requieren tamaño fijo al inicio.\n"
                   "Su estructura se adapta dinámicamente.\n"
                   "Son ideales para inserciones y eliminaciones frecuentes.")

        tk.Label(self.ventana_info, text=mensaje, justify="left", font=("Arial", 10)).pack(padx=10, pady=10)
        tk.Button(self.ventana_info, text="Ver Tipos de Lista Dinámica", command=self.abrir_tipado).pack(pady=10)

    def abrir_tipado(self):
        TiposListasDinamicas(self.ventana_info)

class TiposListasDinamicas:
    def __init__(self, padre):
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Tipos de Listas Dinámicas")
        self.ventana.geometry("500x350")

        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(expand=True, fill="both")

        tipos = {
            "Simplemente Enlazada": "Cada nodo apunta al siguiente nodo en la lista.\nIdeal para recorrido en una sola dirección.",
            "Doblemente Enlazada": "Cada nodo tiene un enlace al nodo siguiente y anterior.\nPermite recorrido en ambas direcciones.",
            "Circular": "El último nodo apunta al primero.\nEvita referencias nulas y permite ciclos continuos.",
            "Pilas Dinámicas": "Se basan en listas enlazadas.\nInserción y extracción solo en un extremo (LIFO).",
            "Colas Dinámicas": "Se basan en listas enlazadas.\nInserción al final y extracción al inicio (FIFO)."
        }

        for nombre, descripcion in tipos.items():
            self._crear_pestana(nombre, descripcion)

    def _crear_pestana(self, titulo, descripcion):
        marco = ttk.Frame(self.notebook)
        self.notebook.add(marco, text=titulo)
        texto = tk.Text(marco, wrap="word", font=("Arial", 11))
        texto.insert("1.0", descripcion)
        texto.config(state="disabled")
        texto.pack(expand=True, fill="both", padx=10, pady=10)
   
class RecursividadInterfaz:
    def __init__(self, padre):
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Recursividad")
        self.ventana.geometry("500x400")

        texto = (
            "La recursividad es una técnica de programación donde una función se llama a sí misma.\n\n"
            "Características:\n"
            "- Debe tener una condición de parada (caso base).\n"
            "- Se utiliza para resolver problemas que se pueden dividir en subproblemas similares.\n\n"
            "Aplicaciones comunes:\n"
            "- Cálculo de factoriales\n"
            "- Serie de Fibonacci\n"
            "- Recorridos en estructuras como árboles y grafos"
        )

        label_info = tk.Label(self.ventana, text=texto, justify="left", wraplength=480, font=("Arial", 11))
        label_info.pack(pady=10)

        tk.Button(self.ventana, text="Ver ejemplo de Factorial y Fibonacci", command=self.mostrar_ejemplos).pack(pady=10)

    def mostrar_ejemplos(self):
        ejemplo_ventana = tk.Toplevel(self.ventana)
        ejemplo_ventana.title("Ejemplos de Recursividad")
        ejemplo_ventana.geometry("500x400")

        texto = tk.Text(ejemplo_ventana, wrap="word", font=("Consolas", 11))
        texto.insert("1.0",
            "def factorial(n):\n"
            "    if n == 0 or n == 1:\n"
            "        return 1\n"
            "    else:\n"
            "        return n * factorial(n-1)\n\n"

            "def fibonacci(n):\n"
            "    if n <= 0:\n"
            "        return 0\n"
            "    elif n == 1:\n"
            "        return 1\n"
            "    else:\n"
            "        return fibonacci(n-1) + fibonacci(n-2)\n\n"

            "# Ejemplos:\n"
            "print('Factorial de 5:', factorial(5))\n"
            "print('Fibonacci de 6:', fibonacci(6))"
        )
        texto.config(state="disabled")
        texto.pack(expand=True, fill="both", padx=10, pady=10)

class Nodo:
    def __init__(self,dato):
        self.dato = dato 
        self.siguiente = None 

class ListaEnlazada:
    def __init__(self):
        self.inicio = None 
    
    def insertar(self, dato):
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.inicio
        self.inicio = nuevo_nodo

    def mostrar(self):
        actual = self.inicio
        elementos = []
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def buscar(self, dato):
        actual = self.inicio
        while actual:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

class GrafoVisual:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.adyacencia = {}

    def agregar_vertice(self, v):
        if v not in self.adyacencia:
            self.adyacencia[v] = ListaEnlazada()
            self.grafo.add_node(v)

    def agregar_arista(self, origen, destino, peso=1, bidireccional=False):
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        if not self.adyacencia[origen].buscar(destino):
            self.adyacencia[origen].insertar(destino)
            self.grafo.add_edge(origen, destino, weight=peso)
        if bidireccional and not self.adyacencia[destino].buscar(origen):
            self.adyacencia[destino].insertar(origen)
            self.grafo.add_edge(destino, origen, weight=peso)

    def mostrar_grafo(self):
        fig, ax = plt.subplots(figsize=(5, 4))
        pos = nx.spring_layout(self.grafo, seed=42)
        nx.draw(self.grafo, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, ax=ax)
        labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=labels, ax=ax)
        return fig

    def mostrar_lista_adyacencia(self):
        resultado = ""
        for vertice, lista in self.adyacencia.items():
            vecinos = ', '.join(lista.mostrar())
            resultado += f"{vertice}: {vecinos}\n"
        return resultado

    def obtener_matriz_adyacencia(self):
        nodos = list(self.grafo.nodes)
        matriz = [[0 for _ in nodos] for _ in nodos]
        for i, u in enumerate(nodos):
            for j, v in enumerate(nodos):
                if self.grafo.has_edge(u, v):
                    matriz[i][j] = self.grafo[u][v]['weight']
        return nodos, matriz

    def bfs(self, inicio):
        visitados = []
        cola = deque([inicio])
        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.append(nodo)
                for vecino in self.adyacencia[nodo].mostrar():
                    cola.append(vecino)
        return visitados

    def dfs(self, inicio):
        visitados = []
        pila = [inicio]
        while pila:
            nodo = pila.pop()
            if nodo not in visitados:
                visitados.append(nodo)
                for vecino in self.adyacencia[nodo].mostrar():
                    pila.append(vecino)
        return visitados

class InterfazGrafos:
    def __init__(self, padre):
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Tema: Grafos")
        self.ventana.geometry("800x600")
        self.grafo = GrafoVisual()
        self._crear_widgets()
        self._cargar_ejemplo()

    def _crear_widgets(self):
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(expand=True, fill='both')

        self.tabs = {}
        for nombre in ["Grafo Dirigido", "Grafo No Dirigido", "Lista de Adyacencia", "Matriz de Adyacencia", "Búsqueda en Grafos"]:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=nombre)
            self.tabs[nombre] = tab

        self._crear_interfaz_dirigido(self.tabs["Grafo Dirigido"])
        self._crear_interfaz_nodirigido(self.tabs["Grafo No Dirigido"])
        self._crear_lista_adyacencia(self.tabs["Lista de Adyacencia"])
        self._crear_matriz_adyacencia(self.tabs["Matriz de Adyacencia"])
        self._crear_busqueda(self.tabs["Búsqueda en Grafos"])

    def _cargar_ejemplo(self):
        self.grafo.agregar_arista("A", "B", 2)
        self.grafo.agregar_arista("B", "C", 3)
        self.grafo.agregar_arista("A", "D", 1, bidireccional=True)
        self.grafo.agregar_arista("D", "E", 4)

    def _crear_interfaz_dirigido(self, frame):
        self._crear_menu_grafo(frame, bidireccional=False)

    def _crear_interfaz_nodirigido(self, frame):
        self._crear_menu_grafo(frame, bidireccional=True)

    def _crear_menu_grafo(self, frame, bidireccional):
        tk.Label(frame, text="Origen:").pack()
        origen = tk.Entry(frame)
        origen.pack()

        tk.Label(frame, text="Destino:").pack()
        destino = tk.Entry(frame)
        destino.pack()

        tk.Label(frame, text="Peso:").pack()
        peso = tk.Entry(frame)
        peso.pack()

        def agregar():
            o = origen.get().strip()
            d = destino.get().strip()
            try:
                p = int(peso.get())
                self.grafo.agregar_arista(o, d, p, bidireccional)
                messagebox.showinfo("Éxito", "Arista agregada correctamente")
            except:
                messagebox.showerror("Error", "Peso inválido")

        def mostrar():
            fig = self.grafo.mostrar_grafo()
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

        tk.Button(frame, text="Agregar Arista", command=agregar).pack(pady=5)
        tk.Button(frame, text="Mostrar Grafo", command=mostrar).pack(pady=5)

    def _crear_lista_adyacencia(self, frame):
        def mostrar():
            resultado = self.grafo.mostrar_lista_adyacencia()
            text.delete("1.0", tk.END)
            text.insert(tk.END, resultado)

        text = tk.Text(frame, height=20)
        text.pack()
        tk.Button(frame, text="Mostrar Lista", command=mostrar).pack(pady=5)

    def _crear_matriz_adyacencia(self, frame):
        def mostrar():
            nodos, matriz = self.grafo.obtener_matriz_adyacencia()
            text.delete("1.0", tk.END)
            header = "\t".join(nodos)
            text.insert(tk.END, f"\t{header}\n")
            for i, fila in enumerate(matriz):
                fila_txt = "\t".join(map(str, fila))
                text.insert(tk.END, f"{nodos[i]}\t{fila_txt}\n")

        text = tk.Text(frame, height=20)
        text.pack()
        tk.Button(frame, text="Mostrar Matriz", command=mostrar).pack(pady=5)

    def _crear_busqueda(self, frame):
        tk.Label(frame, text="Nodo de inicio:").pack()
        entrada = tk.Entry(frame)
        entrada.pack()

        resultado = tk.Text(frame, height=10)
        resultado.pack()

        def ejecutar_bfs():
            inicio = entrada.get().strip()
            visitados = self.grafo.bfs(inicio)
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END, f"Recorrido BFS: {' -> '.join(visitados)}")

        def ejecutar_dfs():
            inicio = entrada.get().strip()
            visitados = self.grafo.dfs(inicio)
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END, f"Recorrido DFS: {' -> '.join(visitados)}")

        tk.Button(frame, text="BFS", command=ejecutar_bfs).pack(pady=3)
        tk.Button(frame, text="DFS", command=ejecutar_dfs).pack(pady=3)

class Nodo1:
    def __init__(self, codigo, nombre, domicilio):
        self.codigo = codigo
        self.nombre = nombre
        self.domicilio = domicilio
        self.izq = None
        self.der = None

    def __str__(self):
        return f"{self.codigo} - {self.nombre} - {self.domicilio}"

class ABB:
    def __init__(self):
        self.raiz = None

    def insertar(self, codigo, nombre, domicilio):
        if not self.raiz:
            self.raiz = Nodo1(codigo, nombre, domicilio)
        else:
            self._insertar_recursivo(self.raiz, codigo, nombre, domicilio)

    def _insertar_recursivo(self, nodo, codigo, nombre, domicilio):
        if codigo < nodo.codigo:
            if nodo.izq:
                self._insertar_recursivo(nodo.izq, codigo, nombre, domicilio)
            else:
                nodo.izq = Nodo1(codigo, nombre, domicilio)
        elif codigo > nodo.codigo:
            if nodo.der:
                self._insertar_recursivo(nodo.der, codigo, nombre, domicilio)
            else:
                nodo.der = Nodo1(codigo, nombre, domicilio)

    def recorrido_inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izq, resultado)
            resultado.append(str(nodo))
            self._inorden_recursivo(nodo.der, resultado)

    def recorrido_preorden(self):
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo, resultado):
        if nodo:
            resultado.append(str(nodo))
            self._preorden_recursivo(nodo.izq, resultado)
            self._preorden_recursivo(nodo.der, resultado)

    def recorrido_postorden(self):
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo, resultado):
        if nodo:
            self._postorden_recursivo(nodo.izq, resultado)
            self._postorden_recursivo(nodo.der, resultado)
            resultado.append(str(nodo))

    def generar_dot(self):
        dot = Digraph()
        dot.attr('node', shape='box')
        if self.raiz:
            self._agregar_dot(dot, self.raiz)
        return dot

    def _agregar_dot(self, dot, nodo):
        etiqueta = f"{nodo.codigo}\n{nodo.nombre}\n{nodo.domicilio}"
        dot.node(etiqueta)
        if nodo.izq:
            izq_etiqueta = f"{nodo.izq.codigo}\n{nodo.izq.nombre}\n{nodo.izq.domicilio}"
            dot.edge(etiqueta, izq_etiqueta)
            self._agregar_dot(dot, nodo.izq)
        if nodo.der:
            der_etiqueta = f"{nodo.der.codigo}\n{nodo.der.nombre}\n{nodo.der.domicilio}"
            dot.edge(etiqueta, der_etiqueta)
            self._agregar_dot(dot, nodo.der)

class ArbolBinarioUI:
    def __init__(self, padre):
        self.arbol = ABB()
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Árboles Binarios")
        self.ventana.geometry("500x500")

        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill='both', expand=True)

        self.crear_pestania_insertar()
        self.crear_pestania_recorridos()
        self.crear_pestania_visualizar()

    def crear_pestania_insertar(self):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Insertar")

        tk.Label(frame, text="Código").pack()
        self.codigo = tk.Entry(frame)
        self.codigo.pack()

        tk.Label(frame, text="Nombre").pack()
        self.nombre = tk.Entry(frame)
        self.nombre.pack()

        tk.Label(frame, text="Domicilio").pack()
        self.domicilio = tk.Entry(frame)
        self.domicilio.pack()

        tk.Button(frame, text="Insertar", command=self.insertar).pack(pady=5)
        tk.Button(frame, text="Cargar ejemplo", command=self.cargar_ejemplo).pack(pady=5)

    def insertar(self):
        c = self.codigo.get().strip()
        n = self.nombre.get().strip()
        d = self.domicilio.get().strip()
        if not c or not n or not d:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return
        self.arbol.insertar(c, n, d)
        messagebox.showinfo("Insertado", f"{n} insertado correctamente")
        self.codigo.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.domicilio.delete(0, tk.END)

    def cargar_ejemplo(self):
        datos = [
            ("LP", "Luis Pérez", "Reforma 100"),
            ("JG", "Juan Gómez", "Insurgentes 200"),
            ("AT", "Ana Torres", "Juárez 300"),
            ("KM", "Karla Morales", "Morelos 400")
        ]
        for c, n, d in datos:
            self.arbol.insertar(c, n, d)
        messagebox.showinfo("Ejemplo", "Ejemplo cargado correctamente")

    def crear_pestania_recorridos(self):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Recorridos")
        self.salida = tk.Text(frame, height=15, width=60)
        self.salida.pack()

        botones = tk.Frame(frame)
        botones.pack(pady=10)

        tk.Button(botones, text="Inorden", command=self.ver_inorden).pack(side=tk.LEFT, padx=5)
        tk.Button(botones, text="Preorden", command=self.ver_preorden).pack(side=tk.LEFT, padx=5)
        tk.Button(botones, text="Postorden", command=self.ver_postorden).pack(side=tk.LEFT, padx=5)

    def ver_inorden(self):
        self.salida.delete("1.0", tk.END)
        for linea in self.arbol.recorrido_inorden():
            self.salida.insert(tk.END, linea + "\n")

    def ver_preorden(self):
        self.salida.delete("1.0", tk.END)
        for linea in self.arbol.recorrido_preorden():
            self.salida.insert(tk.END, linea + "\n")

    def ver_postorden(self):
        self.salida.delete("1.0", tk.END)
        for linea in self.arbol.recorrido_postorden():
            self.salida.insert(tk.END, linea + "\n")

    def crear_pestania_visualizar(self):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Visualizar")
        tk.Button(frame, text="Mostrar Árbol", command=self.visualizar_arbol).pack(pady=20)

    def visualizar_arbol(self):
        dot = self.arbol.generar_dot()
        dot.render("arbol_binario", format="png", cleanup=True)
        imagen = Image.open("arbol_binario.png")
        imagen.show()

class DulceriaSimulador:
    def __init__(self, ventana):
        self.ventana = tk.Toplevel(ventana)
        self.ventana.title("Simulación de Concurrencia - Dulcería")
        self.ventana.geometry("600x400")

        self.cola_clientes = Queue()
        self.lock = threading.Lock()
        self.semaforo = threading.Semaphore(3)  # Máximo 3 cajas disponibles
        self.total_atendidos = 0

        self.texto = tk.Text(self.ventana, height=20, width=70)
        self.texto.pack(pady=10)

        boton_inicio = tk.Button(self.ventana, text="Iniciar Simulación", command=self.iniciar_simulacion)
        boton_inicio.pack(pady=5)

    def log(self, mensaje):
        self.texto.insert(tk.END, mensaje + "\n")
        self.texto.see(tk.END)

    def llegada_clientes(self, total):
        for i in range(1, total + 1):
            time.sleep(random.uniform(0.1, 0.3))
            cliente = f"Cliente-{i}"
            self.cola_clientes.put(cliente)
            with self.lock:
                self.log(f"Llegó {cliente} (en cola: {self.cola_clientes.qsize()})")

    def atender_en_caja(self, numero):
        while not self.cola_clientes.empty():
            try:
                cliente = self.cola_clientes.get(timeout=1)
            except:
                break

            if not self.semaforo.acquire(timeout=1):
                with self.lock:
                    self.log(f"[Caja-{numero}] no pudo atender a {cliente} (timeout)")
                continue

            try:
                with self.lock:
                    self.log(f"[Caja-{numero}] Atendiendo a {cliente}")
                time.sleep(random.uniform(0.3, 0.6))
                with self.lock:
                    self.total_atendidos += 1
                    self.log(f"[Caja-{numero}] Terminó con {cliente} | Total atendidos: {self.total_atendidos}")
            finally:
                self.semaforo.release()
                self.cola_clientes.task_done()

    def iniciar_simulacion(self):
        self.texto.delete("1.0", tk.END)
        total_clientes = 10
        self.total_atendidos = 0
        self.cola_clientes = Queue()

        productor = threading.Thread(target=self.llegada_clientes, args=(total_clientes,))
        productor.start()

        cajas = [threading.Thread(target=self.atender_en_caja, args=(i + 1,)) for i in range(3)]

        for caja in cajas:
            caja.start()

        productor.join()
        self.cola_clientes.join()
        for caja in cajas:
            caja.join()

        self.log("\nTodos los clientes fueron atendidos.")

class ConcurrenciaInterfaz:
    def __init__(self, ventana):
        self.ventana = tk.Toplevel(ventana)
        self.ventana.title("Concurrencia")
        self.ventana.geometry("500x300")

        notebook = ttk.Notebook(self.ventana)
        notebook.pack(fill='both', expand=True)

        frame_info = ttk.Frame(notebook)
        frame_simulador = ttk.Frame(notebook)
        notebook.add(frame_info, text="¿Qué es la concurrencia?")
        notebook.add(frame_simulador, text="Simulación Dulcería")

        texto_info = tk.Text(frame_info, wrap=tk.WORD)
        texto_info.insert(tk.END, 
            "La concurrencia permite ejecutar múltiples tareas al mismo tiempo.\n\n"
            "Race Condition: Error cuando dos procesos acceden al mismo recurso sin control.\n"
            "Deadlock (Interbloqueo): Dos o más procesos quedan esperando recursos entre sí.\n"
            "Starvation (Inanición): Un proceso nunca es atendido porque otros acaparan los recursos.")
        texto_info.config(state='disabled')
        texto_info.pack(padx=10, pady=10, fill='both', expand=True)

        simulador = DulceriaSimulador(frame_simulador)

class MenuPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Proyecto Final - Programación")
        self.ventana.geometry("800x600")
        self.crear_menu()

    def crear_menu(self):
        barra_menu = tk.Menu(self.ventana)

        estructura = {
            "Menú": {
                "Unidad 1": {
                    "Contenedores": self.abrir_contenedores,
                    "Pilas y Colas": self.abrir_pilas_colas
                },
                "Unidad 2": {
                    "Listas Dinamicas": self.arbir_listasDinamicas,
                    "Recursividad": self.abrir_recursividad,
                    "Grafos": self.abrir_grafos
                },
                "Unidad 3": {
                    "Arboles binarios": self.abrir_ABB,
                    "Concurrencia": self.abrir_concurrencia
                },

                "Salir": self.salir
            },
            "Acerca de": {
                "Autor": lambda: messagebox.showinfo("Acerca de", "Monroy Pastrana Leonardo")
            }
        }

        def crear_submenu(padre, estructura):
            for etiqueta, accion in estructura.items():
                if callable(accion):
                    padre.add_command(label=etiqueta, command=accion)
                elif isinstance(accion, dict):
                    sub = tk.Menu(padre, tearoff=0)
                    crear_submenu(sub, accion)
                    padre.add_cascade(label=etiqueta, menu=sub)

        crear_submenu(barra_menu, estructura)
        self.ventana.config(menu=barra_menu)

    def abrir_contenedores(self):
        ContenedorInterfaz(self.ventana)

    def abrir_pilas_colas(self):
        PilasColasInterfaz(self.ventana)

    def arbir_listasDinamicas(self):
        InfoListaDinamica(self.ventana)

    def abrir_recursividad(self):
        RecursividadInterfaz(self.ventana)

    def abrir_grafos(self):
        InterfazGrafos(self.ventana)

    def abrir_ABB(self):
        ArbolBinarioUI(self.ventana)
    
    def abrir_concurrencia(self):
        ConcurrenciaInterfaz(self.ventana)

    def salir(self):
        self.ventana.quit()

    def ejecutar(self):
        self.ventana.mainloop()

# ==================================== BLOQUE PRINCIPAL =====================================
if __name__ == "__main__":
    aplicacion = MenuPrincipal()
    aplicacion.ejecutar()
