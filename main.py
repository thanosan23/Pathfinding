import sys
from enum import Enum
from functools import partial
import pygame

from graph import Node, Graph
from pathfinding import Dijkstra, A_star
from utils import find_by_key, lerp
from ui import HUD, Button, Text

# Constants
FPS = 60
DIM = 30
CELL_SIZE = 20
ALGORITHM = None

# Setup
pos_to_renderpos = lambda x: x * CELL_SIZE

pygame.init()
pygame.display.set_caption("Pathfinding")
screen = pygame.display.set_mode((pos_to_renderpos(DIM),
                                  pos_to_renderpos(DIM)+100))
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

# Utilities
class Colour(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (142, 142, 142)

    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 128)

hud = HUD(0, pos_to_renderpos(DIM), pos_to_renderpos(DIM), 100)
hud.add_element("Dijkstra", Button, Colour.RED.value, (font, "Dijkstra"))
hud.add_element("A star", Button, Colour.BLUE.value, (font, "A star"))
hud.add_element("Path length", Text, Colour.BLACK.value, (font, "Path length: Unknown"))

class Box:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

        self.start = False
        self.end = False
        self.obstacle = False
        self.vis = False

    def make_start(self):
        self.start = True
        self.colour = Colour.RED.value

    def make_end(self):
        self.end = True
        self.colour = Colour.BLUE.value

    def make_obstacle(self):
        self.obstacle = True
        self.colour = Colour.GRAY.value

    def clear(self):
        self.start = False
        self.end = False
        self.obstacle = False
        self.vis = False
        self.colour = Colour.WHITE.value

    def draw(self):
        pygame.draw.rect(screen,
                         self.colour,
                         (self.x*CELL_SIZE, self.y*CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))

class DrawMode(Enum):
    START = 0
    END = 1
    OBSTACLE = 2

def get_mousepos():
    x, y = pygame.mouse.get_pos()
    return x//CELL_SIZE, y//CELL_SIZE


def draw_gridlines():
    for x in range(0, DIM):
        pygame.draw.line(screen,
                         Colour.BLACK.value,
                         (0, x * CELL_SIZE),
                         (pos_to_renderpos(DIM), x * CELL_SIZE))
    for y in range(0, DIM):
        pygame.draw.line(screen,
                         Colour.BLACK.value,
                         (y * CELL_SIZE, 0),
                         (y * CELL_SIZE, pos_to_renderpos(DIM)))

def create_grid():
    grid = {}
    for x in range(0, DIM):
        for y in range(0, DIM):
            grid[(x, y)] = Box(x, y, Colour.WHITE.value)
    return grid

def draw_grid(grid):
    for x in range(0, DIM):
        for y in range(0, DIM):
            grid[(x, y)].draw()

DELTA_X = [1, -1, 0, 0]
DELTA_Y = [0, 0, 1, -1]

def neighbours(x, y):
    # returns all valid neighbours for a node
    ret = []
    for dx, dy in zip(DELTA_X, DELTA_Y):
        if x + dx >= 0 and x + dx < DIM and y + dy >= 0 and y + dy < DIM:
            ret.append((x+dx, y+dy))
    return ret

def generate_graph():
    graph = Graph()
    nodes_map = {}
    # create nodes
    for y in range(DIM):
        for x in range(DIM):
            node = Node()
            nodes_map[(x, y)] = node
    # create edges
    for y in range(DIM):
        for x in range(DIM):
            for nx, ny in neighbours(x, y):
                graph.add_edge(nodes_map[(x, y)], nodes_map[(nx, ny)])
    return graph, nodes_map

# main
GRID = create_grid()
mode = DrawMode.OBSTACLE

# for tracing paths
path = None
visiting = None

visited = False
running = False

# for algorithm
graph, node_map = generate_graph()
start_node = None
end_node = None

