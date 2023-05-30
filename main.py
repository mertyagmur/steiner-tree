import networkx as nx
from graph import stp_to_graph
from melhorn import mehlhorn_algorithm
from mehlhorn2 import steiner_tree_mehlhorn

def check_solution(graph):
    if nx.is_connected(graph) and nx.is_tree(graph):
        for node_t in graph.graph["terminals"]:
            if node_t not in graph.nodes:
                return False
        return True
    
def main():
    path = "./test/steinlib/B/b01.stp"

    G = stp_to_graph(path)
    my_pos = nx.spring_layout(G, seed = 42)
    nx.draw(G, pos=my_pos, with_labels=True)
    #print(G.graph["terminals"])
    #plt.show()

    steiner_tree = nx.algorithms.approximation.steinertree.steiner_tree(G, G.graph["terminals"], method="mehlhorn")
    
if __name__ == "__main__":
    main()