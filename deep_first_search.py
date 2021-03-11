import pygame
from random import choice

RES = WIDTH, HEIGHT = 1202, 902
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw_current_cell(self):
        x = self.x * TILE
        y = self.y * TILE
        pygame.draw.rect(sc, pygame.Color('#f53b57'), (x + 2, y + 2, TILE - 2, TILE - 2))
    
    def draw(self):
        x = self.x * TILE
        y = self.y * TILE

        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#1e272e'), (x, y, TILE, TILE))
        
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#4bcffa'), (x, y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#4bcffa'), (x + TILE, y), (x + TILE, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#4bcffa'), (x + TILE, y + TILE), (x, y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#4bcffa'), (x, y + TILE), (x, y), 3)

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []

        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return choice(neighbors) if neighbors else False


def remove_walls(current, nex):
    dx = current.x - nex.x

    if dx == 1:
        current.walls['left'] = False
        nex.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        nex.walls['left'] = False

    dy = current.y - nex.y

    if dy == 1:
        current.walls['top'] = False
        nex.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        nex.walls['top'] = False

     

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []


while True:
    sc.fill(pygame.Color('#2d3436'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    next_cell = current_cell.check_neighbors()

    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    pygame.display.flip()
    clock.tick(30)