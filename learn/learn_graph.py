"""
file_name: learn_graph.py
create_date: 2022-05-29
purpose: learn about graph and its relationship between networkx

Comments: now only involve undirected graph, i do think manim can incorporate more types of graphs 
"""
from manim import *
import networkx as nx

# The simplist scene: setting up the graph, and moving the vertices, the edges would be updated accordingly
class MovingVertices(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)]
        g = Graph(vertices, edges)
        self.play(Create(g))
        self.wait()
        self.play(
            g[1].animate.move_to([1, 1, 0]),
            g[2].animate.move_to([-1, 1, 0]),
            g[3].animate.move_to([1, -1, 0]),
            g[4].animate.move_to([-1, -1, 0])
        )
        self.wait()

# Displaying different kinds of layout
class GraphLayout(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                 (2, 8), (3, 4), (6, 1), (6, 2),
                 (6, 3), (7, 2), (7, 4)]
        autolayouts = ["spring", "circular", "kamada_kawai", "planar", "random", 
                    "shell", "spectral", "spiral"]
        
        graphs = [
            Graph(vertices, edges, layout = lt).scale(0.5)
            for lt in autolayouts
        ]

        # actually we can use arrange_in_grid function i guess?
        graphs = VGroup(*graphs).arrange_in_grid(rows = 3)
        self.add(graphs)
        """
        r1 = VGroup(*graphs[:3]).arrange()
        r2 = VGroup(*graphs[3:6]).arrange()
        r3 = VGroup(*graphs[6:]).arrange()
        self.add(VGroup(r1, r2, r3).arrange(direction = DOWN))
        """

# Displaying different layouts by transformations
class GraphMoveLayout(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                 (2, 8), (3, 4), (6, 1), (6, 2),
                 (6, 3), (7, 2), (7, 4)]
        autolayouts = ["spring", "circular", "kamada_kawai", "planar", "random", 
                    "shell", "spectral", "spiral"]
        colors = [RED, GOLD, ORANGE, PINK, YELLOW, GREEN, BLUE, PURPLE]

        graphs = [
            Graph(vertices, edges, layout = ly, labels = True, vertex_config = {i : {"fill_color": col} for i in range(1, 9)})
            for ly, col in zip(autolayouts, colors)
        ]

        self.play(Create(graphs[0]))
        self.wait()
        for i in range(1, len(graphs)):
            self.play(ReplacementTransform(graphs[i - 1], graphs[i]))
            self.wait()
        self.wait(2)

# We can manually decide the position of nodes by creaing a dictionary
class GraphManualPosition(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
        lt = {1: [0, 0, 0], 2: [1, 1, 0], 3: [1, -1, 0], 4: [-1, 0, 0]} # manual layout
        G = Graph(vertices, edges, layout = lt)
        self.add(G)

# we can give individual config on vertex and edge such as color
class LabeledModifiedGraph(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                 (2, 8), (3, 4), (6, 1), (6, 2),
                 (6, 3), (7, 2), (7, 4)]
        g = Graph(
            vertices, edges, 
            layout = "circular",
            layout_scale = 3,
            labels = True,
            vertex_config = {7: {"fill_color": RED}},
            edge_config = {
                (1, 7) : {"stroke_color" : RED},
                (2, 7) : {"stroke_color" : RED},
                (4, 7) : {"stroke_color" : RED},
            }
        )
        self.add(g)

class PartiteGraph(Scene):
    def construct(self):
        G = nx.Graph() # null graph
        G.add_nodes_from([0, 1, 2, 3])
        G.add_edges_from([(0,2), (0,3), (1,2)])

        print(G.nodes)
        print(G.edges)

        # actually directly sub list into the parameters is already ok ..

        graph = Graph(
            list(G.nodes),
            list(G.edges),
            layout = "partite",
            partitions = [[0, 1]]
        )
        self.add(graph)

class Tree(Scene):
    def construct(self):
        G = nx.Graph()
        # make use of networkx
        G.add_node("ROOT")

        for i in range(5):
            G.add_node("Child_%i"  % i)
            G.add_node("Grandchild_%i" % i)
            G.add_node("Greatgrandchild_%i" % i)

            G.add_edge("ROOT", "Child_%i" % i)
            G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
            G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)
        
        self.play(
            Create(
                Graph(
                    list(G.nodes),
                    list(G.edges),
                    layout = "tree",
                    root_vertex = "ROOT"
                )
            )
        )

