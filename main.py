import networkx as nx
from graph import stp_to_graph
from matplotlib import pyplot as plt
import pandas as pd
import os
from repetitive_shortest_path import repetitive_shortest_path
from kou_markowsky import kou_markowsky
import time


def main():
    path_to_instances = "./New folder/instances/"
    optimum_values = pd.read_csv("./New folder/track1.csv")
    results = []
    for instance in os.listdir(path_to_instances):
        optimum_value = optimum_values.loc[optimum_values["paceName"].str.lower().str.contains(instance), "opt"].values[0]
        print("-"*60)
        print(f"Benchmark instance: {instance}")
        print(f"Optimum value for the benchmark instance: {optimum_value}")


        G = stp_to_graph(path_to_instances + instance)

        """ my_pos = nx.spring_layout(G, seed = 42)
        nx.draw(G, pos=my_pos, with_labels=True)
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, my_pos, edge_labels=labels)
        plt.show() """

        print(f"Total weight of the instance graph: {G.size(weight='weight')}")

        st_rsp_weight = 0
        number_of_runs_rsp = 0
        execution_times_rsp = []
        best_result_rsp = 0
        while st_rsp_weight != optimum_value:
            if number_of_runs_rsp == 1:
                print("Maximum allocated runs reached")
                break
            start_time = time.time()
            st_rsp = repetitive_shortest_path(G, G.graph["terminals"])
            end_time = time.time()
            execution_times_rsp.append(end_time-start_time)

            st_rsp_weight = st_rsp.size(weight="weight")
            if st_rsp_weight > best_result_rsp:
                best_result_rsp = st_rsp_weight
            number_of_runs_rsp += 1

        st_kou_markowsky_weight = 0
        number_of_runs_kou_markowsky = 0
        execution_times_kou_markowsky = []
        best_result_kou_markowsky = 0
        while st_kou_markowsky_weight != optimum_value:
            if number_of_runs_kou_markowsky == 1:
                print("Maximum allocated runs reached")
                break
            start_time = time.time()
            st_kou_markowsky = kou_markowsky(G, G.graph["terminals"])
            end_time = time.time()
            execution_times_kou_markowsky.append(end_time-start_time)

            st_kou_markowsky_weight = st_kou_markowsky.size(weight="weight")
            if st_kou_markowsky_weight > best_result_kou_markowsky:
                best_result_kou_markowsky = st_kou_markowsky_weight
            number_of_runs_kou_markowsky += 1

        results.append({
            "Instance Name": instance, 
            "Optimum Value": optimum_value, 
            "RSP Best Result": best_result_rsp, 
            "RSP Avg. Time": sum(execution_times_rsp)/len(execution_times_rsp)/1000, 
            "RSP Best Result Acc.": best_result_rsp/optimum_value, 
            "kou_markowsky Best Result": best_result_kou_markowsky, 
            "kou_markowsky Avg. Time": sum(execution_times_kou_markowsky)/len(execution_times_kou_markowsky)/1000, 
            "kou_markowsky Best Result Acc.": best_result_kou_markowsky/optimum_value
        })

    results_df = pd.DataFrame(results, columns=["Instance Name", "Optimum Value", "RSP Best Result", "RSP Avg. Time", "RSP Best Result Acc.", "kou_markowsky Best Result", "kou_markowsky Avg. Time", "kou_markowsky Best Result Acc."])
    results_df.to_excel("results.xlsx", index=False)
if __name__ == "__main__":
    main()
    