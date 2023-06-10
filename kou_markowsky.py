import networkx as nx

def kou_markowsky(graph, terminals):
    # Step 1: Create a complete distance graph
    complete_graph = nx.Graph()
    for u in terminals:
        for v in terminals:
            if u != v:
                shortest_path = nx.shortest_path(graph, source=u, target=v, weight='weight')
                path_length = nx.shortest_path_length(graph, source=u, target=v, weight='weight')
                complete_graph.add_edge(u, v, weight=path_length, path=shortest_path)

    # Step 2: Find the minimum spanning tree
    mst = nx.minimum_spanning_tree(complete_graph)

    # Step 3: Create the Steiner tree
    steiner_tree = nx.Graph()
    for u, v, attrs in mst.edges(data=True):
        shortest_path = attrs['path']
        for i in range(len(shortest_path) - 1):
            u, v = shortest_path[i], shortest_path[i + 1]
            steiner_tree.add_edge(u, v, weight=graph[u][v]['weight'])

    # Step 4: Remove unnecessary edges
    leaves = [node for node in steiner_tree.nodes() if steiner_tree.degree(node) == 1]
    steiner_vertices = set()
    for leaf in leaves:
        if leaf not in terminals:
            steiner_vertices.add(leaf)
    while len(steiner_vertices) > 0:
        leaf = steiner_vertices.pop()
        neighbor = next(steiner_tree.neighbors(leaf))
        steiner_tree.remove_edge(leaf, neighbor)
        if steiner_tree.degree(neighbor) == 1:
            steiner_vertices.add(neighbor)

    # Step 5: Return the Steiner tree
    return steiner_tree