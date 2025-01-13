import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '0'

import numpy as np 
from typing import Literal


class Board:
    def __init__(self, size: int, peak: int, spawns: list[int], prob: list[float]):
        assert len(spawns)==len(prob), "Length of args `spawns` and `prob` must be equal"
        self._size = size
        self._peak = peak
        self._spawns = spawns
        self._prob = prob

        self.array = np.zeros((self._size, self._size), dtype=np.uint8)
        self.has_moved = False 
        self._spawn()
        self._spawn()
    
    @classmethod
    def fromstate(cls, array2d: np.ndarray[np.uint8], peak: int, spawns: list[int], prob: list[float]):
        size = len(array2d)
        for row in array2d:
            assert len(row)==size, "array2d must be square array"
        obj = cls(size, peak, spawns, prob)
        obj.array.setfield(array2d, dtype=np.uint8)
        return obj
    
    def size(self) -> int:
        return self._size
    
    def peak(self) -> int:
        return self._peak
    
    def dead_end(self):
        return self.array.all() and self.can_merge()==False

    def reset(self):
        self.array.fill(0)
        self._spawn()
        self._spawn()
    
    @staticmethod
    def is_equal(arr1: np.ndarray[np.uint8], arr2: np.ndarray[np.uint8]) -> bool:
        return (arr1==arr2).all()
    
    def can_merge(self):
        if not self.is_equal(self.left(self.array), self.array):
            return True
        if not self.is_equal(self.right(self.array), self.array):
            return True
        if not self.is_equal(self.up(self.array), self.array):
            return True
        if not self.is_equal(self.down(self.array), self.array):
            return True
        return False
    
    def finished(self):
        return self.array.max() == self._peak
    
    def _spawn(self):
        assert not self.array.all(), "No space to spawn a number on board!"
        data = 1
        while data!=0:
            r = np.random.randint(0, self._size)
            c = np.random.randint(0, self._size)
            data = self.array[r][c]
        self.array[r][c] = int(np.random.choice(self._spawns, 1, p=self._prob))
    
    def _merge(self, stack: list[int]) -> list[int]:
        new_stack = []
        last_data = 0
        for new_data in reversed(stack):
            if last_data==new_data and last_data!=0:
                new_stack.append(new_stack.pop()+1)
                last_data = 0
            else:
                new_stack.append(new_data)
                last_data = new_data

        self.has_moved += len(new_stack)<len(stack)
        new_stack += [0 for _ in range(self._size-len(new_stack))]
        return new_stack
    
    def push(self, to: Literal['u', 'd', 'l', 'r']):
        old_array = self.array.copy()
        match to:
            case 'd':
                self.array = self.down(self.array)
            case 'u':
                self.array = self.up(self.array)
            case 'r':
                self.array = self.right(self.array)
            case 'l':
                self.array = self.left(self.array)
            case _:
                return

        # to see any movement of data
        if not self.is_equal(self.array, old_array):
            self.has_moved = 0
            self._spawn()

        
    def left(self, arr: np.ndarray[np.uint8]) -> np.ndarray[np.uint8]:
        for r in range(self._size):
            stack = [arr[r][self._size-1-c] for c in range(self._size) if arr[r][self._size-1-c]!=0]
            for c, new_data in enumerate(self._merge(stack)):
                arr[r][c] = new_data
        return arr

    def right(self, arr: np.ndarray[np.uint8]) -> np.ndarray[np.uint8]:
        for r in range(self._size):
            stack = [arr[r][c] for c in range(self._size) if arr[r][c]!=0]
            for c, new_data in enumerate(self._merge(stack)):
                arr[r][self._size-1-c] = new_data
        return arr

    def up(self, arr: np.ndarray[np.uint8]) -> np.ndarray[np.uint8]:
        for c in range(self._size):
            stack = [arr[self._size-1-r][c] for r in range(self._size) if arr[self._size-1-r][c]!=0]
            for r, new_data in enumerate(self._merge(stack)):
                arr[r][c] = new_data
        return arr

    def down(self, arr: np.ndarray[np.uint8]) -> np.ndarray[np.uint8]:
        for c in range(self._size):
            stack = [arr[r][c] for r in range(self._size) if arr[r][c]!=0]
            for r, new_data in enumerate(self._merge(stack)):
                arr[self._size-1-r][c] = new_data
        return arr


