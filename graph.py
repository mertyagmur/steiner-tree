import networkx as nx
import matplotlib.pyplot as plt

def gr_to_stp(path, convert=False):
        line = "33D32945 STP File, STP Format Version 1.0\n\n"
        with open(path, "r") as f:
            with open(f"./instances/{path[-14:]}",'w') as f2: 
                f2.write(line)
                f2.write(f.read())
            #os.remove(path)
            #os.rename('stp_format.gr', path)
        return f"./instances/{path[-14:]}"

def stp_to_graph(path):
    G = nx.Graph()
    section = ""
    with open(path, "r") as stp_file:
        for line in stp_file:
            line = line.strip()
            if line != "":
                line_start = line.split()[0]
                line_content = line.split()[1:]
                if line_start == "SECTION":
                    section = line_content[0]
                if line_start == "E" and section == "Graph":
                    G.add_edge(int(line_content[0]), 
                                int(line_content[1]), 
                                weight=int(line_content[2]))
                elif line_start == "T" and section == "Terminals":
                    G.nodes[int(line_content[0])]["terminal"] = True
                    G.graph["terminals"] = G.graph.get("terminals", []) + [int(line_content[0])]
    return G