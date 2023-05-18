import networkx as nx

# Criar grafo
G = nx.Graph()

# Adicionar noh ao grafo G
G.add_node(1)

# Adicionar mais que um noh por um container, exemplo, lista
G.add_nodes_from([2, 3])

# Adicionar nohs com atributos, e mais que um
G.add_nodes_from([
    (4, {"color": "red"}),
    (5, {"color": "green"}),
])

# Cria um grafo H, usando essa outra funcao que ainda nao sei o que faz, e adiciona os nós dele como nós do G
H = nx.path_graph(10)
G.add_nodes_from(H)

# Adiciona o grafo H em sih como um noh em G
G.add_node(H)

# Adicionar arestas (uma por vez e com desempacotamento de tupla)
G.add_edge(1, 2)
e = (2, 3)
G.add_edge(*e)  # unpack edge tuple*

# Com um container como uma lista de tuplas
G.add_edges_from([(1, 2), (1, 3)])

# Arestas podem ter atributos EX: (2, 3, {'weight': 3.1415})

# Como os nohs, eh possivel usar arestas de outro grafo
# Adiciona arestas do grafo H para o grafo G
G.add_edges_from(H.edges)

# Limpando todo o grafo
G.clear()

# O NetworkX ignora sem avisos a adicao de nohs ou arestas que já estao presentes
G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')

# Checar numero de nohs
G.number_of_nodes()

# Checar numero de arestas
G.number_of_edges()

# Ordem de adjacencias é a ordem em que as arestas foram adicionadas para
# order adjacency reporting (e.g., G.adj, G.successors, G.predecessors)
# por outro lado G.edges leva em conta a ordem dos nohs e suas adjacencias ****** <- Revisar
DG = nx.DiGraph()
DG.add_edge(2, 1)   # adds the nodes in order 2, 1
DG.add_edge(1, 3)
DG.add_edge(2, 4)
DG.add_edge(1, 2)
assert list(DG.successors(2)) == [1, 4]
assert list(DG.edges) == [(2, 1), (2, 4), (1, 3), (1, 2)]