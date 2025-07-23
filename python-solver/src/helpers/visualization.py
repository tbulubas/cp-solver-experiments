import networkx as nx
import matplotlib.pyplot as plt


def plot_task_dependency_dag(tasks, task_id_map):
    G = nx.DiGraph()

    # Reverse map for labels: index → (run_id, template_id)
    index_to_key = {v: k for k, v in task_id_map.items()}

    # Add all nodes
    for i, key in index_to_key.items():
        label = f"{i}\n{key[1][-4:]}"  # Short taskId for readability
        G.add_node(i, label=label)

    # Add edges based on dependencies
    for j, task in enumerate(tasks):
        for pred in task.get("dependingOn", []):
            pred_key = (pred["prodId"], pred["taskId"])
            if pred_key in task_id_map:
                i = task_id_map[pred_key]
                G.add_edge(i, j)

        imm_pred = task.get("preceding")
        if imm_pred:
            pred_key = (imm_pred["prodId"], imm_pred["taskId"])
            if pred_key in task_id_map:
                i = task_id_map[pred_key]
                G.add_edge(i, j)

    # Draw graph
    pos = nx.spring_layout(G, seed=42)  # or nx.nx_pydot.graphviz_layout(G, prog='dot')
    # pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
    labels = nx.get_node_attributes(G, 'label')

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=1200, node_color="lightblue", arrows=True, font_size=8)
    plt.title("Task Dependency DAG")
    plt.tight_layout()
    plt.show()