# make wheel?
class LargeTreeGeneration(MovingCameraScene):
    DEPTH = 4
    CHILDREN_PER_VERTEX = 3
    LAYOUT_CONFIG = {"vertex_spacing" : (0.5, 1)}
    VERTEX_CONF = {"radius" : 0.25, "color": BLUE_B, "fill_opacity": 1}

    def expand_vertex(self, g, vertex_id : str, depth : int): # build the tree recursively
        new_vertices = [f"{vertex_id}/{i}" for i in range(self.CHILDREN_PER_VERTEX)]
        new_edges = [(vertex_id, child_id) for child_id in new_vertices]
        g.add_edges(
            *new_edges,
            vertex_config = self.VERTEX_CONF,
            positions = {
                k : g.vertices[vertex_id].get_center() + 0.1 * DOWN for k in new_vertices
            },
        )
        if depth < self.DEPTH: 
            for child_id in new_vertices:
                self.expand_vertex(g, child_id, depth + 1) # recursion
        return g
    
    def construct(self):
        g = Graph(["ROOT"], [], vertex_config = self.VERTEX_CONF)
        g = self.expand_vertex(g, "ROOT", 2)
        self.add(g)
        
        self.play(
            g.animate.change_layout(
                "tree",
                root_vertex = "ROOT",
                layout_config = self.LAYOUT_CONFIG,
            )
        )
        self.play(self.camera.auto_zoom(g, margin = 1), run_time = 0.5)

class ImportNetworkxGraph(Scene):
    def construct(self):
        nxgraph = nx.erdos_renyi_graph(14, 0.5)
        G = Graph.from_networkx(nxgraph, layout = "spring", layout_scale = 3.5)
        self.play(Create(G))
        self.play(
            *[
                G[v].animate.move_to(5 * RIGHT * np.cos(ind / 7 * PI) + 3 * UP * np.sin(ind / 7 * PI))
                for ind, v in enumerate(G.vertices)
            ]
        )
        self.play(Uncreate(G))

# Today's hw

class AddVerticesAnimation(Scene):
    def construct(self):
        G = nx.random_tree(n = 10, seed = 1)
        graph = Graph(
            list(G.nodes),
            list(G.edges),
            layout = "tree",
            root_vertex = 1
        )
        print(G.nodes)
        print(G.edges)

        self.add(graph)

        #graph.add_vertices(12, positions = {12: graph.vertices[1].get_center() + 3 * RIGHT + DOWN})
        #graph.add_edges((1, 12))
        #graph.change_layout(layout = "tree")
        pos_graph = graph.copy()
        pos_graph.add_vertices(12)
        pos_graph.add_edges((1, 12))
        pos_graph.change_layout(layout = "tree", root_vertex = 1)
        #graph.vertices[1].get_center() + 3 * RIGHT + DOWN
        self.play(
            graph.animate.add_vertices(12, positions = {12: pos_graph[12]}),
            # graph.animate.change_layout(
            #    "tree",
            #    root_vertex = 1
            #)
        )
        self.play(
            graph.animate.add_edges((1, 12))
        )
        self.wait()
        self.play(
            graph.animate.remove_edges((1,4))
        )
        """
        self.play(
            graph._add_vertices_animation(12, positions = graph.vertices[0].center() + 1 * RIGHT),
            #graph._add_edges_animation((1, 12))
        )
        
        graph.generate_target()
        
        graph.target.add_vertices(12)
        graph.target.add_edges((1, 12))
        self.play(
            MoveToTarget(graph)
        )
        """
        

# pass in: Graph (tree), vertice_trasversal_color, edge_trasversal_color
# out: animation
class DFS_Tree_Scene(Scene):   
    def dfs(self, vertex):
        print(f"Vertex {vertex}")
        self.animation.append(
            self.graph.vertices[vertex].animate.set_color(self.vertice_trasversal_color)
        )
        if not vertex in nx.dfs_successors(self.G, source = 1):
            return
        for v in nx.dfs_successors(self.G, source = 1)[vertex]:
            if (v, vertex) in self.graph.edges:
                edge = self.graph.edges[(v, vertex)]
            else:
                edge = self.graph.edges[(vertex, v)]

            self.animation.append(
                edge.animate.set_color(ORANGE)
            )
            self.dfs(v)

    def construct(self):
        N = 35
        self.vis = np.full((N + 1,0), False)
        self.G = nx.random_tree(n = N, seed = 1)
        print(nx.dfs_successors(self.G, source = 1))
        self.vertice_trasversal_color = RED
        self.edge_trasversal_color = ORANGE
        root_vertex = 1
        self.graph = Graph(
            list(self.G.nodes),
            list(self.G.edges),
            layout = "tree",
            root_vertex = root_vertex,
            layout_scale = 3
        )
        self.animation = []

        self.play(Create(
            self.graph
        ))
        self.wait()
        self.dfs(root_vertex)
        self.play(Succession(*self.animation))

# hw problem
# maybe consider constructing a class called Neural Network (inherited from Graph)
class NeuralNetwork(Graph):
    def __init__():
        pass

class ForwardPropagation(Scene):
    def construct(self):
        pass

class BackwardPropagation(Scene):
    def construct(self):
        pass