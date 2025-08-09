import networkx as nx
import matplotlib.pyplot as plt
import os
import pydot

class Arco:
    """Representa una relación entre dos nodos."""
    def __init__(self, origen, destino, etiqueta):
        self.origen = origen
        self.destino = destino
        self.etiqueta = etiqueta

    def __str__(self):
        return f"{self.origen.etiqueta} -- {self.etiqueta} --> {self.destino.etiqueta}"

class Nodo:
    """Representa un concepto en la red."""
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.arcos = []

    def agregar_arco(self, destino, etiqueta_arco):
        self.arcos.append(Arco(self, destino, etiqueta_arco))

class RedSemantica:
    """Gestiona la red semántica."""
    def __init__(self):
        self.nodos = {}

    def crear_nodo(self, etiqueta):
        if etiqueta not in self.nodos:
            self.nodos[etiqueta] = Nodo(etiqueta)
        return self.nodos[etiqueta]

    def mostrar_red_por_concepto(self, concepto_clave):
        if concepto_clave not in self.nodos:
            print(f"El concepto '{concepto_clave}' no se encuentra en la red.")
            return False
        
        print(f"--- Relaciones para '{concepto_clave}' ---")
        nodo_inicial = self.nodos[concepto_clave]
        self._recorrer_y_mostrar(nodo_inicial, "")
        return True

    def _recorrer_y_mostrar(self, nodo_actual, prefijo):
        for i, arco in enumerate(nodo_actual.arcos):
            es_ultimo = i == len(nodo_actual.arcos) - 1
            nuevo_prefijo = prefijo + ("└── " if es_ultimo else "├── ")
            
            print(f"{nuevo_prefijo} {arco.etiqueta} -> {arco.destino.etiqueta}")
            
            sub_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            self._recorrer_y_mostrar(arco.destino, sub_prefijo)

    def generar_grafico(self, concepto_clave, nombre_archivo="red_semantica.png"):
        """Genera y guarda una representación gráfica de la sub-red del concepto clave."""
        G = nx.DiGraph()
        
        if concepto_clave not in self.nodos:
            print("El concepto no existe en la red.")
            return

        # Se obtienen los nodos a partir del concepto clave para dibujar solo el subgrafo
        sub_nodos = self._obtener_sub_nodos(self.nodos[concepto_clave])
        for nodo in sub_nodos:
            for arco in nodo.arcos:
                if arco.destino.etiqueta in [n.etiqueta for n in sub_nodos]:
                    G.add_edge(arco.origen.etiqueta, arco.destino.etiqueta, label=arco.etiqueta)
        
        if not G.nodes():
            G.add_node(concepto_clave)
        
        try:
            # Se usa pydot para un diseño de árbol jerárquico
            pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
        except ImportError:
            print("pydot no está instalado. Utilizando el diseño de resorte por defecto.")
            pos = nx.spring_layout(G, seed=42)
            
        plt.figure(figsize=(20, 15))
        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue', edgecolors='black', linewidths=1)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1.5, arrowsize=20, edge_color='gray', arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        
        plt.title(f"Red Semántica de '{concepto_clave}'", fontsize=15)
        plt.axis('off')
        
        plt.savefig(nombre_archivo, format="png", bbox_inches='tight')
        plt.close()
        print(f"Gráfico de la sub-red guardado como '{nombre_archivo}'")

    def _obtener_sub_nodos(self, nodo_inicial, visitados=None):
        if visitados is None:
            visitados = set()
        sub_nodos = [nodo_inicial]
        visitados.add(nodo_inicial.etiqueta)
        for arco in nodo_inicial.arcos:
            if arco.destino.etiqueta not in visitados:
                sub_nodos.extend(self._obtener_sub_nodos(arco.destino, visitados))
        return sub_nodos

if __name__ == "__main__":
    red = RedSemantica()
    ia = red.crear_nodo("Inteligencia Artificial")
    aa = red.crear_nodo("Aprendizaje Automático (Machine Learning)")
    ap = red.crear_nodo("Aprendizaje Profundo (Deep Learning)")
    algoritmos = red.crear_nodo("Algoritmos")
    an_supervisado = red.crear_nodo("Aprendizaje Supervisado")
    an_no_supervisado = red.crear_nodo("Aprendizaje No Supervisado")
    an_refuerzo = red.crear_nodo("Aprendizaje por Refuerzo")
    clasificacion = red.crear_nodo("Clasificación")
    regresion = red.crear_nodo("Regresión")
    clustering = red.crear_nodo("Clustering")
    rn_artificiales = red.crear_nodo("Redes Neuronales Artificiales")
    cnn = red.crear_nodo("CNN (Redes Convolucionales)")
    rnn = red.crear_nodo("RNN (Redes Recurrentes)")
    gan = red.crear_nodo("GAN (Redes Generativas Adversarias)")
    ia.agregar_arco(aa, "incluye")
    ia.agregar_arco(ap, "incluye")
    aa.agregar_arco(an_supervisado, "se divide en")
    aa.agregar_arco(an_no_supervisado, "se divide en")
    aa.agregar_arco(an_refuerzo, "se divide en")
    aa.agregar_arco(algoritmos, "se basa en")
    an_supervisado.agregar_arco(clasificacion, "utiliza")
    an_supervisado.agregar_arco(regresion, "utiliza")
    an_no_supervisado.agregar_arco(clustering, "utiliza")
    ap.agregar_arco(rn_artificiales, "se basa en")
    ap.agregar_arco(cnn, "utiliza")
    ap.agregar_arco(rnn, "utiliza")
    ap.agregar_arco(gan, "utiliza")
    print("Red Semántica de Inteligencia Artificial")
    print("Conceptos disponibles: Inteligencia Artificial, Aprendizaje Automático (Machine Learning), Aprendizaje Profundo (Deep Learning), etc.")
    while True:
        concepto_a_buscar = input("\nIngrese un concepto para ver sus relaciones (o 'salir' para terminar): ")
        if concepto_a_buscar.lower() == 'salir':
            break
        resultado_valido = red.mostrar_red_por_concepto(concepto_a_buscar)
        if resultado_valido:
            opcion = input("\n¿Desea generar una imagen del gráfico para este concepto? (s/n): ")
            if opcion.lower() == 's':
                nombre_archivo = f"red_semantica_{concepto_a_buscar.replace(' ', '_').replace('(', '').replace(')', '')}.png"
                red.generar_grafico(concepto_a_buscar, nombre_archivo)
                print(f"Imagen guardada en: {os.path.abspath(nombre_archivo)}")

