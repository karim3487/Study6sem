import graphviz
from networkx.drawing.nx_agraph import graphviz_layout


class GameNode:
    def __init__(self, value, children=None):
        self.value = value  # Оценка вершины
        self.children = children or []  # Дети вершины

    def add_child(self, child_node):
        self.children.append(child_node)


class GameTree:
    def __init__(self, root):
        self.root = root  # Корневая вершина игрового дерева


# Создание вершин дерева
leaf1 = GameNode(3)
leaf2 = GameNode(7)
leaf3 = GameNode(2)
leaf4 = GameNode(5)

# Создание внутренних вершин и связей
inner_node1 = GameNode(0, [leaf1, leaf2])
inner_node2 = GameNode(0, [leaf3, leaf4])
root = GameNode(0, [inner_node1, inner_node2])

# Создание игрового дерева
game_tree = GameTree(root)

import networkx as nx
import matplotlib.pyplot as plt


# Создание графа Graphviz
dot = graphviz.Digraph()

# Рекурсивная функция для построения графа
def build_graph(node, parent_node=None):
    # Создание узла и добавление его в граф
    dot.node(str(id(node)), str(node.value))

    # Создание ребра между текущим и родительским узлами
    if parent_node is not None:
        dot.edge(str(id(parent_node)), str(id(node)))

    # Рекурсивный вызов для каждого ребенка текущего узла
    for child in node.children:
        build_graph(child, node)

# Построение графа
build_graph(game_tree.root)

# Вывод графа
dot.format = 'png'  # Формат вывода (можно изменить на другой поддерживаемый формат)
dot.render('game_tree', view=True)

