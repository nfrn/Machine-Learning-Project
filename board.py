class Edge:
    def __init__(self, origin, direction):
        """
        Create Edge

        :param origin:  The starting node for this edge
        :param direction:     Direction 'h' for horizontal, 'v' for vertical
        """
        self.origin = origin
        self.dir = direction
        self.destination = self.get_des()

    def __eq__(self, other):
        return self.origin == other.origin and self.dir == other.dir

    def __str__(self):
        return "[" + str(self.origin) + ", " + str(self.dir) + "]"

    def __hash__(self):
        return hash(self.origin) + hash(self.dir)

    def get_org(self): return self.origin

    def set_org(self, org): self.origin = org

    def get_dir(self): return self.dir

    def get_nodes(self): return self.origin, self.destination

    def get_des(self):
        if self.dir == 'h':
            return self.get_org().hnext()
        else:
            return self.get_org().vnext()


class Node:
    def __init__(self, x, y):
        """
        Create node

        :param x:   The x coordinate of this node on the board.
        :param y:   The y coordinate of this node on the board.
        """
        self.pos = (x, y)

    def __eq__(self, other):
        return self.pos == other.pos

    def __gt__(self, other):
        return self.pos > other.pos

    def __add__(self, other):
        return Node(self.get_pos()[0] + other.get_pos()[0],
                    self.get_pos()[1] + other.get_pos()[1])

    def __sub__(self, other):
        return Node(self.get_pos()[0] - other.get_pos()[0],
                    self.get_pos()[1] - other.get_pos()[1])

    def __hash__(self):
        return hash(self.pos)

    def __str__(self):
        return str(self.get_pos())

    def hnext(self):
        return Node(self.get_pos()[0], self.get_pos()[1] + 1)

    def vnext(self):
        return Node(self.get_pos()[0] + 1, self.get_pos()[1])

    def next(self, direction):
        if direction == 'h':
            return self.hnext()
        else:
            return self.vnext()

    def get_pos(self):
        return self.pos


class Chain:
    def __init__(self, edge):
        """
        Create Chain

        :param edge:    The first edge of this chain
        """
        self.origin = edge.get_org()
        self.edges = set()
        self.nodes = set()

        self.add_edge(edge)

    def __gt__(self, other):
        return self.origin > other.origin

    def __str__(self):
        edges = ""
        for i in self.get_edges():
            edges += str(i) + " "
        nodes = ""
        for i in self.get_nodes():
            nodes += str(i) + " "

        return "Origin: " + str(self.get_org()) + \
               "\nEdges:  " + edges + "\nNodes:  " + nodes

    def __eq__(self, other):
        return self.get_nodes() == other.get_nodes() and \
               self.get_edges() == other.get_edges()

    def __hash__(self):
        return hash(self.get_org())

    def get_org(self): return self.origin

    def set_org(self, org): self.origin = org

    def get_edges(self): return self.edges

    def set_edges(self, edges): self.edges = edges

    def get_nodes(self): return self.nodes

    def set_nodes(self, nodes): self.nodes = nodes

    def add_node(self, node): self.get_nodes().add(node)

    def update_nodes(self):
        nodes = set()
        for i in self.get_edges():
            nodes.add(i.get_org())
            nodes.add(i.get_des())

        self.nodes = nodes

    def add_edge(self, edge):
        if edge.get_org() < self.get_org():
            self.update_chain(self.get_org() - edge.get_org())
            self.set_org(edge.get_org())

        self.add_rel_edge(edge)

    def add_rel_edge(self, edge):
        rel_org = edge.get_org() - self.get_org()
        rel_des = edge.get_des() - self.get_org()
        self.get_edges().add(Edge(rel_org, edge.get_dir()))
        self.get_nodes().add(rel_org)
        self.get_nodes().add(rel_des)

    def update_chain(self, update):
        # TODO search for how to do map, filter, reduce in python 3.x
        # self.edges = map(lambda x: x + update, self.edges)
        # self.nodes = map(lambda x: x + update, self.nodes)
        edges = set()
        for i in self.get_edges():
            i.set_org(i.get_org() + update)
            edges.add(i)

        self.set_edges(edges)
        self.update_nodes()

    def merge(self, other):
        higher = min(self, other)
        lower = max(self, other)
        high_org = higher.get_org()
        low_org = lower.get_org()

        lower.update_chain(low_org - high_org)

        self.set_org(high_org)
        self.set_edges(self.get_edges().union(other.get_edges()))
        self.set_nodes(self.get_nodes().union(other.get_nodes()))
        return self


# TODO implement symmetries: mirrors, rotations -> standard representation
# TODO make equals function quicker?
class Board:
    def __init__(self, rows, columns, chains):
        """
        Create Board

        :param rows:    The number of rows of nodes in the board
        :param columns: The number of columns of nodes in the board
        :param chains:  A list containing the boards chains
        :param player:  0 -> player1, 1 -> player2
        """
        self.rows = rows
        self.columns = columns
        self.chains = chains
        self.free_edges = self.init_free_edges()
        self.player = 0
        self.last_move = 0

    def __eq__(self, other):
        return self.rows == other.rows and self.columns == other.columns \
               and self.get_chains() == other.get_chains()

    def get_rows(self): return self.rows

    def get_columns(self): return self.columns

    def get_chains(self): return self.chains

    def get_player(self): return self.player

    def get_free_edges(self): return self.free_edges

    def get_last_move(self):
        return self.last_move

    def get_number_free_edges(self):
        return len(self.free_edges)

    def init_free_edges(self):
        free_edges = set()
        for i in range(self.rows+1):
            for j in range(self.columns+1):
                if i == self.rows and j < self.columns:
                    free_edges.add(Edge(Node(i, j), 'h'))
                elif j == self.columns and i < self.rows:
                    free_edges.add(Edge(Node(i, j), 'v'))
                elif j != self.columns or i != self.rows:
                    free_edges.add(Edge(Node(i, j), 'v'))
                    free_edges.add(Edge(Node(i, j), 'h'))
        return free_edges

    def add_edge(self, edge):
        self.last_move = edge
        if edge in self.get_free_edges():
            self.get_free_edges().remove(edge)
            chains = self.find_neighbouring_chains(edge)

            if len(chains) == 0:
                self.chains.add(Chain(edge))
            elif len(chains) == 1:
                self.add_edge_to_chain(edge, chains[0])
            else:
                self.merge_chains(chains[0], chains[1])

        self.player = ((self.player + 1) % 2)

    def add_edge_to_chain(self,edge, chain):
        # TODO there is probably a more efficient way to do this.
        self.get_chains().remove(chain)
        chain.add_edge(edge)
        self.get_chains().add(chain)

    def merge_chains(self, chain1, chain2):
        self.get_chains().remove(chain1)
        self.get_chains().remove(chain2)
        self.chains.add(chain1.merge(chain2))

    def find_neighbouring_chains(self, edge):
        found_chains = []
        org, des = edge.get_nodes()

        for chain in self.get_chains():
            if org - chain.get_org() in chain.get_nodes() or\
               des - chain.get_org() in chain.get_nodes():
                found_chains.append(chain)

            if len(found_chains) == 2:
                break

        return found_chains

    def is_finished(self):
        return len(self.free_edges)


