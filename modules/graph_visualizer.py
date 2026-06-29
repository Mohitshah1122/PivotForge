from pyvis.network import Network

from modules.graph_engine import GraphEngine


class GraphVisualizer:

    def __init__(self):

        self.engine = GraphEngine()

    def generate_graph(self):

        self.engine.build_graph()

        graph = self.engine.get_graph()

        net = Network(

            height="750px",

            width="100%",

            bgcolor="#121212",

            font_color="white",

            directed=True

        )

        # -----------------------------
        # Add Nodes
        # -----------------------------

        for node in graph.nodes():

            net.add_node(

                node,

                label=node,

                color="#ff4d4d",

                shape="dot",

                size=20

            )

        # -----------------------------
        # Add Edges
        # -----------------------------

        for source, destination in graph.edges():

            net.add_edge(

                source,

                destination,

                color="#00bfff",

                arrows="to"

            )

        output_file = "static/graphs/enterprise_graph.html"

        net.save_graph(output_file)

        return output_file