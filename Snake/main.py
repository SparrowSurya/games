from tkinter import *
from tkinter import messagebox
import random

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# Literals
EMPTY = 'empty'
BODY = 'snake_body'
HEAD = 'snake_head'
FOOD = 'food'
OBSTACLE = 'obstacle'
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class _Cell:
    def __init__(self, canvas:Canvas, xi, yi, size, color):
        self.canvas:Canvas = canvas
        self.xi:int = xi
        self.yi:int = yi
        self.xf:int = xi + size
        self.yf:int = yi + size
        self.size:int = size
        self.color = color
        self.temp_color = None
        self.status:str = EMPTY
    
    def _draw(self):
        """draws cell at beginning"""
        self.br = self.canvas.create_rectangle(self.xi, self.yi, self.xf, self.yf, fill="black", width=0)
        self.bg = self.canvas.create_rectangle(self.xi+1, self.yi+1, self.xf-1, self.yf-1, fill=self.color, width=0)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class Cell(_Cell):
    def __init__(self, canvas:Canvas, xi, yi, size, color):
        super().__init__(canvas, xi, yi, size, color)

    def draw(self):
        """draws cell at beginning"""
        super()._draw()
    
    def showcolor(self, color, status):
        """changes the colour"""
        self.temp_color = color
        self.status = status
        self.canvas.itemconfig(self.bg, fill=color)

    def refresh(self):
        """refreshes cell with the lastest color"""
        if self.temp_color:
            self.canvas.itemconfig(self.bg, fill=self.temp_color)
        else:
            self.canvas.itemconfig(self.bg, fill=self.color)

    def reset(self):
        """resets cell with original color"""
        self.temp_color = None
        self.status = EMPTY
        self.canvas.itemconfig(self.bg, fill=self.color)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class _Board:
    def __init__(self, frame:Frame, rows, cols, cellsize, cellcolor):
        self.frame:Frame = frame
        self.rows:int = rows
        self.cols:int = cols
        self.cellsize:int = cellsize
        self.cellcolor:str = cellcolor
        self.cells:list = []

    def _craetecanvas(self):
        """creates canvas"""
        self.canvas = Canvas(
            self.frame,
            height=self.rows*self.cellsize,
            width=self.cols*self.cellsize,
            highlightthickness=0
        )
        p = 1
        self.canvas.pack(padx=p, pady=p)

    def _drawcells(self):
        """draws cells on canvas"""
        for i in range(self.rows):
            temp = []
            for j in range(self.cols):
                cell = Cell(self.canvas, j*self.cellsize, i*self.cellsize, self.cellsize, self.cellcolor)
                cell.draw()
                temp.append(cell)
            self.cells.append(temp)
    
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class Board(_Board):
    def __init__(self, frame:Frame, rows, cols, cellsize, cellcolor):
        super().__init__(frame, rows, cols, cellsize, cellcolor)

    def craetecanvas(self):
        """creates canvas"""
        super()._craetecanvas()

    def drawcells(self):
        """draws cells on canvas"""
        super()._drawcells()
    
    def refresh_all(self):
        """refreshes all cells"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].refresh()

    def refreshcell(self, r, c):
        """refreshes mentioned cell"""
        self.cells[r][c].refresh()

    def resetcell(self, r, c):
        """resets mentioned cell"""
        self.cells[r][c].reset()
    
    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.resetcell(i, j)
        self.refresh_all()
        
    def drawobstacle(self, row:int, col:int):
        """draws obstacle in the board not developed"""
        self.cells[row][col].showcolor("black", OBSTACLE)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class Snake:
    def __init__(self, board:Board, color:tuple((str, str)), resttime:int):
        self.board:Board = board
        self.color_head = color[0]
        self.color_body = color[1]
        self.r:list = [0]
        self.c:list = [0]
        self.dir = E
        self.main_dir = E
        self.resttime:int = resttime
        self.refresh(full=True)
        self.grow = False
        self.stop = True
    
    @property
    def length(self):
        if len(self.r)==len(self.c):
            return len(self.r)
        else:
            raise Exception("something went wrong; some parts of snake has missing coordinates")
    
    @property
    def head(self):
        """returns row and column of the head"""
        return self.r[0], self.c[0]
    
    @property
    def tail(self):
        """returns row and column of the head"""
        return self.r[-1], self.c[-1]

    def init(self, game):
        """important for game to run good"""
        self.game = game

    def run(self):
        """initialisez the snake to keep running"""
        self.set_event()
     
    def keep_moving(self):
        self.set_event()
    
    def set_event(self):
        """sets snake moving event"""
        if not self.stop:
            self.move_event = self.board.canvas.after(self.resttime, self.move)
    
    def get_next_tile(self, dr=0, dc=0):
        """returns next cell for head to show on"""
        r = self.board.rows-1 if self.r[0]+dr<0 else 0 if self.r[0]+dr>=self.board.rows else self.r[0]+dr
        c = self.board.cols-1 if self.c[0]+dc<0 else 0 if self.c[0]+dc>=self.board.cols else self.c[0]+dc
        return r, c
    
    def _move(self, r, c):
        """moves snake ahead"""
        self.r.insert(0, r)
        self.c.insert(0, c)

        # snake grow control
        if not self.grow:
            self.cleartail()
            self.refresh(full=0)
        else:
            self.refresh(full=1)
    
    def recordNmove(self, dr=0, dc=0):
        """records the next valid tile"""
        isover = False
        self.main_dir = self.dir
        r, c = self.get_next_tile(dr, dc)
        
        # next cell detection
        cell_status = self.cellahead(r, c)

        if (cell_status is BODY and (r, c) != self.tail) or cell_status is OBSTACLE: # game end
            self.game.end()
            self.stop = True
        else: # game not end
            if cell_status is FOOD: # food ahead
                isover = self.game.newfood()
                self.grow = True
            else: # food not ahead
                self.grow = False
            
            # moving snake
            self.r.insert(0, r)
            self.c.insert(0, c)

            # snake grow control
            if not self.grow:
                self.cleartail()
                self.refresh(full=0)
            else:
                self.refresh(full=1)
        
        if isover: # game won
            self.game.won()
        elif not self.stop: # move
            self.keep_moving()
        
    def move(self):
        """moves snake one cell in the direction"""
        if self.dir == N: self.recordNmove(dr=-1)
        if self.dir == S: self.recordNmove(dr=+1)
        if self.dir == E: self.recordNmove(dc=+1)
        if self.dir == W: self.recordNmove(dc=-1)
    
    def _stop(self):
        """stops the snake"""
        self.board.canvas.after_cancel(self.move_event)
    
    def cleartail(self):
        """clears the last cell"""
        self.board.resetcell(self.r[-1], self.c[-1])
        self.r.pop(-1)
        self.c.pop(-1)
    
    def set_direction(self, direction):
        """sets appropriate direction based upon key pressed and snake movement"""
        if direction==E and self.main_dir is not W:
            self.dir = E
        if direction==W and self.main_dir is not E:
            self.dir = W
        if direction==N and self.main_dir is not S:
            self.dir = N
        if direction==S and self.main_dir is not N:
            self.dir = S

    def refresh(self, full=0):
        """refreshes snake, fully if full else head, after head"""
        if full:
            for i in range(self.length):
                if i==0: # head
                    self.board.cells[self.r[i]][self.c[i]].showcolor(self.color_head, HEAD)
                else:
                    self.board.cells[self.r[i]][self.c[i]].showcolor(self.color_body, BODY)
        else:
            self.board.cells[self.r[0]][self.c[0]].showcolor(self.color_head, HEAD) # head
            try:
                self.board.cells[self.r[1]][self.c[1]].showcolor(self.color_body, BODY) # just after head
            except: # the snake has only head
                pass

    def cellahead(self, nr=0, nc=0):
        """returns status of the cell"""
        return self.board.cells[nr][nc].status

    def reset(self):
        self.r = [0]
        self.c = [0]
        self.dir = self.main_dir = E
        self.grow = False
        self.stop = False
        self.refresh(1)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class Food:
    def __init__(self, board:Board, color:str):
        self.board:Board = board
        self.color:str = color
        self.max_ir = len(self.board.cells)-1
        self.max_ic = len(self.board.cells[0])-1
    
    def _getemptycells(self):
        cells = []
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                if self.board.cells[i][j].status is EMPTY:
                    cells.append((i, j))
        return tuple(cells)
    
    def gen(self):
        """finds and places food on board"""
        cells = self._getemptycells()
        n = random.randint(0, len(cells)-1)
        self.show(*cells[n])
    
    def show(self, r, c):
        """shows food on board"""
        self.board.cells[r][c].showcolor(self.color, FOOD)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class Game:
    def __init__(self, title:str, rows:int, cols:int, cellsize:int, cell_color:str, snake_color:tuple or list, food_color:str, snake_rest_time:int):
        """input game constants"""
        self.title:str = title
        self.rows:int = rows
        self.cols:int = cols
        self.cellsize:int = cellsize
        self.cell_color:str = cell_color
        self.snake_color:str = snake_color
        self.food_color:str = food_color
        self.snake_rest_time:int = snake_rest_time
        self.started:bool = False
        self.score:int= 0
    
    def prepare_window(self):
        self.root = Tk()
        self.root.title(self.title)
        self.root.resizable(0, 0)
        self.root.config(bg="white")
    
    def prepare_layout(self):
        self.canvas_fr = Frame(self.root, bg="black")
        self.canvas_fr.pack(padx=2, pady=2)
    
    def prepare_content(self):
        self.board = Board(self.canvas_fr, self.rows, self.cols, self.cellsize, self.cell_color)
        self.board.craetecanvas()
        self.board.drawcells()

        self.snake = Snake(self.board, self.snake_color, self.snake_rest_time)
        self.snake.refresh()

        self.food = Food(self.board, self.food_color)
    
    def newfood(self):
        if self.snake.length+1 == self.rows*self.cols:
            return True
        else:
            self.food.gen()
            self.score += 1
            return False

    def keybind(self, e:Event):
        """snake movement key binds"""
        key = e.keysym
        if key=='Right' and self.started: self.snake.set_direction(E)
        if key=='Left' and self.started: self.snake.set_direction(W)
        if key=='Up' and self.started: self.snake.set_direction(N)
        if key=='Down' and self.started: self.snake.set_direction(S)

    def startgame(self, e:Event):
        if not self.started:
            self.reset()
            self.started = True
            self.food.gen()
            self.snake.run()

    def reset(self):
        self.score = 0
        self.board.reset()
        self.snake.reset()

    def init(self):
        self.root.bind("<Key>", self.keybind)
        self.root.bind("<Return>", self.startgame)
        self.snake.init(self)

    def loop(self):
        self.root.mainloop()
    
    def end(self):
        self.started = False
        messagebox.showinfo("Game ended", f"Your score: {self.score}")

    def won(self):
        self.started = False
        messagebox.showinfo("Game won", f"Your score: {self.score}")

    def reset(self):
        self.board.reset()
        self.snake.reset()
        self.started = False
        self.score = 0

    def run(self):
        self.prepare_window()
        self.prepare_layout()
        self.prepare_content()
        self.init()
        self.loop()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
if __name__ == '__main__':
    # Game("python mania", 25, 25, 24, "light grey", ["blue", "yellow"], "orange", 75).run()
    Game("python mania", 25, 25, 24, "black", ["#28FC0A", "#28FC0A"], "#F90101", 60).run()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
"""
how to play:
    arrow keys to move
    enter to start or restart
"""