import pygame
pygame.init()


WIDTH  = 410
HEIGHT = 410
FPS    = 60

TILE_SIZE = 75
TILE_PADDING = 10

BLACK  = (000, 000, 000)
WHITE  = (255, 255, 255)
RED    = (255, 000, 000)
GREEN  = (000, 255, 000)
BLUE   = (000, 000, 255)
YELLOW = (255, 255, 000)
CYAN   = (000, 255, 255)
PURPLE = (255, 000, 255)

WIN_COLOR   = (250, 248, 239)
BOARD_COLOR = (187, 173, 160)

# 0 -> dark, 1 -> light
TEXT_FG = (113, 101,  91), (255, 236, 239)

# color mapping for each number on tile: range(12)
TEXT_BG  =  (
    (205, 193, 180),
    (232, 229, 219),
    (234, 223, 200),
    (242, 176, 125),
    (237, 155, 103),
    (238, 127,  99),
    (242,  98,  67),
    (235, 208, 121),
    (240, 204, 107),
    (234, 199,  90),
    (228, 197,  87),
    (232, 190,  77),
)

# game state
GAMEPLAY = 0
GAMEWON  = 1
GAMEOVER = 2


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

FONT_FAMILY = 'calibri'
FONT_BOLD = pygame.font.SysFont(FONT_FAMILY, 30, True)
FONT_NORMAL = pygame.font.SysFont(FONT_FAMILY, 16)

# game data
board = Board(4, 11, (1, 2), (0.9, 0.1))
board_surf = pygame.Surface((TILE_SIZE*4 + TILE_PADDING*5, TILE_SIZE*4 + TILE_PADDING*5))
board_surf.fill(BOARD_COLOR)

def show_end(surf: pygame.Surface, msg: str):
    w, h = board_surf.get_width(), board_surf.get_height()

    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((237, 211, 132, 100))
    text = FONT_BOLD.render(msg, False, WHITE)

    surf.blit(overlay, (30, 30))
    surf.blit(text, text.get_rect(center=(WIDTH/2, HEIGHT/2)))


def draw_board(surf: pygame.Surface):
    global board, board_surf
    for r, row in enumerate(board.array):
        for c, data in enumerate(row):
            y = TILE_PADDING*(r+1) + TILE_SIZE*r
            x = TILE_PADDING*(c+1) + TILE_SIZE*c

            # bg
            pygame.draw.rect(board_surf, TEXT_BG[data], (x, y, TILE_SIZE, TILE_SIZE))
            
            # fg
            if data==0:
                continue
            elif data==1 or data==2:
                text = FONT_BOLD.render(f'{2**data}', False, TEXT_FG[0])
            else:
                text = FONT_BOLD.render(f'{2**data}', False, TEXT_FG[1])

            w, h = text.get_width(), text.get_height()
            board_surf.blit(text, text.get_rect(topleft=(x+(TILE_SIZE-w)/2, y+(TILE_SIZE-h)/2)))

    surf.blit(board_surf, (30, 30))
import random


# game init
assert board.peak()+1==len(TEXT_BG), "Not enough bg color defined for each possible value!"
state = GAMEPLAY
run = True

# mainloop
while run:
    pygame.time.Clock().tick(FPS)
    WIN.fill(WIN_COLOR)

    # board.push(random.choice(['u', 'd', 'l', 'r']))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN and state==GAMEPLAY:
            if event.key == pygame.K_UP:
                board.push('u')
            elif event.key == pygame.K_DOWN:
                board.push('d')
            elif event.key == pygame.K_LEFT:
                board.push('l')
            elif event.key == pygame.K_RIGHT:
                board.push('r')

    # game state
    if state == GAMEPLAY:
        if   board.finished():
            state = GAMEWON
        elif board.dead_end():
            state = GAMEOVER

    # rendering
    draw_board(WIN)

    if state!=GAMEPLAY:
        show_end(WIN, "You Win!" if state==GAMEWON else "You Lost!")


    pygame.display.update()

pygame.quit()
