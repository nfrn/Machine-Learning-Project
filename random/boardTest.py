from board import *


def test_edge():
    edge = Edge(Node(4, 5), 'h')
    assert edge.get_nodes() == (edge.get_org(), edge.get_des())
    assert edge.dir == 'h'
    assert edge.get_des() == Node(4, 6)

    edge = Edge(Node(15, 7), 'v')
    assert edge.get_nodes() == (edge.get_org(), edge.get_des())
    assert edge.get_dir() == 'v'
    assert edge.get_des() == Node(16, 7)
    assert str(edge) == "[(15, 7), v]"

    print("Edge successfully tested")


def test_node():
    node1 = Node(4, 4)
    node2 = Node(4, 5)
    node3 = Node(5, 4)
    node4 = Node(5, 5)
    node5 = Node(4, 4)

    assert node1 < node2
    assert node1 < node3
    assert node1 < node4
    assert node1 == node5
    assert node1.hnext() == node2
    assert node1.vnext() == node3
    assert node1 + node2 == Node(8, 9)
    assert node3 - node1 == Node(1, 0)

    node1 += node2
    assert node1 == Node(8, 9)

    assert str(node1) == "(8, 9)"

    print("Node successfully tested")


def test_chain():
    chain = Chain(Edge(Node(4, 5), 'h'))

    assert chain.get_org() == Node(4, 5)
    assert Edge(Node(0, 0), 'h') in chain.get_edges()
    assert Node(0, 1) in chain.get_nodes()

    chain.add_edge(Edge(Node(3, 5), 'v'))
    chain2 = Chain(Edge(Node(2, 4), 'v'))
    chain2.add_edge(Edge(Node(2, 4), 'h'))
    chain2.add_edge(Edge(Node(2, 5), 'v'))
    chain.merge(chain2)

    assert chain.get_org() == Node(2, 4)
    assert chain2.get_org() == Node(2, 4)
    assert chain.get_org() == chain2.get_org()

    assert Edge(Node(0, 0), 'h') in chain.edges
    assert Edge(Node(0, 0), 'v') in chain.edges
    assert Edge(Node(0, 1), 'v') in chain.edges
    assert Edge(Node(1, 1), 'v') in chain.edges
    assert Edge(Node(2, 1), 'h') in chain.edges

    assert Node(0, 0) in chain.nodes
    assert Node(0, 1) in chain.nodes
    assert Node(1, 1) in chain.nodes
    assert Node(2, 1) in chain.nodes
    assert Node(2, 2) in chain.nodes

    print("Chain successfully tested")


def test_board():
    b = Board(8, 8, set())

    assert Edge(Node(4, 5), 'h') in b.get_free_edges()
    assert Edge(Node(8, 8), 'h') not in b.get_free_edges()
    assert Edge(Node(8, 8), 'v') not in b.get_free_edges()
    assert Edge(Node(3, 8), 'h') not in b.get_free_edges()
    assert Edge(Node(8, 7), 'v') not in b.get_free_edges()

    b.add_edge(Edge(Node(4, 5), 'h'))
    assert Edge(Node(4, 5), 'h') not in b.get_free_edges()
    assert Chain(Edge(Node(4, 5), 'h')) in b.get_chains()

    b.add_edge(Edge(Node(3, 5), 'v'))
    b.add_edge(Edge(Node(2, 4), 'v'))
    b.add_edge(Edge(Node(2, 4), 'h'))

    assert len(b.get_chains()) == 2

    b.add_edge(Edge(Node(2, 5), 'v'))

    assert len(b.get_chains()) == 1

    print("Board successfully tested")


if __name__ == "__main__":
    test_edge()
    test_node()
    test_chain()
    test_board()
    print("Tests successfully completed")
