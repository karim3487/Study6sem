from astar_algorithm import astar
from ant_colony_algorithm import ant_colony_algorithm

graph = {
    1: {2: {'weight': 23, 'heuristic': 2}, 5: {'weight': 125, 'heuristic': 5}},
    2: {1: {'weight': 23, 'heuristic': 1}, 3: {'weight': 32, 'heuristic': 3},
        4: {'weight': 8, 'heuristic': 4}, 5: {'weight': 23, 'heuristic': 5}},
    3: {2: {'weight': 32, 'heuristic': 2}, 4: {'weight': 22, 'heuristic': 4},
        5: {'weight': 8, 'heuristic': 5}},
    4: {3: {'weight': 22, 'heuristic': 4}, 2: {'weight': 8, 'heuristic': 2}},
    5: {1: {'weight': 125, 'heuristic': 1}, 2: {'weight': 23, 'heuristic': 2},
        3: {'weight': 8, 'heuristic': 3}}
}
start_node = 1
end_node = 3

print(astar(graph, start_node, end_node))

num_ants = 10
num_iterations = 100
evaporation_rate = 0.5
alpha = 2
beta = 1
Q = 2

path, best_path_length, search_log = ant_colony_algorithm(graph, start_node, end_node, num_ants,
                                                          num_iterations,
                                                          evaporation_rate, alpha, beta, Q)

print("Best Path:", path)
print("Best Path Length:", best_path_length)

for log in search_log:
    print(f"Итерация {log['iteration']}:")
    print('\tФерамоны:', log['pheromone'])
    print('\tПройденные муравьями пути:', log['paths'])
    print('\tДлина путей:', log['path_lengths'])
