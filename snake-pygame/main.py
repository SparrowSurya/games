from collections import deque
from itertools import islice
import random
import pygame


pygame.mixer.init()
pygame.init()

BIT = 32
ROWS = 16
COLS = 20
OFFSET_X = 60
OFFSET_Y = 60
WIDTH  = OFFSET_X*2 + BIT*COLS
HEIGHT = OFFSET_Y*2 + BIT*ROWS
FPS    = 30

BLACK  = (000, 000, 000)
GREY   = (128, 128, 128)
WHITE  = (255, 255, 255)
RED    = (255, 000, 000)
GREEN  = (000, 255, 000)
BLUE   = (000, 000, 255)
YELLOW = (255, 255, 000)
CYAN   = (000, 255, 255)
PURPLE = (255, 000, 255)

GREEN1 = (175, 215, 70)
GREEN2 = (167, 209, 61)
GREEN3 = ( 74, 117, 44)
GREEN4 = ( 87, 138, 52)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

PLAY       = 0
MAIN_MENU  = 1
END_SCREEN = 2
SETTINGS   = 3
TUTORIAL   = 4



class Snake:
    max_time = 6

    def __init__(self, name: str, target_dir: str):
        self.name = name
        self.active = False

        self.head_up = pygame.image.load(f".\\Graphics\\{target_dir}\\head_up.png").convert_alpha()
        self.head_down = pygame.image.load(f".\\Graphics\\{target_dir}\\head_down.png").convert_alpha()
        self.head_left = pygame.image.load(f".\\Graphics\\{target_dir}\\head_left.png").convert_alpha()
        self.head_right = pygame.image.load(f".\\Graphics\\{target_dir}\\head_right.png").convert_alpha()

        self.body_horizontal = pygame.image.load(f".\\Graphics\\{target_dir}\\body_horizontal.png").convert_alpha()
        self.body_vertical = pygame.image.load(f".\\Graphics\\{target_dir}\\body_vertical.png").convert_alpha()

        self.body_bl = pygame.image.load(f".\\Graphics\\{target_dir}\\body_bl.png").convert_alpha()
        self.body_tl = pygame.image.load(f".\\Graphics\\{target_dir}\\body_tl.png").convert_alpha()
        self.body_br = pygame.image.load(f".\\Graphics\\{target_dir}\\body_br.png").convert_alpha()
        self.body_tr = pygame.image.load(f".\\Graphics\\{target_dir}\\body_tr.png").convert_alpha()

        self.tail_up = pygame.image.load(f".\\Graphics\\{target_dir}\\tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load(f".\\Graphics\\{target_dir}\\tail_down.png").convert_alpha()
        self.tail_left = pygame.image.load(f".\\Graphics\\{target_dir}\\tail_left.png").convert_alpha()
        self.tail_right = pygame.image.load(f".\\Graphics\\{target_dir}\\tail_right.png").convert_alpha()

    def set(self, hx: int, hy: int, tx: int, ty: int, face: str, maxlen: int):
        self.length = 2
        self.face = face
        self.direct = face
        self.head_ix = hx
        self.head_iy = hy
        self.pop = True
        self.counter = 0
        self.alive = True
        self.body = deque(((tx, ty),), maxlen=maxlen)

    def run_and_draw(self, surface: pygame.Surface):
        if self.counter//self.max_time: self._run()
        self.counter += 1
        self.draw(surface)

    def draw(self, surface: pygame.Surface):
        # body
        x0, y0 = self.head_ix, self.head_iy
        for (x1, y1), (x2, y2) in zip(list(islice(self.body, 0, self.length-1)), list(islice(self.body, 1, self.length))):
            ends = set((Snake.get_dir(x1, y1, x0, y0), Snake.get_dir(x1, y1, x2, y2)))
            x0, y0 = x1, y1

            if ends == set((UP, DOWN)):
                surf2 = self.body_vertical
            elif ends == set((UP, LEFT)):
                surf2 = self.body_tl
            elif ends == set((UP, RIGHT)):
                surf2 = self.body_tr
            elif ends == set((DOWN, LEFT)):
                surf2 = self.body_bl
            elif ends == set((DOWN, RIGHT)):
                surf2 = self.body_br
            elif ends == set((LEFT, RIGHT)):
                surf2 = self.body_horizontal
            else:
                raise RuntimeError(f"Invalid Option to choose the image for snake body \n"
                    f"ends: {ends}"
                    f"before: {x0, y0}  |  mid: {x1, y1}  |  after: {x2, y2}")
            surface.blit(surf2, surf2.get_rect(topleft=(x1*BIT, y1*BIT)))

        # tail
        try:
            f3 = Snake.get_dir(x1, y1, x2, y2)
        except UnboundLocalError:
            x2, y2 = self.body[0]
            f3 = Snake.get_dir(x0, y0, x2, y2)
            
        if f3 is UP:
            surf3 = self.tail_up
        elif f3 is DOWN:
            surf3 = self.tail_down
        elif f3 is LEFT:
            surf3 = self.tail_left
        elif f3 is RIGHT:
            surf3 = self.tail_right
        else:
            raise RuntimeError(f"Invalid Tail Face Option while drawing tail face: {f3}")
        surface.blit(surf3, surf3.get_rect(topleft=(x2*BIT, y2*BIT)))

        # head
        if self.face is UP:
            surf1 = self.head_up
        elif self.face is DOWN:
            surf1 = self.head_down
        elif self.face is LEFT:
            surf1 = self.head_left
        elif self.face is RIGHT:
            surf1 = self.head_right
        surface.blit(surf1, surf1.get_rect(topleft=(self.head_ix*BIT, self.head_iy*BIT)))


    @staticmethod
    def get_dir(xi: int, yi: int, xf: int, yf: int):
        dx, dy = xf-xi, yf-yi
        if   dx== 1 and dy== 0: return RIGHT
        elif dx==-1 and dy== 0: return LEFT
        elif dx== 0 and dy==-1: return UP
        elif dx== 0 and dy== 1: return DOWN
        else:
            raise RuntimeError("[Invalid coordinates for snake body to be drawn continuous]")

    def _run(self):
        self.counter %= self.max_time
        if self.face != self.direct:
            if SOUND: pygame.mixer.Sound(".\\Sound\\turn.wav").play()
        self.face = self.direct
        if self.face is UP:
            dx, dy = 0, -1
        elif self.face is DOWN:
            dx, dy = 0, +1
        elif self.face is LEFT:
            dx, dy = -1, 0
        elif self.face is RIGHT:
            dx, dy = +1, 0

        self.body.appendleft((self.head_ix, self.head_iy))
        self.head_ix, self.head_iy = self.head_ix + dx, self.head_iy + dy

        if self.pop:
            self.body.pop()
        else:
            self.length += 1
            self.pop = True

    def eat(self):
        if self.active:
            self.pop = False
            if SOUND: pygame.mixer.Sound(".\\Sound\\apple-crunch.wav").play()
    
    def eat_self(self):
        return self.onbody(self.head_ix, self.head_iy, False)

    def faceto(self, to: str):
        if ((self.face is UP    and to is not DOWN ) or
            (self.face is DOWN  and to is not UP   ) or
            (self.face is LEFT  and to is not RIGHT) or
            (self.face is RIGHT and to is not LEFT )):
            self.direct = to
    
    def onbody(self, ix: int, iy: int, check_head: bool = True):
        if check_head and ix == self.head_ix and iy == self.head_iy:
            return True
        return (ix, iy) in self.body

    def dead(self):
        self.alive = False
        if SOUND: pygame.mixer.Sound(".\\Sound\\game-over.mp3").play()
    
    def all(self):
        return set(list(self.body) + [self.head_ix, self.head_iy])
    
    def __repr__(self):
        return self.name


class Fruit:
    def __init__(self):
        self.img = pygame.image.load(".\\Graphics\\apple.png").convert_alpha()
        self.loop: list[pygame.Surface] = [
            pygame.transform.rotozoom(self.img, 0, 0.75),
            pygame.transform.rotozoom(self.img, 0, 0.80),
            pygame.transform.rotozoom(self.img, 0, 0.85),
            pygame.transform.rotozoom(self.img, 0, 0.90),
            pygame.transform.rotozoom(self.img, 0, 0.95),
            self.img,
            pygame.transform.rotozoom(self.img, 0, 0.95),
            pygame.transform.rotozoom(self.img, 0, 0.90),
            pygame.transform.rotozoom(self.img, 0, 0.85),
            pygame.transform.rotozoom(self.img, 0, 0.80),
            pygame.transform.rotozoom(self.img, 0, 0.75)
        ]
        self.counter = 0

    def draw(self, surface: pygame.Surface):
        self.counter = (self.counter+0.2)%len(self.loop)
        n = int(self.counter)
        surface.blit(self.loop[n], self.loop[n].get_rect(center=(self.ix*BIT+BIT/2, self.iy*BIT+BIT/2)))
    
    def spawn(self, ix: int, iy: int):
        self.ix = ix
        self.iy = iy

# not used for now
# class Wall:
#     def __init__(self):
#         self.path = ""
#         self.loc = []
    
#     def new(self, ix: int, iy: int):
#         self.loc.append((ix, iy))
    
#     def destroy(self, ix: int, iy:int):
#         self.loc.remove((ix, iy))

#     def draw(self, surface: pygame.Surface):
#         for ix, iy in self.loc:
#             pygame.draw.rect(surface, GREY, (ix*BIT, iy*BIT, BIT, BIT))


class Score:
    def __init__(self):
        self.val = 0
        self.icon = pygame.image.load(".\\Graphics\\apple.png").convert_alpha()
    
    def update(self):
        self.val += 1
    
    def reset(self):
        self.val = 0
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font, x: int, y: int):
        txt = font.render(f"Score: {self.val}", False, WHITE)
        surface.blit(txt, txt.get_rect(topright=(x, y)))


