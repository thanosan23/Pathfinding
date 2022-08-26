import sys
from enum import Enum
import pygame

from graph import Node, Graph
from pathfinding import Dijkstra

# Constants
FPS = 60
DIM = 30
CELL_SIZE = 20

# Setup
pos_to_renderpos = lambda x: x * CELL_SIZE

pygame.init()
pygame.display.set_caption("Pathfinding")
screen = pygame.display.set_mode((pos_to_renderpos(DIM),
                                  pos_to_renderpos(DIM)))
clock = pygame.time.Clock()

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

class Box:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
    def draw(self):
        pygame.draw.rect(screen,
                         self.colour,
                         (self.x*CELL_SIZE, self.y*CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))

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
graph, node_map = generate_graph()

while True:
    # clear screen
    screen.fill(Colour.WHITE.value)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        # get mouse press
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            x, y = get_mousepos()
            GRID[(x, y)].colour = Colour.GRAY.value
        elif right:
            x, y = get_mousepos()
            GRID[(x, y)].colour = Colour.WHITE.value
        # get keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                GRID = create_grid()

    # draw grid & gridlines
    draw_grid(GRID)
    draw_gridlines()

    pygame.display.update()
    clock.tick(FPS)
