import matplotlib.pyplot as plt
import networkx as nx
from networkx import NetworkXNoPath
from collections import deque

G = nx.Graph()
MESSAGE_ERROR = 'Вы ввели что-то не то, попробуйте еще раз!'
START_NODE = None
END_NODE = None


def draw_graph():
    colors = set_color_map()
    nx.draw(G, pos, with_labels=True, font_color="whitesmoke", node_size=500, node_color=colors)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


def get_count_node():
    while True:
        try:
            count_node = int((input("Введите количество узлов: ")))
            if count_node < 15:
                raise ValueError
            return count_node
        except ValueError:
            print("Попробуйте еще раз!")


def is_correct_node(node):
    if node in list(G.nodes):
        return True
    return False


def is_correct_edge(nodes_to_join, nodes_lst):
    try:
        nodes_to_join = [int(item) for item in nodes_to_join]
    except ValueError:
        return False
    is_two_nodes = len(nodes_to_join) == 2
    is_G_contains_nodes = set(nodes_to_join).issubset(set(nodes_lst))
    if is_two_nodes and is_G_contains_nodes:
        return True
    return False


def name_node():
    graph_nodes = list(G.nodes())
    while True:
        while True:
            try:
                name = int((input("Введите название для узла(цифру): ")))

                if name in graph_nodes:
                    raise ValueError
                return name
            except ValueError:
                print("Попробуйте еще раз!")


def add_edge():
    nodes_lst = list(G.nodes)
    while True:
        print(f"Вот список вершин: {nodes_lst}\n")
        nodes_to_join = input(f"Введите ДВЕ вершины которые хотите соединить: ").split(' ')
        if is_correct_edge(nodes_to_join, nodes_lst):
            nodes_to_join = [int(item) for item in nodes_to_join]
            while True:
                try:
                    weight = int(input("Введите вес для этого ребра: "))
                    return tuple(nodes_to_join), weight
                except ValueError:
                    print("NO OK")
        else:
            print("NO OK")


def check_count_edges():
    count_edges = len(G.nodes)
    if count_edges == 0:
        return True
    max_count = count_edges * (count_edges - 1) / 2
    if count_edges >= max_count:
        return False
    return True


def node_define(edge_type):
    while True:
        try:
            node = int(input(f"Введите {edge_type} вершину графа: "))
            if is_correct_node(node):
                return node
        except ValueError:
            print(MESSAGE_ERROR)


def set_color_map():
    c_m = []
    for node in G.nodes:
        if node is START_NODE:
            c_m.append('#55ff12')
        elif node == END_NODE:
            c_m.append('#ff1212')
        else:
            c_m.append('#ff7af2')
    return c_m


def print_adjacency_matrix():
    nodelist = list(G.nodes)
    matrix = nx.to_pandas_adjacency(G, nodelist=nodelist)
    print(matrix)


# def a_star_algorithm(graph, start, stop):
#     d = {
#         1: {
#             2: {'weight': 12},
#             5: {'weight': 21}
#         },
#         2: {
#             1: {'weight': 12},
#             3: {'weight': 32}
#         },
#         3: {
#             2: {'weight': 32}
#         },
#         4: {},
#         5: {
#             1: {'weight': 21}
#         }
#     }
#     # In this open_lst is a lisy of nodes which have been visited, but who's
#     # neighbours haven't all been always inspected, It starts off with the start
#     # node
#     # And closed_lst is a list of nodes which have been visited
#     # and who's neighbors have been always inspected
#     open_lst = set([start])
#     closed_lst = set([])
#
#     # poo has present distances from start to all other nodes
#     # the default value is +infinity
#     poo = {}
#     poo[start] = 0
#
#     # par contains an adjac mapping of all nodes
#     par = {}
#     par[start] = start
#
#     while len(open_lst) > 0:
#         n = None
#
#         # it will find a node with the lowest value of f() -
#         for v in open_lst:
#             if n is None or poo[v] + graph[v] < poo[n] + self.h(n):
#                 n = v;
#
#         if n == None:
#             print('Path does not exist!')
#             return None
#
#         # if the current node is the stop
#         # then we start again from start
#         if n == stop:
#             reconst_path = []
#
#             while par[n] != n:
#                 reconst_path.append(n)
#                 n = par[n]
#
#             reconst_path.append(start)
#
#             reconst_path.reverse()
#
#             print('Path found: {}'.format(reconst_path))
#             return reconst_path
#
#         # for all the neighbors of the current node do
#         for (m, weight) in self.get_neighbors(n):
#             # if the current node is not presentin both open_lst and closed_lst
#             # add it to open_lst and note n as it's par
#             if m not in open_lst and m not in closed_lst:
#                 open_lst.add(m)
#                 par[m] = n
#                 poo[m] = poo[n] + weight
#
#             # otherwise, check if it's quicker to first visit n, then m
#             # and if it is, update par data and poo data
#             # and if the node was in the closed_lst, move it to open_lst
#             else:
#                 if poo[m] > poo[n] + weight:
#                     poo[m] = poo[n] + weight
#                     par[m] = n
#
#                     if m in closed_lst:
#                         closed_lst.remove(m)
#                         open_lst.add(m)
#
#         # remove n from the open_lst, and add it to closed_lst
#         # because all of his neighbors were inspected
#         open_lst.remove(n)
#         closed_lst.add(n)
#
#     print('Path does not exist!')
#     return None


def ant_colony_algorithm():
    ...


# count_nodes = get_count_node()
count_nodes = 5

for i in range(count_nodes):
    print(f"#{i + 1}", end="\t")
    name = name_node()
    G.add_node(name)
pos = nx.spring_layout(G)
draw_graph()

while True:
    choice = input("Хотите добавить ребро?\n1. Да\n2. Нет\n>>> ")
    match choice:
        case '1':
            if check_count_edges():
                edge, weight = add_edge()
                G.add_edge(*edge, weight=weight)
                draw_graph()
            else:
                print("Вы больше не можете добавить ребро")
        case '2':
            break
        case __:
            print(MESSAGE_ERROR)

while True:
    START_NODE = node_define('начальную')
    END_NODE = node_define('конечную')
    try:
        nx.dijkstra_path(G, START_NODE, END_NODE)
        break
    except NetworkXNoPath:
        print('Эти вершины не соединены, введите другие')

set_color_map()
draw_graph()
print_adjacency_matrix()

while True:
    choice = input("Выберите алгоритм:\n1. A*\n2. Агоритм муравьиной колонии\n>>> ")
    match choice:
        case '1':
            # a_star_algorithm()
            print(nx.to_dict_of_dicts(G))
            print(nx.astar_path(G, START_NODE, END_NODE))
            break
        case '2':
            ant_colony_algorithm()
            break
        case __:
            print(MESSAGE_ERROR)

draw_graph()