class Button:
    def __init__(self, image: str, center: tuple[int, int]):
        self.img = pygame.image.load(image).convert_alpha()
        self.center = center
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.img.get_rect(center=self.center))
    
    def on_button(self, dx: float = 0, dy: float = 0):
        x, y = self.center
        if self.img.get_rect(center=(x+dx, y+dy)).collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def draw_box(self, surface: pygame.Surface, dw, dh, fill, border, outline, radius):
        rect = pygame.rect.Rect(0, 0, self.img.get_width()+dw, self.img.get_height()+dh)
        rect.center = self.center
        pygame.draw.rect(SCREEN, fill, rect, 0, radius)
        pygame.draw.rect(SCREEN, outline, rect, border, radius)
        self.draw(surface)
    
    def draw_zoom(self, surface: pygame.Surface, scale: float):
        new = pygame.transform.rotozoom(self.img, 0, scale)
        surface.blit(new, new.get_rect(center=self.center))


class Num:
    wd = 40
    ht = 60

    def __init__(self):
        self.val = 0

    def path(self, digit: int):
        return f".\\Graphics\\num\\{digit}.png"

    def images(self):
        return [pygame.image.load(self.path(digit)).convert_alpha() for digit in str(abs(self.val))]

    def draw(self, surface: pygame.Surface, tx: int, ty: int):
        for i, surf in enumerate(self.images()):
            surface.blit(surf, surf.get_rect(topleft=(tx + self.wd*i, ty)))
    
    def increment(self):
        self.val += 1
    
    def reset(self):
        self.val = 0


