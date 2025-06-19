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

    def eliminar(self, dato):
        actual = self.inicio
        previo = None
        while actual and actual.dato != dato:
            previo = actual
            actual = actual.siguiente
        if actual:
            if previo:
                previo.siguiente = actual.siguiente
            else:
                self.inicio = actual.siguiente
            del actual
            return True
        return False

    def buscar(self, dato):
        actual = self.inicio
        while actual:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def mostrar(self):
        actual = self.inicio
        conexiones = []
        while actual:
            conexiones.append(actual.dato)
            actual = actual.siguiente
        return conexiones

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

    def buscarRuta(self):
        print("\nPUNTOS DISPONIBLES:")
        for nodo in sorted(self.calle.G.nodes):
            print("-", nodo)
        print()
        origen = input("Ingrese el punto de origen: ").strip().title()
        destino = input("Ingrese el destino: ").strip().title()

        if origen not in self.calle.G.nodes or destino not in self.calle.G.nodes:
            print("Puntos del mapa no encontrados.")
            return

        try:
            ruta = nx.shortest_path(self.calle.G, source=origen, target=destino, weight='weight')
            print(f"\nRuta más corta: {' ➝ '.join(ruta)}")
            self.calle.mostrar(ruta_resaltada=ruta)
        except nx.NetworkXNoPath:
            print("No hay ruta entre esos puntos.")

    def simularTrafico(self):
        for u, v in self.calle.G.edges:
            nuevo_peso = random.randint(1, 10)
            self.calle.G[u][v]['weight'] = nuevo_peso
        print("Simulación de tráfico actualizada.")
        self.calle.mostrar()

class Menu:
    def __init__(self):
        self.grafo = GrafoDirigido()
        self.sistema = SistemaGPS(self.grafo)
        self.sistema.mapa()

    def ejecutar(self):
        while True:
            print("\n---SISTEMA GPS ---")
            print("1. Ver mapa de tráfico")
            print("2. Buscar ruta más corta")
            print("3. Ver puntos del mapa")
            print("4. Simular tráfico")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.grafo.mostrar()
            elif opcion == "2":
                self.sistema.buscarRuta()
            elif opcion == "3":
                print("\nPUNTOS DISPONIBLES:")
                for nodo in sorted(self.grafo.G.nodes):
                    print("-", nodo)
            elif opcion == "4":
                self.sistema.simularTrafico()
            elif opcion == "5":
                print("Programa finalizado.")
                break
            else:
                print("Opción no válida")
# ==============================================================================
#                               BLOQUE PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    menu = Menu()
    menu.ejecutar()
