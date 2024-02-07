from ant_colony_algorithm import ant_colony_algorithm
import matplotlib.pyplot as plt
import networkx as nx
from networkx import NetworkXNoPath

from astar_algorithm import astar

G = nx.Graph()
MESSAGE_ERROR = 'Вы ввели что-то не то, попробуйте еще раз!'
START_NODE = None
END_NODE = None


def draw_graph(g):
    position = pos
    colors = set_color_map()

    nx.draw_networkx(g, pos=position, node_color=colors, with_labels=True, node_size=800, font_size=14)
    edge_labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, position, edge_labels=edge_labels)

    node_labels = nx.get_node_attributes(g, 'heuristic')
    for node, h in node_labels.items():
        x, y = position[node]
        plt.text(x + 0.1, y + 0.1, s=h, horizontalalignment='center', color='blue', fontsize=13)
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


def set_heuristic(node_name):
    while True:
        while True:
            try:
                return int((input(f'Введите эмпирическую стоимость для узла {node_name}: ')))
            except ValueError:
                print("Попробуйте еще раз!")


def get_integer(s):
    while True:
        try:
            return int(input(s))
        except ValueError:
            print("Вы ввели не целое число\nПопробуйте еще раз")


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
            c_m.append('#2d912c')
        elif node == END_NODE:
            c_m.append('#ff1212')
        else:
            c_m.append('#2bc8fc')
    return c_m


def print_adjacency_matrix():
    nodelist = list(G.nodes)
    matrix = nx.to_pandas_adjacency(G, nodelist=nodelist)
    print(matrix)


# count_nodes = get_count_node()
count_nodes = 5
heuristic_lst = []
for i in range(count_nodes):
    print(f"#{i + 1}", end="\t")
    G.add_node(i + 1)
    heuristic_lst.append(set_heuristic(i + 1))
nx.set_node_attributes(G, {node: heuristic_lst[i] for i, node in enumerate(G.nodes())}, 'heuristic')
pos = nx.spring_layout(G)
draw_graph(G)

while True:
    choice = input("Хотите добавить ребро?\n1. Да\n2. Нет\n>>> ")
    match choice:
        case '1':
            if check_count_edges():
                edge, weight = add_edge()
                G.add_edge(*edge, weight=weight)
                draw_graph(G)
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
draw_graph(G)
print_adjacency_matrix()

graph_without_heuristic = nx.to_dict_of_dicts(G)
h = nx.get_node_attributes(G, 'heuristic')
graph = {}
for node in graph_without_heuristic:
    graph[node] = {}
    for neighbor in graph_without_heuristic[node]:
        weight = graph_without_heuristic[node][neighbor]['weight']
        heuristic = h[neighbor]
        graph[node][neighbor] = {'weight': weight, 'heuristic': heuristic}


while True:
    choice = input("Выберите алгоритм:\n1. A*\n2. Агоритм муравьиной колонии\n3. Выход>>> ")
    match choice:
        case '1':
            path, cost = astar(graph, START_NODE, END_NODE)
            print("Кртотчайший путь: ", end='')
            print(*path, sep=' -> ')
            print("Цена пути:", cost)
            draw_graph(G)
        case '2':
            num_ants = get_integer('Введите количество муравьев: ')
            num_iterations = get_integer('Введите количество итераций: ')
            evaporation_rate = 0.8
            alpha = 1.2
            beta = 0.2
            Q = 1

            path, best_path_length = ant_colony_algorithm(graph, START_NODE, END_NODE, num_ants,
                                                          num_iterations,
                                                          evaporation_rate, alpha, beta, Q)

            print("Кротчайший путь: ", end='')
            print(*path, sep=' -> ')
            print("Цена пути:", best_path_length)
            draw_graph(G)
        case '3':
            break
        case __:
            print(MESSAGE_ERROR)
