import networkx as nx

from modules.relationship_manager import get_all_relationships


class GraphEngine:

    def __init__(self):

        self.graph = nx.DiGraph()

        self.build_graph()

    # ==============================
    # Build Graph
    # ==============================

    def build_graph(self):

        self.graph.clear()

        relationships = get_all_relationships()

        for relationship in relationships:

            self.graph.add_edge(

                relationship["source_name"],

                relationship["destination_name"],

                relationship_type=relationship["relationship_type"]

            )

    # ==============================
    # Return Graph
    # ==============================

    def get_graph(self):

        return self.graph

    # ==============================
    # Statistics
    # ==============================

    def total_nodes(self):

        return self.graph.number_of_nodes()

    def total_edges(self):

        return self.graph.number_of_edges()

    # ==============================
    # Node List
    # ==============================

    def node_list(self):

        return list(self.graph.nodes())

    # ==============================
    # Edge List
    # ==============================

    def edge_list(self):

        return list(self.graph.edges())