def play(duel: bool = False):
    """To start game."""
    global GAME_STATE, HOVER, SCORE
    SNAKE1.set(2, 1, 1, 1, RIGHT, ROWS*COLS), SNAKE2.set(COLS-3, ROWS-2, COLS-2, ROWS-2, LEFT, ROWS*COLS)
    SCORE.reset()
    if duel: SNAKE2.active = True
    else: SNAKE2.active = False
    FRUIT.spawn(*spawn())
    GAME_STATE = PLAY
    click()

def on_snake(x: int, y: int):
    """Checks whether a coord lies on snakes currently running in game."""
    return SNAKE1.onbody(x, y) or (SNAKE2.onbody(x, y) if SNAKE2.active else False)

def spawn():
    """Spawns the fruit."""
    total, occupied = ROWS*COLS, SNAKE1.length + SNAKE2.length
    x, y = SNAKE1.head_ix, SNAKE1.head_iy
    if occupied < total//2:
        while on_snake(x, y):
            x, y = random.randint(0, COLS-1), random.randint(0, ROWS-1)
    else:
        comb = set([(ix, iy) for ix in range(COLS) for iy in range(ROWS)])
        occupied = SNAKE1.all().add(SNAKE2.all() if SNAKE2.active else set())
        comb.difference_update(occupied)
        x, y = random.choice(comb)
    return x, y

