from matplotlib import pyplot as plt, animation
import networkx as nx
import random

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()

G = nx.DiGraph()
G.add_nodes_from([0, 1, 2, 3, 4])

nx.draw(G, with_labels=True)

def animate(frame):
   fig.clear()
   num1 = random.randint(0, 4)
   num2 = random.randint(0, 4)
   G.add_edges_from([(num1, num2)])
   nx.draw(G, with_labels=True)

ani = animation.FuncAnimation(fig, animate, frames=6, interval=1000, repeat=True)

plt.show()