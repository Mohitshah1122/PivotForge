import networkx as nx

from modules.graph_engine import GraphEngine


class AttackPathEngine:

    def __init__(self):

        self.graph_engine = GraphEngine()

    # ==========================================
    # Refresh Graph
    # ==========================================

    def refresh(self):

        self.graph_engine.build_graph()

    # ==========================================
    # Assets
    # ==========================================

    def get_assets(self):

        self.refresh()

        return self.graph_engine.node_list()

    # ==========================================
    # BFS
    # ==========================================

    def bfs_path(self, source, destination):

        self.refresh()

        graph = self.graph_engine.get_graph()

        try:

            return nx.shortest_path(graph, source, destination)

        except:

            return []

    # ==========================================
    # DFS
    # ==========================================

    def dfs_path(self, source, destination):

        self.refresh()

        graph = self.graph_engine.get_graph()

        try:

            path = list(nx.dfs_preorder_nodes(graph, source))

            if destination not in path:
                return []

            result = []

            for node in path:

                result.append(node)

                if node == destination:
                    break

            return result

        except:

            return []

    # ==========================================
    # Dijkstra
    # ==========================================

    def dijkstra_path(self, source, destination):

        self.refresh()

        graph = self.graph_engine.get_graph()

        try:

            for edge in graph.edges():

                graph[edge[0]][edge[1]]["weight"] = 1

            return nx.dijkstra_path(

                graph,

                source,

                destination,

                weight="weight"

            )

        except:

            return []

    # ==========================================
    # Graph Statistics
    # ==========================================

    def total_nodes(self):

        self.refresh()

        return self.graph_engine.total_nodes()

    def total_edges(self):

        self.refresh()

        return self.graph_engine.total_edges()