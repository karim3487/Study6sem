import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []


def draw_tree(node):
    G = nx.Graph()
    traverse_tree(node, G)
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=12, font_weight='bold')
    plt.title("Игровое дерево")
    plt.show()


def traverse_tree(node, graph):
    graph.add_node(node.value)
    for child in node.children:
        graph.add_edge(node.value, child.value)
        traverse_tree(child, graph)


# Создаем игровое дерево
root = Node(0)
node1 = Node(3)
node2 = Node(5)
node3 = Node(2)
node4 = Node(9)

root.children = [node1, node2, node3]
node1.children = [node4]

# Отображаем дерево
draw_tree(root)
