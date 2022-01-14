from tkinter import *
from tkinter import messagebox
import pygame as pg
import random
import copy

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class TetrisBlocks:
    def __init__(self):
        self.round = [self.S, self.Z, self.L, self.J, self.Square, self.I, self.T]
        random.shuffle(self.round)

    def S(self, r:int=0, c:int=0):
        block = [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ]
        guide = [
            [[r+0, c+0], [r+0, c+1], [r+0, c+2]],
            [[r+1, c+0], [r+1, c+1], [r+1, c+2]],
            [[r+2, c+0], [r+2, c+1], [r+2, c+2]]
        ]
        return block, guide 

    def Z(self, r:int=0, c:int=0):
        block = [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ]
        guide = [
            [[r+0, c+0], [r+0, c+1], [r+0, c+2]],
            [[r+1, c+0], [r+1, c+1], [r+1, c+2]],
            [[r+2, c+0], [r+2, c+1], [r+2, c+2]]
        ]
        return block, guide 

    def L(self, r:int=0, c:int=0):
        block = [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ]
        guide = [
            [[r+0, c+0], [r+0, c+1], [r+0, c+2]],
            [[r+1, c+0], [r+1, c+1], [r+1, c+2]],
            [[r+2, c+0], [r+2, c+1], [r+2, c+2]]
        ]
        return block, guide 

    def J(self, r:int=0, c:int=0):
        block = [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        guide = [
            [[r+0, c+0], [r+0, c+1], [r+0, c+2]],
            [[r+1, c+0], [r+1, c+1], [r+1, c+2]],
            [[r+2, c+0], [r+2, c+1], [r+2, c+2]]
        ]
        return block, guide 

    def Square(self, r:int=0, c:int=0):
        block = [
            [1, 1],
            [1, 1]
        ]
        guide = [
            [[r+0, c+0], [r+0, c+1]],
            [[r+1, c+0], [r+1, c+1]]
        ]
        return block, guide

    def I(self, r:int=0, c:int=0):
        block = [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        guide = [
            [[r+0, c+0], [r+0, c+1], [r+0, c+2], [r+0, c+3]],
            [[r+1, c+0], [r+1, c+1], [r+1, c+2], [r+1, c+3]],
            [[r+2, c+0], [r+2, c+1], [r+2, c+2], [r+2, c+3]],
            [[r+3, c+0], [r+3, c+1], [r+3, c+2], [r+3, c+3]]
        ]
        return block, guide 


    def T(self, r:int=0, c:int=0):
        block = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        guide = [
            [[r+0, c+0], [r+0, c+1], [r+0, c+2]],
            [[r+1, c+0], [r+1, c+1], [r+1, c+2]],
            [[r+2, c+0], [r+2, c+1], [r+2, c+2]]
        ]
        return block, guide 

    def reset(self):
        Tetrisblocks = [self.S, self.Z, self.L, self.J, self.Square, self.I, self.T]
        self.round = Tetrisblocks.copy()

    def random(self):
        if not self.round:
            self.reset()
        random.shuffle(self.round)
        func = random.choice(self.round)
        self.round.pop(self.round.index(func))
        return func

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# sound
class Sound:
    def __init__(self, file):
        self.file = file
        self.sound = pg.mixer.Sound(self.file)
    def play(self):
        self.channel = self.sound.play()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class TetrisCell:
    screen = "#9CAE84"
    inactive = "#859564"
    active = "#111111"
    width = 2
    a = 2
    b = 5

    def __init__(self, canvas:Canvas, x, y, size):
        self.canvas = canvas
        self.xi = x
        self.yi = y
        self.xf = x+size
        self.yf = y+size
        self.size = size
        self.state = 'inactive'
    
    def draw(self):
        # background rectangle
        self.bg = self.canvas.create_rectangle(self.xi, self.yi, self.xf, self.yf, fill=self.screen, width=0)
        # empty rectangle
        self.st = self.canvas.create_rectangle(self.xi+self.a, self.yi+self.a, self.xf-self.a-1, self.yf-self.a-1, fill=self.screen, outline=self.inactive, width=self.width)
        # filled rectangle
        self.cn = self.canvas.create_rectangle(self.xi+self.b, self.yi+self.b, self.xf-self.b-1, self.yf-self.b-1, fill=self.inactive, width=0)
    
    def makeactive(self, full=1):
        self.canvas.itemconfig(self.st, outline=self.active)
        if full:
            self.canvas.itemconfig(self.cn, outline=self.active, fill=self.active)
            self.state = 'active'
        else:
            self.canvas.itemconfig(self.cn, outline=self.inactive, fill=self.inactive)
            self.state = 'partially active'
    
    def makeinactive(self):
        self.canvas.itemconfig(self.st, outline=self.inactive)
        self.canvas.itemconfig(self.cn, fill=self.inactive)
        self.state = 'inactive'
    
    def hide(self):
        self.canvas.itemconfig(self.st, outline=self.screen)
        self.canvas.itemconfig(self.cn, outline=self.screen, fill=self.screen)
        self.state = 'hidden'

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class TetrisCanvasGrid:
    def __init__(self, root:Tk, frame:Frame, rows:int, cols:int, cellsize:int, padding:int):
        self.root = root
        self.frame = frame
        self.rows = rows
        self.cols = cols
        self.cellsize = cellsize
        self.padding = padding

        self.width = self.cols*self.cellsize
        self.height = self.rows*self.cellsize

        self.cells = []
        self.grid = []
        self.falltime = 1000
        self.block_count = 0
        self._gen = TetrisBlocks()
        self.running = False

    # DrawCanvas-----
    def drawcanvas(self):
        """generates all cells in inactive state"""
        self.canvas = Canvas(self.frame, height=self.height-3, width=self.width-3, highlightbackground="#9CAE84")
        self.canvas.pack(padx=self.padding, pady=self.padding)
    
    # DrawCells-----
    def drawcells(self):
        for i in range(1, self.height, self.cellsize):
            tc = []
            tg = []
            for j in range(1, self.width, self.cellsize):
                temp = TetrisCell(self.canvas, j, i, self.cellsize)
                temp.draw()
                tc.append(temp)
                tg.append(0)
            self.cells.append(tc)
            self.grid.append(tg)

    # Initialization-----
    def init(self, taskmanager):
        """Initialises everything when starting the game"""
        self.taskmanager = taskmanager
        self.bindkeys()

    def start(self, *args):
        """starts the new round"""
        if not self.running:
            try:
                self.reset()
            except AttributeError:
                pass
            except Exception as e:
                messagebox.showerror("Error", ("In class TetrisCanvasGrid, in start method; unexpected", e))
            try:
                self.top.destroy()
            except:
                pass
            self.setnextblock()
            self.setactiveblock()
            self.setnextblock()
            self.update()
            self._updatesync([1, 1, 0], [None, 1, 0], [None, 1, 0], [None, 1, 0])
            self.falleventset()
            self.running = True

    # FallEvent-----
    def falleventset(self):
        """block fall after_event"""
        self.blockfall_event = self.canvas.after(ms=self.falltime, func=self.moveblockdown)
    
    # FallEventReet-----
    def falleventreset(self, same_event_again=True):
        """cancles the previous event and places new event"""
        self.canvas.after_cancel(self.blockfall_event)
        if same_event_again:
            self.falleventset()

    # KeyBindings-----
    def bindkeys(self):
        """Binds keyboard commands with block movement"""
        self.root.bind("<Key>", self.moveblock)
        self.root.bind("<Return>", self.start)
    
    # KeyActions-----
    def moveblock(self, e:Event=None):
        """takes action on keyboard input"""
        if e is not None and self.running:
            if e.keysym=='Right':
                self.moveblockright()
            if e.keysym=='Left':
                self.moveblockleft()
            if e.keysym=='Down':
                self.moveblockdown()
            # if e.keysym=='Up': # this is not for gameplay purpose
                # self.moveblockup()
            if e.keysym=='space':
                self.blockdrop()
            if e.keysym=='s':
                self.rotateblockcw()
            if e.keysym=='a':
                self.rotateblockacw()
    
    # UpdateCanvas-----
    def update(self):
        """updates everything(in graphics) only self"""
        self.refreshgrid()
        self.refreshdestiny()
        self.showblock(0)

    # GridRowQuery-----
    def anyrowfull(self):
        """returns tuple containing row/s"""
        rows = []
        for i in range(len(self.grid)):
            if all(self.grid[i]):
                rows.append(i)
        return tuple(rows)

    # CleanupActionAnim-----
    def rowcleanup_anim(self, rows):
        """destroys each row element one by one as animation effect"""
        for c in range(self.cols):
            for i in rows:
                self.grid[i][c] = 0
            self.update()
            self.root.update_idletasks()

    # GridRowAction-----
    def destroyrow(self, rows):
        """makes all values at that row 0 also updates the graphics and score"""
        if rows:
            self._score(update=len(rows))
            self.taskmanager.sound.destroy.play() # sound
            self.rowcleanup_anim(rows)
            for row in rows:
                self.grid.pop(row)
                self.grid.insert(0, [0 for _ in range(self.cols)])
                self.update()
                self._line(update=1)

    def refreshgrid(self):
        """refreshes the grid(graphics) only"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j]:
                    self.cellactive(i, j)
                else:
                    self.cellinactive(i, j)
    
    # WriteOnGrid-----
    def blockwritegrid(self, all=0):
        """write the rested block on grid"""
        for i in range(len(self.curr_block)):
            for j in range(len(self.curr_block[i])):
                try:
                    r, c = self.curr_guide[i][j]
                    if self.curr_block[i][j]:
                        self.cellactive(r, c, 1)
                    elif all:
                        self.cellinactive(r, c, 1)
                except IndexError:
                    pass

    # Cell----
    def cellactive(self, row, column, updategrid=0, full=1):
        """makes cell active if full else partial active"""
        if full:
            self.cells[row][column].makeactive(1)
        else:
            self.cells[row][column].makeactive(0)

        if updategrid:
            self.grid[row][column] = 1

    def cellinactive(self, row, column, updategrid=0):
        """makes cell inactive"""
        self.cells[row][column].makeinactive()
        if updategrid:
            self.grid[row][column] = 0

    # BlockSetup-----
    def setactiveblock(self):
        """sets current block and guide from next block and guide"""
        self.curr_block = copy.deepcopy(self.next_block)
        self.curr_guide = copy.deepcopy(self.next_guide)
        self.block_count += 1
    
    def setnextblock(self):
        """sets the next block"""
        func = self._gen.random()
        self.next_block, self.next_guide = func(0, (self.cols//2)-2)
    
    # BlockIntervals-----
    def changeactiveblock(self):
        """changes active block to next block\n
        generates next block\n
        updates the grid values\n
        destroys filled row if any"""
        self.blockwritegrid()
        self.setactiveblock()
        if self.isgameover():
            self.gameover()
        else:
            self.setnextblock()
            self.update()
            self.destroyrow(rows=self.anyrowfull())
            self.update()
            self._display(update=1)
            self.falleventreset(1)

    # BlockVisual-----
    def showblock(self, each=True):
        """shows the block(graphics)"""
        for i in range(len(self.curr_block)):
            for j in range(len(self.curr_block[i])):
                try:
                    r, c = self.curr_guide[i][j]
                    if self.curr_block[i][j]:
                        self.cellactive(r, c)
                    elif each:
                        self.cellinactive(r, c)
                except IndexError:
                    pass

    # BlockMove-----
    def moveblockup(self):
        """moves the block"""
        if self.canmoveup():
            self.taskmanager.sound.movement.play() # sound
            self._up()
            self.update()
            self.falleventreset()
    
    def moveblockdown(self, user=1):
        """moves the block"""
        if self.canmovedown():
            if user:
                self.taskmanager.sound.movement.play() # sound
            self._down()
            self.update()
            self.falleventreset()
        else:
            self.changeactiveblock()

    def moveblockleft(self):
        """moves the block"""
        if self.canmoveleft():
            self.taskmanager.sound.movement.play() # sound
            self._left()
            self.update()

    def moveblockright(self):
        """moves the block"""
        if self.canmoveright():
            self.taskmanager.sound.movement.play() # sound
            self._right()
            self.update()
    
    def blockdrop(self):
        """moves the block all the way bottom"""
        self.falleventreset(0)
        self.taskmanager.sound.harddrop.play() # sound
        while self.canmovedown():
            self.moveblockdown(0)
        self.changeactiveblock()
    
    # RotateBlock----
    def rotateblockcw(self):
        """rotates block clockwise"""
        mod_block = self._reverseitems(self._transpose(self.curr_block))
        if self.isvalidrotation(mod_block):
            self.taskmanager.sound.rotate.play() # sound
            self.curr_block = copy.deepcopy(mod_block)
            self.update()
    
    def rotateblockacw(self):
        """rotates block anti-clockwise"""
        mod_block = self._transpose(self._reverseitems(self.curr_block))
        if self.isvalidrotation(mod_block):
            self.taskmanager.sound.rotate.play() # sound
            self.curr_block = copy.deepcopy(mod_block)
            self.update()

    # BlockRotationQuery-----
    def isvalidrotation(self, newblock):
        """checks validity of new block position"""
        for i in range(len(newblock)):
            for j in range(len(newblock[i])):
                r, c = self.curr_guide[i][j]
                if r<0 or c<0 or r>self.rows or c>self.cols:
                    return False
                if newblock[i][j]:
                    try:
                        if self.grid[r][c]:
                            return False
                    except IndexError:
                        return False
        return True

    # BlockCollissionsQuery-----
    def canmoveup(self):
        """return False if block can go one step up\n
        else True if block cant move up anymore"""
        for i in range(len(self.curr_block)):
            for j in range(len(self.curr_block[i])):
                if self.curr_block[i][j]:
                    try:
                        r, c = self.curr_guide[i][j]
                        if r-1<0:
                            return False
                        if self.grid[r-1][c]:
                            return False
                    except IndexError:
                        return False
        return True
    
    def canmovedown(self):
        """return False if block can go one step down\n
        else True if block cant move down anymore"""
        for i in range(len(self.curr_block)):
            for j in range(len(self.curr_block[i])):
                if self.curr_block[i][j]:
                    try:
                        r, c = self.curr_guide[i][j]
                        if r+1>=self.rows:
                            return False
                        if self.grid[r+1][c]:
                            return False
                    except IndexError:
                        return False
        return True
    
    def canmoveleft(self):
        """return False if block can go one step left\n
        else True if block cant move left anymore"""
        for i in range(len(self.curr_block)):
            for j in range(len(self.curr_block[i])):
                if self.curr_block[i][j]:
                    try:
                        r, c = self.curr_guide[i][j]
                        if c-1<0:
                            return False
                        if self.grid[r][c-1]:
                            return False
                    except IndexError:
                        return False
        return True
    
    def canmoveright(self):
        """return False if block can go one step right\n
        else True if block cant move right anymore"""
        for i in range(len(self.curr_block)):
            for j in range(len(self.curr_block[i])):
                if self.curr_block[i][j]:
                    try:
                        r, c = self.curr_guide[i][j]
                        if c+1>=self.cols:
                            return False
                        if self.grid[r][c+1]:
                            return False
                    except IndexError:
                        return False
        return True

    # BlockDestiny-----
    def refreshdestiny(self):
        """partially activates block's destination"""
        array = self._destiny()
        for i in range(len(array)):
            for j in range(len(array[i])):
                if self.curr_block[i][j]:
                    try:
                        r, c = array[i][j]
                        self.cellactive(r, c, 0, 0)
                    except IndexError:
                        pass

    # DestinationQuery-----
    def _cangodown(self, array):
        """return False if block can go one step down\n
        else True if block cant move down anymore"""
        for i in range(len(array)):
            for j in range(len(array[i])):
                if self.curr_block[i][j]:
                    try:
                        r, c = array[i][j]
                        if r+1>=self.rows:
                            return False
                        if self.grid[r+1][c]:
                            return False
                    except IndexError:
                        return False
        return True

    # BlockDestination-----
    def _destiny(self):
        """returns list containg[r, c] to show final destiny of block"""
        guide = copy.deepcopy(self.curr_guide)
        while self._cangodown(guide):
            self._godown(guide, 1)
        return guide

    @staticmethod
    def _godown(array, val:int=1):
        """return the array with all row values increased by val"""
        for i in range(len(array)):
            for j in range(len(array[i])):
                array[i][j][0] += val
        return array
        
    # Transformations-----
    def _up(self):
        """moves block up by subtracting 1 from row"""
        for i in range(len(self.curr_guide)):
            for j in range(len(self.curr_guide[i])):
                self.curr_guide[i][j][0] -= 1

    def _down(self):
        """moves block down by adding 1 to row"""
        for i in range(len(self.curr_guide)):
            for j in range(len(self.curr_guide[i])):
                self.curr_guide[i][j][0] += 1

    def _left(self):
        """moves block left by subtracting 1 from column"""
        for i in range(len(self.curr_guide)):
            for j in range(len(self.curr_guide[i])):
                self.curr_guide[i][j][1] -= 1

    def _right(self):
        """moves block right by adding 1 to column"""
        for i in range(len(self.curr_guide)):
            for j in range(len(self.curr_guide[i])):
                self.curr_guide[i][j][1] += 1

    # GameoverQuery-------------------------
    def isgameover(self):
        """checks if game is over or not"""
        for i in range(len(self.curr_guide)):
            for j in range(len(self.curr_guide[i])):
                r, c = self.curr_guide[i][j]
                if self.grid[r][c] and self.curr_block[i][j]:
                    return True
        return False
        
    # GameoverAction-------------------------
    def gameover(self):
        """action on gameover"""
        self.running = False
        self.taskmanager.nextblock.shownull()
        self.gameoverwindow()

    # Reset-------------------------
    def reset(self):
        """resets the grid, side displays, block generator"""
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.refreshgrid()
        self._gen.reset()
        self._updatesync([0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1])

    # GameoverWindow-------------------------
    def gameoverwindow(self):
        self.top = Toplevel()
        self.top.title("GameOver")
        self.top.resizable(0, 0)

        fnt = ('Times New Roman', 20, 'italic')
        msg = f"Your Score: {self.taskmanager.score.value}\nLines destroyed: {self.taskmanager.line.value}"

        fr = Frame(self.top, bg="black")
        fr.pack()

        lb = Label(fr, text=msg, relief=RAISED, border=10, bg=TetrisCell.screen, fg="black", font=fnt)
        lb.pack(padx=10, pady=10, ipadx=20, ipady=20)

        self.top.mainloop()

    # Tools-------------------------
    @staticmethod
    def _reverseitems(array):
        """reverse each element in the array"""
        for i in array:
            i.reverse()
        return array

    @staticmethod
    def _transpose(array):
        """returns transpose of array"""
        output = []
        for i in range(len(array)):
            temp = []
            for j in range(len(array[i])):
                temp.append(array[j][i])
            output.append(temp)
        return output

    def _updatesync(self, display, score, line, level):
        """triggers display, score, line, level with their respective values\n
        order: update, reresh, reset"""
        self._display(*display)
        self._score(*score)
        self._line(*line)
        self._level(*level)

    # DisplayNextBlock-----
    def _display(self, update=None, refresh=None, reset=None):
        """triggers corresponding task manager functions"""
        self.taskmanager.display_func(update, refresh, reset)
    
    # Score-----
    def _score(self, update=None, refresh=None, reset=None):
        """triggers corresponding task manager functions"""
        self.taskmanager.score_func(update, refresh, reset)
    
    # Line-----
    def _line(self, update=None, refresh=None, reset=None):
        """triggers corresponding task manager functions"""
        self.taskmanager.line_func(update, refresh, reset)
        if (self.taskmanager.line.value)%10==0 and self.taskmanager.line.value!=0:
            self._level(update=1)
    
    # Level-----
    def _level(self, update=None, refresh=None, reset=None):
        """triggers corresponding task manager functions"""
        self.taskmanager.level_func(update, refresh, reset)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class TetrisBlockDisplay(TetrisCanvasGrid):
    def __init__(self, root, frame, rows, cols, cellsize, padding, target:TetrisCanvasGrid):
        super().__init__(root, frame, rows, cols, cellsize, padding)
        self.target = target
    
    def drawcanvas(self):
        return super().drawcanvas()
    
    def drawcells(self):
        return super().drawcells()
    
    def getblock(self):
        self.block = self.target.next_block

    def showblock(self):
        try:
            for i in range(self.rows):
                for j in range(self.cols):
                    try:
                        if self.block[i][j]:
                            self.cells[i][j].makeactive()
                        else:
                            self.cells[i][j].hide()
                    except IndexError:
                            self.cells[i][j].hide()
        except AttributeError:
            self.getblock()
    
    def shownull(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].makeinactive()

    def update(self):
        self.getblock()
        self.refresh()

    def refresh(self):
        self.showblock()
    
    def reset(self):
        del self.grid
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.refresh()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class Value:
    screen = "#9CAE84"
    def __init__(self, frame, increment):
        self.frame = frame
        self.value = 0
        self.inc = increment
    
    def draw(self):
        self.display = Label(self.frame, text=f"{self.value}", bg=self.screen, font=('Helvatica', 20, 'bold'), justify=RIGHT)
        self.display.pack()
    
    def update(self):
        self.value += self.inc
        self.refresh()
    
    def refresh(self):
        self.display.config(text=f"{self.value}")
    
    def reset(self):
        self.value = 0
        self.refresh()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class Score(Value):
    def __init__(self, frame, increment):
        self.frame = frame
        self.value = 0
        self.inc = increment
    
    def draw(self):
        return super().draw()
    
    def refresh(self):
        return super().refresh()
    
    def update(self, count, lvl):
        self.value += int((self.inc[count-1])*(lvl+1))
        self.refresh()
    
    def reset(self):
        return super().reset()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# sound
class SFX:
    softdrop_file = "sfx/softdrop.wav"
    harddrop_file = "sfx/harddrop.wav"
    rotate_file = "sfx/rotate.wav"
    movement_file = "sfx/movement.wav"
    newblock_file = "sfx/newblock.wav"
    destroy_file = "sfx/destroy.wav"
    levelup_file = "sfx/levelup.wav"

    def __init__(self):
        self.softdrop = Sound(self.softdrop_file)
        self.harddrop = Sound(self.harddrop_file)
        self.rotate = Sound(self.rotate_file)
        self.movement = Sound(self.movement_file)
        self.newblock = Sound(self.newblock_file)
        self.destroy = Sound(self.destroy_file)
        self.levelup = Sound(self.levelup_file)
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class TaskManager:
    def __init__(self):
        pass

    def init(self, nextdisp_obj:TetrisBlockDisplay, score_obj:Score, line_obj:Value, level_obj:Value, sound_obj:SFX):
        self.nextblock = nextdisp_obj
        self.score = score_obj
        self.line = line_obj
        self.level = level_obj
        self.sound = sound_obj
    
    def display_func(self, update=None, refresh=None, reset=None):
        if reset is not None:
            self.nextblock.reset()
        if refresh is not None:
            self.nextblock.refresh()
        if update is not None:
            self.sound.newblock.play() # newblock sound
            self.nextblock.update()

    def score_func(self, update=None, refresh=None, reset=None):
        if reset is not None:
            self.score.reset()
        if refresh is not None:
            self.score.refresh()
        if update is not None:
            self.score.update(update, self.level.value)

    def line_func(self, update=None, refresh=None, reset=None):
        if refresh is not None:
            self.line.refresh()
        if update is not None:
            self.line.update()
        if reset is not None:
            self.line.reset()

    def level_func(self, update=None, refresh=None, reset=None):
        if refresh is not None:
            self.level.refresh()
        if update is not None:
            self.sound.levelup.play() # levelup sound
            self.level.update()
        if reset is not None:
            self.level.reset()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
class Tetris:
    def __init__(self) -> None:
        self.running = 0
     
    def preparewindow(self):
        self.root = Tk()
        self.root.title("Tetris")
        self.root.resizable(0, 0)
        self.root.config(bg="grey")

    def preparelayout(self):
        col = "#9CAE84"
        fonts = ('Times New Roman', 15, 'italic')

        # main frame
        self.main = Frame(self.root, bg=col, border=5, relief=SOLID)
        self.main.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        # display
        self.display = Frame(self.main, bg=col, border=3, relief=FLAT)
        self.display.pack(side=RIGHT, padx=10, fill=Y)

        # nextblock
        self.viewnext = LabelFrame(self.display, text="Next...", bg=col, border=2, relief=FLAT, font=fonts)
        self.viewnext.pack(padx=11, pady=20, fill=X, anchor='n')

        # score
        self.scoreboard = LabelFrame(self.display, text="Score:", bg=col, border=2, relief=FLAT, font=fonts)
        self.scoreboard.pack(padx=11, pady=10, fill=X)

        # lines
        self.lineboard = LabelFrame(self.display, text="Lines:", bg=col, border=2, relief=FLAT, font=fonts)
        self.lineboard.pack(padx=11, pady=10, fill=X)

        # level
        self.levelboard = LabelFrame(self.display, text="Level:", bg=col, border=2, relief=FLAT, font=fonts)
        self.levelboard.pack(padx=11, pady=10, fill=X)

    def loadcontent(self):

        self.taskmanager = TaskManager()
        sz = 24

        self.playspace = TetrisCanvasGrid(self.root, self.main, 20, 10, sz, 3)
        self.playspace.drawcanvas()
        self.playspace.drawcells()

        self.sidespace = TetrisBlockDisplay(self.root, self.viewnext, 2, 4, sz, 6, self.playspace)
        self.sidespace.drawcanvas()
        self.sidespace.drawcells()

        self.score_val = Score(self.scoreboard, (40, 100, 300, 1200))
        self.score_val.draw()

        self.line_val = Value(self.lineboard, 1)
        self.line_val.draw()

        self.level_val = Value(self.levelboard, 1)
        self.level_val.draw()

        self.soundeffects = SFX() # sound

        self.taskmanager.init(self.sidespace, self.score_val, self.line_val, self.level_val, self.soundeffects)
    
    def syncmainloop(self):
        self.playspace.init(self.taskmanager)
        self.root.mainloop()
    
    def run(self):
        self.preparewindow()
        self.preparelayout()
        pg.mixer.init(11025) # sound
        self.loadcontent()
        self.syncmainloop()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
def main():
    Game = Tetris()
    Game.run()
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
if __name__ == '__main__':
    main()

"""
this game requires pygame(not present by default) module for sounds

currently there are some issues with the rotation of blocks at one side

How to play:
    arrow keys to move (only left right down)
    a to rotate anti-clockwise; s for clockwise rotation
    spacebar for harddrop
"""