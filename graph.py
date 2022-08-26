class Node:
    def __init__(self):
        self.neighbours = set()

    def add_neighbour(self, node, weight):
        self.neighbours.add((node, weight))

    # Priority queue lexiographically sorts, however
    # we don't want it to so we return false
    def __ge__(self, node):
        return False
    def __le__(self, node):
        return False
    def __gt__(self, node):
        return False
    def __lt__(self, node):
        return False

class Edge:
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.distances = {}
        self.visited = set()
        self.parents = {} # keeps track of where a node came from to print best path

    def add_edge(self, node1, node2, weight=1, bidirectional=True):
        if node1 not in self.nodes:
            node1.add_neighbour(node2, weight)
            self.nodes.append(node1)
        else:
            self.nodes[self.nodes.index(node1)].add_neighbour(node2, weight)
        if bidirectional:
            if node2 not in self.nodes:
                node2.add_neighbour(node1, weight)
                self.nodes.append(node2)
            else:
                self.nodes[self.nodes.index(node2)].add_neighbour(node1, weight)
        self.edges.append(Edge(node1, node2, weight))

    def visited_node(self, node):
        self.visited.add(node)

    def set_distances(self, dist):
        for node in self.nodes:
            self.distances[node] = dist

    def reset(self):
        self.visited.clear()
        self.distances.clear()
        self.parents.clear()

    def update_distance(self, node, new_distance):
        self.distances[node] = new_distance

    def get_distance(self, node):
        # returns -1 if we cannot get to node from the start node
        return -1 if node not in self.distances else self.distances[node]

    def get_parent(self, node):
        return -1 if node not in self.parents else self.parents[node]

    def get_path(self, node):
        # returns path
        nodes = []
        if self.get_parent(node) == -1:
            return []
        nodes.append(node)
        while self.get_parent(node) != node:
            node = self.get_parent(node)
            nodes.append(node)
        return list(reversed(nodes))
