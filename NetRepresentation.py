import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

graph = nx.Graph()

initial_population = 20
initial_agg_percentage = 0.3
num_food_nodes = 10
total_nodes = initial_population + num_food_nodes

population_nodes = []
positions = {}
color_map = []
edges = [(i, np.random.randint(initial_population, total_nodes)) for i in range(initial_population)]

for i in range(total_nodes):
    if i < int(initial_population * initial_agg_percentage):  # aggressive nodes
        graph.add_node(i, food_amount=0, aggressive=True, food_node=False)
        positions[i] = [0, i]
        color_map.append('red')
    elif int(initial_population * initial_agg_percentage) <= i < initial_population:  # passive nodes
        graph.add_node(i, food_amount=0, aggressive=False, food_node=False)
        positions[i] = [0, i]
        color_map.append('blue')
    elif i >= initial_population:  # food nodes
        graph.add_node(i, food_amount=3, food_node=True)
        positions[i] = [10, i - 15]  # change position parametar
        color_map.append('green')

graph.add_edges_from(edges)

edges_to_food = {}  # which food nodes connect with which creature nodes
for i in range(initial_population, total_nodes):
    edges_to_food[i] = [0, []]
for (creature, food) in graph.edges:
    edges_to_food[food][0] += 1
    edges_to_food[food][1].append(creature)

"""
    passive food total: 1/(N+num_agg)
    aggressive food total: 1 - passive food total
    
    passive food per creature: passive food total / num_pass
    aggressive food per creature: aggressive food total / num_agg
"""

for food_nodes in edges_to_food:  # for each food node
    total_creatures = len(edges_to_food[food_nodes][1])
    num_passive = 0
    num_aggressive = 0
    for creatures in edges_to_food[food_nodes][1]:
        if graph.nodes[creatures]["aggressive"]:
            num_aggressive += 1
        else:
            num_passive += 1

    food_aggressive = 0
    food_passive = 0
    if num_passive == 0 and num_aggressive == 0:
        continue
    elif num_aggressive == 0:
        food_passive = graph.nodes[food_nodes]["food_amount"] / num_passive
    elif num_passive == 0:
        food_aggressive = graph.nodes[food_nodes]["food_amount"] / num_aggressive
    else:
        passive_percentage = 1 / (total_creatures + num_aggressive)
        aggressive_percentage = 1 - passive_percentage
        food_passive = (passive_percentage / num_passive) * graph.nodes[food_nodes]["food_amount"]
        food_aggressive = (aggressive_percentage / num_aggressive) * graph.nodes[food_nodes]["food_amount"]

    for creatures in edges_to_food[food_nodes][1]:  # assign food to each creature node
        if graph.nodes[creatures]["aggressive"]:
            graph.nodes[creatures]["food_amount"] += food_aggressive
        else:
            graph.nodes[creatures]["food_amount"] += food_passive

new_num_agg = int(initial_agg_percentage * initial_population)
new_num_pass = initial_population - new_num_agg

print(new_num_agg, new_num_pass)
for i in range(initial_population):
    print(i, graph.nodes[i]["aggressive"], graph.nodes[i]["food_amount"])
    if graph.nodes[i]["food_amount"] < 0.6:  # not enough food, dies
        if graph.nodes[i]["aggressive"]:  # is aggressive
            new_num_agg -= 1
        else:  # is passive
            new_num_pass -= 1
    if graph.nodes[i]["food_amount"] > 1.5:  # if 0.6 < food < 1.5 it survives, if food > 1.5 it reproduces
        if graph.nodes[i]["aggressive"]:  # is aggressive
            new_num_agg += 1
        else:  # is passive
            new_num_pass += 1

nx.draw(graph, node_color=color_map, pos=positions, with_labels=True)
plt.show()