def result():
    """
    Checks for the result for running game.

    Duel:-
        :Winner   -> Snake object
        :draw     -> False
        :continue -> None
    Solo:-
        :Gameover -> True
        :continue -> None
    """
    if SNAKE2.active:
        if (
            (SNAKE1.head_ix==SNAKE2.head_ix and SNAKE1.head_iy==SNAKE2.head_iy) or # headon collision at same coord
            ( # headon collision with biting each other neck
                (SNAKE1.head_ix, SNAKE1.head_iy)==SNAKE2.body[0] and
                (SNAKE2.head_ix, SNAKE2.head_iy)==SNAKE1.body[0]
            ) or
            ( # both went out of bounds at same time
                (SNAKE1.head_ix not in range(COLS) or SNAKE1.head_iy not in range(ROWS)) and
                (SNAKE2.head_ix not in range(COLS) or SNAKE2.head_iy not in range(ROWS))
            )
        ):
            # checking whether both have same score or not
            if SNAKE1.length == SNAKE2.length:
                return False
            else:
                return SNAKE1 if SNAKE1.length>SNAKE2.length else SNAKE2
        elif (
            SNAKE2.eat_self() or # snake2 bites itself
            SNAKE1.onbody(SNAKE2.head_ix, SNAKE2.head_iy, False) or # snake2 bites on body of snake1
            SNAKE2.head_ix not in range(COLS) or SNAKE2.head_iy not in range(ROWS) # snake2 went out of bounds
        ):
            return SNAKE1
        elif (
            SNAKE1.eat_self() or # snake1 bites itself
            SNAKE2.onbody(SNAKE1.head_ix, SNAKE1.head_iy, False) or # snake1 bites on body of snake2
            SNAKE1.head_ix not in range(COLS) or SNAKE1.head_iy not in range(ROWS) # snake1 went out of bounds
        ):
            return SNAKE2
        else:
            return None
    else:
        return True if (
            SNAKE1.onbody(SNAKE1.head_ix, SNAKE1.head_iy, False) or
            SNAKE1.head_ix not in range(COLS) or SNAKE1.head_iy not in range(ROWS)
        ) else None

def hover_in(by):
    global HOVER, SOUND
    if HOVER is None and SOUND:
        pygame.mixer.Sound(".\\Sound\\hover.wav").play()
        HOVER = by

def hover_out(by):
    global HOVER
    if HOVER==by:
        HOVER = None

def click():
    global SOUND, HOVER
    if SOUND:
        pygame.mixer.Sound(".\\Sound\\click.wav").play()
    HOVER = None

def is_game_over():
    """Gets the game result and have decision on it."""
    global GAME_STATE, RESULT
    res = result()
    if SNAKE2.active:
        if isinstance(res, Snake):
            if res.name.lower() == 'blue': RESULT = blue_won
            elif res.name.lower() == 'pink': RESULT = pink_won
            else: raise RuntimeError("[Winner is snake object but dont matches with any snake present]")
        elif res is False:
            RESULT = draw
        else:
            return
    else:
        if res is True: RESULT = game_over
        else: return
    if SOUND: pygame.mixer.Sound(".\\Sound\\game-over.mp3").play()
    GAME_STATE = END_SCREEN


def draw_bg(surface: pygame.Surface):
    """Draws tiled background."""
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(surface, GREEN1 if (r+c)%2 else GREEN2, (c*BIT, r*BIT, BIT, BIT))

def draw_layout():
    """Draws Game Screen on window."""
    pygame.draw.rect(WIN, GREEN3, (OFFSET_X-5, OFFSET_Y-5, COLS*BIT+10, ROWS*BIT+10))
    WIN.blit(SCREEN, SCREEN.get_rect(topleft=(OFFSET_X, OFFSET_Y)))

