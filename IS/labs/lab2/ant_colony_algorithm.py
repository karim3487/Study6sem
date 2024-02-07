import random
from tabulate import tabulate


def print_pher(pheromone):
    headers = [''] + list(pheromone.keys())
    rows = []

    for row_key, row_data in pheromone.items():
        row = [row_key] + [f"{row_data.get(column_key, '–'):.5f}" if row_data.get(column_key) is not None else '–' for
                           column_key in headers[1:]]
        rows.append(row)

    table = tabulate(rows, headers, tablefmt="grid")
    print(table)


def print_paths(paths, path_lengths):
    table_data = [
        ["Путь"] + [str(row) for row in paths],
        ["Значения"] + [str(value) for value in path_lengths]
    ]

    table = tabulate(table_data, tablefmt="grid")
    print(table)


def ant_colony_algorithm(graph, start_node, end_node, num_ants, num_iterations, evaporation_rate, alpha, beta, Q):
    pheromone = initialize_pheromone(graph)  # Инициализация феромонов на всех ребрах = 1.
    best_path = None
    best_path_length = float('inf')  # Иницилизация кротчайшего пути бесконечностью

    search_log = []  # Журнал поиска, содержащий информацию о каждой итерации.

    for i in range(num_iterations):
        paths = []
        path_lengths = []

        # Создание пути для каждого муравья
        for _ in range(num_ants):
            path = construct_path(graph, start_node, end_node, pheromone, alpha, beta)
            path_length = calculate_path_length(graph, path)

            paths.append(path)
            path_lengths.append(path_length)

            # Обновление лучшего пути, если текущий путь лучше
            if path_length < best_path_length:
                best_path = path
                best_path_length = path_length

        print("Итерация", i + 1)

        print("Феромоны:")
        print_pher(pheromone)

        print("Пути:")
        print_paths(paths, path_lengths)

        # Запись информации о поиске для первых 5 итераций
        # if i > :

        # Обновление феромонов на ребрах
        update_pheromone(pheromone, paths, path_lengths, evaporation_rate, Q)

    return best_path, best_path_length


def initialize_pheromone(graph):
    pheromone = {}

    for node in graph:
        pheromone[node] = {}
        for neighbor in graph[node]:
            pheromone[node][neighbor] = 1.0

    return pheromone


def construct_path(graph, start_node, end_node, pheromone, alpha, beta):
    # Построение пути муравья от начальной до конечной вершины
    path = [start_node]
    current_node = start_node

    while current_node != end_node:
        probabilities = calculate_probabilities(graph, current_node, path, pheromone, alpha, beta)
        next_node = select_next_node(probabilities)
        path.append(next_node)
        current_node = next_node

    return path


def calculate_probabilities(graph, current_node, path, pheromone, alpha, beta):
    # Вычисление вероятностей перехода муравья в соседние вершины
    probabilities = []
    total = 0.0

    for neighbor in graph[current_node]:
        if neighbor not in path:
            pheromone_level = pheromone[current_node][neighbor]
            heuristic = graph[current_node][neighbor]['heuristic']
            probability = pheromone_level ** alpha * heuristic ** beta
            probabilities.append((neighbor, probability))
            total += probability

    # Нормализация вероятностей
    probabilities = [(neighbor, probability / total) for neighbor, probability in probabilities]
    return probabilities


def select_next_node(probabilities):
    # Выбор следующей вершины на основе вероятностей
    random_value = random.uniform(0, 1)
    cumulative_probability = 0.0

    for neighbor, probability in probabilities:
        cumulative_probability += probability
        if random_value <= cumulative_probability:
            return neighbor


def calculate_path_length(graph, path):
    # Вычисление длины пути
    length = 0

    for i in range(len(path) - 1):
        node = path[i]
        next_node = path[i + 1]
        length += graph[node][next_node]['weight']

    return length


def update_pheromone(pheromone, paths, path_lengths, evaporation_rate, Q):
    # Обновление феромонов на ребрах
    for node in pheromone:
        for neighbor in pheromone[node]:
            pheromone[node][neighbor] *= (1 - evaporation_rate)

    for i in range(len(paths)):
        path = paths[i]
        path_length = path_lengths[i]

        for j in range(len(path) - 1):
            node = path[j]
            next_node = path[j + 1]
            pheromone[node][next_node] += Q / path_length
