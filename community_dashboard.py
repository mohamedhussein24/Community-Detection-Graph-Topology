import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import label_propagation_communities
import community as community_louvain

st.title("Community Detection Dashboard")
uploaded_file = st.file_uploader("Upload edge list file (e.g., ca-GrQc.txt)", type="txt")

if uploaded_file:
    G = nx.read_edgelist(uploaded_file, comments='#', create_using=nx.Graph())

    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()

    st.write(f"Graph loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

    # Select algorithm
    method = st.selectbox("Select Community Detection Method", ["Louvain", "Label Propagation"])

    # Run algorithm
    if method == "Louvain":
        partition = community_louvain.best_partition(G)
        modularity = community_louvain.modularity(partition, G)
        communities = [set() for _ in range(max(partition.values()) + 1)]
        for node, group in partition.items():
            communities[group].add(node)

    elif method == "Label Propagation":
        communities_gen = label_propagation_communities(G)
        communities = list(communities_gen)
        partition = {node: idx for idx, com in enumerate(communities) for node in com}
        modularity = "N/A (not calculated)"

   
    st.write(f"Number of communities: {len(communities)}")
    st.write(f"Modularity: {modularity}")
    st.subheader("Graph Visualization")
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_size=20, cmap=plt.cm.Set3,
                           node_color=[partition[node] for node in G.nodes()], ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.2, ax=ax)
    ax.set_title(f"{method} Community Detection")
    ax.set_axis_off()
    st.pyplot(fig)
else:
    st.info("Please upload a graph edge list file to begin.")
