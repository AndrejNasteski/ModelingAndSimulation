import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

g = nx.Graph()

g.add_node(None)
g.add_node(None)
g.add_node(None)

nx.draw(g, with_labels=True)
plt.show()

# edges = [(i, np.random.randint(20, 30)) for i in range(20)]
# print(edges)
