from math import inf
from queue import PriorityQueue
from graph import Node, Graph

class PathfindingAlgorithm():
    @staticmethod
    def run(graph, start, end, callback):
        assert isinstance(graph, Graph)
        assert isinstance(start, Node)
        assert isinstance(end, Node)
        assert callable(callback)
        graph.reset()

class Dijkstra(PathfindingAlgorithm):
    @staticmethod
    def run(graph, start, end, callback):
        super(Dijkstra, Dijkstra).run(graph, start, end, callback)

        pq = PriorityQueue()
        graph.set_distances(inf)
        graph.distances[start] = 0
        graph.parents[start] = start

        pq.put([0, start]) # [distance, node]
        while not pq.empty():
            _, node = pq.get()
            if node in graph.visited:
                continue
            if node == end:
                break
            graph.visited_node(node)
            callback(node)
            for neighbour, weight in node.neighbours:
                if graph.distances[neighbour] > graph.distances[node] + weight:
                    graph.update_distance(neighbour,
                                          graph.distances[node] + weight)
                    graph.parents[neighbour] = node
                    pq.put([graph.distances[neighbour], neighbour])
