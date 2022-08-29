from math import inf
from queue import PriorityQueue
from graph import Node, Graph

from utils import find_by_key

class PathfindingAlgorithm():
    @staticmethod
    def run(graph, start, end, node_map, callback, skip_node_clause):
        assert isinstance(graph, Graph)
        assert isinstance(start, Node)
        assert isinstance(end, Node)
        assert isinstance(node_map, dict)
        assert callable(callback)
        assert callable(skip_node_clause)
        graph.reset()

class Dijkstra(PathfindingAlgorithm):
    @staticmethod
    def run(graph, start, end, node_map={}, callback=lambda node: None,
            skip_node_clause=lambda node: None):
        super(Dijkstra, Dijkstra).run(graph, start, end, node_map, callback,
                                      skip_node_clause)

        pq = PriorityQueue()
        graph.set_distances(inf)
        graph.distances[start] = 0
        graph.parents[start] = start

        pq.put([0, start]) # [distance, node]
        while not pq.empty():
            _, node = pq.get()
            if node == end:
                break
            if skip_node_clause(node) or node in graph.visited:
                continue
            graph.visited_node(node)
            callback(node)
            for neighbour, weight in node.neighbours:
                if graph.distances[neighbour] > graph.distances[node] + weight:
                    graph.update_distance(neighbour,
                                          graph.distances[node] + weight)
                    graph.parents[neighbour] = node
                    pq.put([graph.distances[neighbour], neighbour])

class A_star(PathfindingAlgorithm):
    @staticmethod
    def run(graph, start, end, node_map, callback=lambda node: None,
            skip_node_clause=lambda node: None):
        super(A_star, A_star).run(graph, start, end, node_map, callback,
                                  skip_node_clause)

        # heuristic function, uses manhattan distance relative to end node (i.e. our goal)
        def h(node):
            node_x, node_y = find_by_key(node_map, node)
            end_x, end_y = find_by_key(node_map, end)
            return abs(node_x - end_x) + abs(node_y - end_y)

        # NOTE: distances[x] = g(x)
        pq = PriorityQueue()
        graph.set_distances(inf)
        graph.distances[start] = 0
        graph.parents[start] = start

        # NOTE: f(x) = g(x) + h(x)
        f = {}
        for node in graph.nodes:
            f[node] = inf
        f[start] = graph.distances[start] + h(start)

        pq.put([f[start], start])
        while not pq.empty():
            _, node = pq.get()
            if node == end:
                break
            if skip_node_clause(node) or node in graph.visited:
                continue
            graph.visited_node(node)
            callback(node)
            for neighbour, weight in node.neighbours:
                if graph.distances[node] + weight < graph.distances[neighbour]:
                    graph.parents[neighbour] = node
                    graph.update_distance(neighbour,
                                          graph.distances[node] + weight)
                    f[neighbour] = graph.distances[neighbour] + h(neighbour)
                    pq.put([f[neighbour], neighbour])
