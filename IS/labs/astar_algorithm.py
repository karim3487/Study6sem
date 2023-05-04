def astar(graph, start, goal):
    # Initialize the open and closed sets.
    open_set = set([start])
    closed_set = set()

    # Initialize the parent and cost variables.
    parent = {}
    cost = {}
    for node in graph:
        parent[node] = None
        cost[node] = float('inf')

    # Set the cost of the start node to 0.
    cost[start] = 0

    # While the open set is not empty:
    while open_set:
        # Find the node with the lowest f(n) value in the open set.
        node = min(open_set, key=lambda n: cost[n] + (graph[n].get('heuristic', 0)))

        # Remove the node from the open set.
        open_set.remove(node)

        # If the node is the goal node, return the path.
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], cost[goal]

        # Add the node to the closed set.
        closed_set.add(node)

        # For each neighbor of the node:
        for neighbor in graph[node]:
            # Calculate the tentative cost of the neighbor.
            tentative_cost = cost[node] + graph[node][neighbor]['weight']

            # If the tentative cost is less than the current cost of the neighbor:
            if tentative_cost < cost[neighbor]:
                # Update the cost of the neighbor.
                cost[neighbor] = tentative_cost

                # Set the parent of the neighbor.
                parent[neighbor] = node

                # Add the neighbor to the open set.
                open_set.add(neighbor)

        # Output the contents of the open and unopened vertices at each step of the search.
        print("Шаг {}:".format(len(closed_set)))
        print("Открытые на этом шаге: {}".format(open_set))
        print("Посещенные: {}".format(closed_set))
        print()

    # The goal node was not found.
    return []
