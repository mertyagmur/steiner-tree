import networkx as nx
import math

def repetitive_shortest_path(graph, terminals):
    # Find shortest paths from each terminal to other nodes
    shortest = {t: {'length': l, 'path': p} \
                for t in terminals for l, p in \
                    [nx.single_source_dijkstra(graph, t, weight='weight')]}

    # Make sure that when there are multiple shortest paths, the stored 
    # shortest path from t1 to t2 is identical to the shortest path from t2 to t1.
    for i, t1 in enumerate(terminals):
        for j, t2 in enumerate(terminals[i+1:], start=i+1):
            path = shortest[t1]['path'][t2]
            shortest[t2]['path'][t1] = path

    processed_terminal_num = 1
    terminals_covered = [terminals[0]]

    steiner_tree = nx.Graph()
    all_terminals = len(terminals)

    while processed_terminal_num < all_terminals:
        shortest_dist_to_uncovered_termin = math.inf
        shortest_dist_uncovered_terminal = None
        current_terminal = None

        for terminal in terminals_covered:
            length = shortest[terminal]['length']
            unterminals_covered = [(x, length[x]) for x in length if x not in terminals_covered and x != terminal and x in terminals]

            closest_uncovered_terminal, min_dist_to_uncovered_terminal = min(unterminals_covered, key=lambda x: x[1])

            if min_dist_to_uncovered_terminal < shortest_dist_to_uncovered_termin:
                current_terminal = terminal
                shortest_dist_to_uncovered_termin = min_dist_to_uncovered_terminal
                shortest_dist_uncovered_terminal = closest_uncovered_terminal


        # Include the edges from the shortest path to the selected uncovered terminal into the existing tree
        shortest_path = shortest[current_terminal]['path'][shortest_dist_uncovered_terminal]
        for index in range(len(shortest_path) - 1):
            u = shortest_path[index]
            v = shortest_path[index + 1]
            steiner_tree.add_edge(u, v, weight=graph[u][v]['weight'])

        processed_terminal_num += 1
        terminals_covered.append(shortest_dist_uncovered_terminal)

    # Discard non-terminals with degree 1
    while any(node for node in steiner_tree.nodes if node not in terminals \
              and steiner_tree.degree[node] == 1):
        steiner_tree.remove_nodes_from(node for node in steiner_tree.nodes if \
                                       node not in terminals and steiner_tree.degree[node] == 1)


    return steiner_tree