def run_algorithm():
    if ALGORITHM is not None:
        path = None
        visiting = None

        visited = False
        running = False

        if end_node is not None and start_node is not None:
            start = node_map[start_node]
            end = node_map[end_node]
            visits = []

            def callback(current_node, start, end, visits):
                if current_node not in (start, end):
                    x, y = find_by_key(node_map, current_node)
                    visits.append((x, y))

            def skip_node_clause(current_node):
                # skip if current node is an obstacle
                x, y = find_by_key(node_map, current_node)
                return GRID[(x, y)].obstacle

            ALGORITHM.run(graph, start, end, node_map,
                          partial(callback, start=start, end=end, visits=visits),
                          skip_node_clause)
            path = iter(graph.get_path(end))
            visiting = iter(visits)
            running = True
    return path, visiting, visited, running

while True:
    # clear screen
    screen.fill(Colour.WHITE.value)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if not running:
            # get mouse press
            left, _, right = pygame.mouse.get_pressed()
            if left:
                hud.elements_dict["Path length"].update_text(f"Path length: Unknown")
                x, y = get_mousepos()
                if x < DIM and y < DIM:
                    if GRID[(x, y)].obstacle or GRID[(x, y)].start or GRID[(x, y)].end:
                        continue
                    if mode == DrawMode.OBSTACLE:
                        GRID[(x, y)].make_obstacle()
                    elif mode == DrawMode.START:
                        GRID[(x, y)].make_start()
                        start_node = (x, y)
                    elif mode == DrawMode.END:
                        GRID[(x, y)].make_end()
                        end_node = (x, y)
                    mode = DrawMode.OBSTACLE
                for element in hud.elements:
                    if element.clickable is True:
                        if element.clicked(*pygame.mouse.get_pos()):
                            if (
                                    ALGORITHM is not None and
                                    start_node is not None and
                                    end_node is not None
                                ):
                                for x in range(0, DIM):
                                    for y in range(0, DIM):
                                        if GRID[(x, y)].vis:
                                            GRID[(x, y)].clear()
                            if element.name == "Dijkstra":
                                ALGORITHM = Dijkstra
                            elif element.name == "A star":
                                ALGORITHM = A_star
                            else:
                                ALGORITHM = None
                            path, visiting, visited, running = run_algorithm()
                            if start_node is not None and end_node is not None:
                                dist = graph.get_distance(node_map[end_node])
                                hud.elements_dict["Path length"].update_text(f"Path length: {dist}")

            elif right:
                hud.elements_dict["Path length"].update_text(f"Path length: Unknown")
                x, y = get_mousepos()
                if x < DIM and y < DIM:
                    GRID[(x, y)].clear()
                    if start_node == (x, y):
                        start_node = None
                    elif end_node == (x, y):
                        end_node = None
            # get keyboard press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    hud.elements_dict["Path length"].update_text(f"Path length: Unknown")
                    GRID = create_grid()
                    start_node = None
                    end_node = None
                if event.key == pygame.K_s:
                    hud.elements_dict["Path length"].update_text(f"Path length: Unknown")
                    if start_node is None:
                        if mode != DrawMode.START:
                            mode = DrawMode.START
                        else:
                            mode = DrawMode.OBSTACLE
                if event.key == pygame.K_e:
                    hud.elements_dict["Path length"].update_text(f"Path length: Unknown")
                    if end_node is None:
                        if mode != DrawMode.END:
                            mode = DrawMode.END
                        else:
                            mode = DrawMode.OBSTACLE
    mouse_on_button = False
    for element in hud.elements:
        if element.clickable:
            if element.clicked(*pygame.mouse.get_pos()):
                element.transparency = lerp(255, 100, 0.3)
                mouse_on_button = True
            else:
                if element.transparency != 255:
                    element.transparency = lerp(element.transparency, 255, 0.3)

    if mouse_on_button:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # draw grid & gridlines (replay algorithm)
    if running:
        if visiting is not None:
            coordinate = next(visiting, None)
            if coordinate is None:
                visiting = None
                visited = True
            else:
                GRID[coordinate].colour = Colour.GREEN.value
                GRID[coordinate].vis = True
        if visited:
            if path is not None:
                node = next(path, None)
                if node is None:
                    path = None
                    visited = False
                    running = False
                else:
                    if node not in (node_map[start_node], node_map[end_node]):
                        x, y = find_by_key(node_map, node)
                        GRID[(x, y)].colour = Colour.PURPLE.value
                        GRID[(x, y)].vis = True
    draw_grid(GRID)
    draw_gridlines()
    hud.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