def draw_main_menu():
    """yess this draws main menu."""
    SCREEN.fill(GREEN2)
    SCREEN.blit(title, title.get_rect(midtop=(BIT*COLS//2, 30)))
    if play_btn.on_button(OFFSET_X, OFFSET_Y):
        play_btn.draw_zoom(SCREEN, 1.2)
        hover_in('play_btn')
    else:
        play_btn.draw(SCREEN)
        hover_out('play_btn')
    if duel_btn.on_button(OFFSET_X, OFFSET_Y):
        duel_btn.draw_zoom(SCREEN, 1.2)
        hover_in("duel_btn")
    else:
        duel_btn.draw(SCREEN)
        hover_out("duel_btn")
    if setting_btn.on_button(OFFSET_X, OFFSET_Y):
        setting_btn.draw_zoom(SCREEN, 1.2)
        hover_in('setting_btn')
    else:
        setting_btn.draw(SCREEN)
        hover_out('setting_btn')
    if how_to_btn.on_button(OFFSET_X, OFFSET_Y):
        how_to_btn.draw_zoom(SCREEN, 1.2)
        hover_in('how_to_btn')
    else:
        how_to_btn.draw(SCREEN)
        hover_out('how_to_btn')

def draw_game_screen():
    """yess this draws game contents on screen."""
    FRUIT.draw(SCREEN)
    SNAKE1.run_and_draw(SCREEN)
    if SNAKE2.active: SNAKE2.run_and_draw(SCREEN)

def draw_end_screen():
    """yess this draws game end screen."""
    global RESULT
    SCREEN.fill(GREEN2)
    SCREEN.blit(RESULT, RESULT.get_rect(midtop=(BIT*COLS//2, 30)))
    if not SNAKE2.active:
        SCREEN.blit(score, score.get_rect(topleft=((COLS*BIT)/2-score.get_width(), 150)))
        SCORE.draw(SCREEN, (COLS*BIT)/2, 150)
    if play_again_btn.on_button(OFFSET_X, OFFSET_Y):
        play_again_btn.draw_zoom(SCREEN, 1.2)
        hover_in('play_again_btn')
    else:
        play_again_btn.draw(SCREEN)
        hover_out('play_again_btn')
    if main_menu_btn.on_button(OFFSET_X, OFFSET_Y):
        main_menu_btn.draw_zoom(SCREEN, 1.2)
        hover_in('main_menu_btn')
    else:
        main_menu_btn.draw(SCREEN)
        hover_out('main_menu_btn')

def draw_settings():
    SCREEN.fill(GREEN2)
    SCREEN.blit(settings, settings.get_rect(center=((COLS*BIT)//2, 40)))
    SCREEN.blit(width, width.get_rect(center=((COLS*BIT)//2, 250)))
    SCREEN.blit(height, height.get_rect(center=((COLS*BIT)//2, 320)))
    if SOUND: sound_btn = sound_enable_btn
    else: sound_btn = sound_disable_btn
    if sound_btn.on_button(OFFSET_X, OFFSET_Y):
        sound_btn.draw_zoom(SCREEN, 1.2)
        hover_in('sound_btn')
    else:
        sound_btn.draw(SCREEN)
        hover_out('sound_btn')
    if back_btn.on_button(OFFSET_X, OFFSET_Y):
        back_btn.draw_zoom(SCREEN, 1.2)
        hover_in('back_btn')
    else:
        back_btn.draw(SCREEN)
        hover_out('back_btn')


def draw_tutorial():
    pass


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Newtown`s Apple")
SCREEN = pygame.Surface((COLS*BIT, ROWS*BIT))
CLOCK = pygame.time.Clock()

SNAKE1 = Snake("Blue", "snake-blue")
SNAKE2 = Snake("Pink", "snake-pink")
FRUIT = Fruit()
SCORE = Num()


title = pygame.image.load(".\\Graphics\\title.png").convert_alpha()
blue_won = pygame.image.load(".\\Graphics\\blue-won.png").convert_alpha()
pink_won = pygame.image.load(".\\Graphics\\pink-won.png").convert_alpha()
draw = pygame.image.load(".\\Graphics\\draw.png").convert_alpha()
game_over = pygame.image.load(".\\Graphics\\game_over.png").convert_alpha()
settings = pygame.image.load(".\\Graphics\\settings.png").convert_alpha()
width = pygame.image.load(".\\Graphics\\width.png").convert_alpha()
height = pygame.image.load(".\\Graphics\\height.png").convert_alpha()
score = pygame.image.load(".\\Graphics\\score.png").convert_alpha()

play_btn = Button(".\\Graphics\\play.png", ((BIT*COLS)//2, 240))
duel_btn = Button(".\\Graphics\\duel.png", ((BIT*COLS)//2, 310))
setting_btn = Button(".\\Graphics\\settings.png", ((BIT*COLS)//2, 380))
how_to_btn = Button(".\\Graphics\\how-to.png", ((BIT*COLS)//2, 450))

sound_enable_btn = Button(".\\Graphics\\sound-enable.png", ((BIT*COLS)//2, 180))
sound_disable_btn = Button(".\\Graphics\\sound-disable.png", ((BIT*COLS)//2, 180))
back_btn = Button(".\\Graphics\\back.png", ((COLS*BIT)//2, 450))

play_again_btn = Button(".\\Graphics\\play_again.png", (BIT*COLS//2, 320))
main_menu_btn = Button(".\\Graphics\\main_menu.png", (BIT*COLS//2, 400))

FONT1 = pygame.font.SysFont("consolas", 25)
FONT2 =  pygame.font.SysFont("cambria", 48, True)

RESULT = False
SOUND = False
HOVER = None
SNAKE1.active = True
GAME_STATE = MAIN_MENU
RUN = True
while RUN:
    CLOCK.tick(FPS)

    # game end detection
    if GAME_STATE is PLAY:
        is_game_over()
 
    # event based actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                SNAKE1.faceto(UP)
            elif event.key == pygame.K_s:
                SNAKE1.faceto(DOWN)
            elif event.key == pygame.K_a:
                SNAKE1.faceto(LEFT)
            elif event.key == pygame.K_d:
                SNAKE1.faceto(RIGHT)

            if SNAKE2.active:
                if event.key == pygame.K_UP:
                    SNAKE2.faceto(UP)
                elif event.key == pygame.K_DOWN:
                    SNAKE2.faceto(DOWN)
                elif event.key == pygame.K_LEFT:
                    SNAKE2.faceto(LEFT)
                elif event.key == pygame.K_RIGHT:
                    SNAKE2.faceto(RIGHT)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAME_STATE is END_SCREEN:
                if play_again_btn.on_button(OFFSET_X, OFFSET_Y):
                    play(SNAKE2.active)
                elif main_menu_btn.on_button(OFFSET_X, OFFSET_Y):
                    GAME_STATE = MAIN_MENU
                    click()

            elif GAME_STATE is MAIN_MENU:
                if play_btn.on_button(OFFSET_X, OFFSET_Y):
                    play()
                elif duel_btn.on_button(OFFSET_X, OFFSET_Y):
                    play(True)
                elif setting_btn.on_button(OFFSET_X, OFFSET_Y):
                    click()
                    GAME_STATE = SETTINGS
                elif how_to_btn.on_button(OFFSET_X, OFFSET_Y):
                    click()
                    # GAME_STATE = TUTORIAL
            
            elif GAME_STATE is SETTINGS:
                if SOUND: sound_btn = sound_enable_btn
                else: sound_btn = sound_disable_btn
                if sound_btn.on_button(OFFSET_X, OFFSET_Y):
                    click()
                    SOUND = not SOUND
                elif back_btn.on_button(OFFSET_X, OFFSET_Y):
                    click()
                    GAME_STATE = MAIN_MENU


    # draw
    WIN.fill(GREEN4)
    if GAME_STATE is PLAY:
        if SNAKE1.head_ix == FRUIT.ix and SNAKE1.head_iy == FRUIT.iy:
            SNAKE1.eat()
            SCORE.increment()
            FRUIT.spawn(*spawn())
        if SNAKE2.head_ix == FRUIT.ix and SNAKE2.head_iy == FRUIT.iy:
            SNAKE2.eat()
            FRUIT.spawn(*spawn())
        draw_bg(SCREEN)
        draw_game_screen()
    elif GAME_STATE is MAIN_MENU:
        draw_main_menu()
    elif GAME_STATE is END_SCREEN:
        draw_end_screen()
    elif GAME_STATE is SETTINGS:
        draw_settings()
    elif GAME_STATE is TUTORIAL:
        draw_tutorial()

    draw_layout() # after updating all the required things on screen finally placing it on wim screen 
    pygame.display.update()


pygame.quit()

