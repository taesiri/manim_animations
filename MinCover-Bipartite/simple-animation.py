from manim import *
import networkx as nx


class MinimumSetCover(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        G, steps = self.create_data()

        # Create nodes
        nodes = []
        for node in G.nodes:
            if node < 7:  # left partition
                color = GREEN_E
                edge_color = GREY
            else:  # right partition
                color = BLUE_D
                edge_color = GREY

            circle = Circle(
                radius=0.3, color=edge_color, fill_color=color, fill_opacity=1.0
            )
            circle.move_to(self.node_position(node))
            nodes.append(circle)

        # Create edges
        edges = []
        for edge in G.edges:
            line = Line(
                self.node_position(edge[0]), self.node_position(edge[1]), color=BLACK
            )
            edges.append(line)

        self.add(*edges)
        self.add(*nodes)

        # Highlight nodes
        for i in range(len(steps)):
            new_node = steps[i]
            idx = list(G.nodes).index(new_node)
            self.play(nodes[idx].animate.set_color(YELLOW_D), run_time=1)

    def node_position(self, node):
        x = -2 if node < 7 else 2
        y = (node % 7) - 3
        return np.array([x, y, 0])

    def create_data(self):
        def min_set_cover(G, left_nodes, right_nodes):
            steps = []
            while right_nodes:
                max_node = max(
                    left_nodes,
                    key=lambda x: len(set(right_nodes) & set(G.neighbors(x))),
                )
                connected_nodes = set(G.neighbors(max_node)) & set(right_nodes)

                left_nodes.remove(max_node)
                right_nodes = [
                    node for node in right_nodes if node not in connected_nodes
                ]

                steps.append(max_node)

            return steps

        G = nx.Graph()
        left_nodes = list(range(7))
        right_nodes = list(range(7, 14))

        G.add_nodes_from(left_nodes, bipartite=0)
        G.add_nodes_from(right_nodes, bipartite=1)

        edges = [
            (0, 7),
            (0, 8),
            (1, 9),
            (2, 10),
            (2, 11),
            (3, 12),
            (4, 13),
            (5, 7),
            (6, 10),
        ]
        G.add_edges_from(edges)

        steps = min_set_cover(G, left_nodes, right_nodes)

        return G, steps
