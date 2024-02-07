from astar_algorithm import astar
from ant_colony_algorithm import ant_colony_algorithm

graph = {
    1: {2: {'weight': 23, 'heuristic': 2}, 5: {'weight': 125, 'heuristic': 5}},
    2: {1: {'weight': 23, 'heuristic': 1}, 3: {'weight': 12, 'heuristic': 3},
        4: {'weight': 8, 'heuristic': 4}, 5: {'weight': 23, 'heuristic': 5}},
    3: {2: {'weight': 12, 'heuristic': 2}, 4: {'weight': 22, 'heuristic': 4},
        5: {'weight': 8, 'heuristic': 5}},
    4: {3: {'weight': 22, 'heuristic': 4}, 2: {'weight': 8, 'heuristic': 2}, 5: {'weight': 15, 'heuristic': 5}},
    5: {1: {'weight': 125, 'heuristic': 1}, 2: {'weight': 23, 'heuristic': 2},
        3: {'weight': 8, 'heuristic': 3}, 4: {'weight': 15, 'heuristic': 5}}
}
start_node = 1
end_node = 5

print(astar(graph, start_node, end_node))

num_ants = 10
num_iterations = 100
evaporation_rate = 0.8
alpha = 1.2
beta = 0.2
Q = 1

path, best_path_length = ant_colony_algorithm(graph, start_node, end_node, num_ants,
                                              num_iterations,
                                              evaporation_rate, alpha, beta, Q)

print("Кротчайший путь: ", end='')
print(*path, sep=' -> ')
print("Цена пути:", best_path_length)
