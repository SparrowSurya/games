#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
import json
from tkinter import *
from tkinter import messagebox
import random
import copy



#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# rawboard
class RawBoard:
    maxlen = 60
    def __init__(self, rows, columns, bombs):
        self.isend = False
        self.check_input(rows, columns, bombs)
        self.rows = rows
        self.columns = columns
        self.bombs = bombs+1
        self.bomb_tiles = []

    def check_input(self, rows, columns, bombs):
        if type(rows) != int or type(columns) != int or type(bombs) != int:
            messagebox.showwarning("Invalid Input", "Enter integer")
            self.isend = True
        if rows < 1:
            messagebox.showwarning("Invalid Input", "minimum row size should be 2")
            self.isend = True
        if columns < 1:
            messagebox.showwarning("Invalid Input", "minimum column size should be 2")
            self.isend = True
        if rows > self.maxlen:
            messagebox.showwarning("Invalid Input", f"maximum row size should be {self.maxlen}")
            self.isend = True
        if columns > self.maxlen:
            messagebox.showwarning("Invalid Input", f"maximum column size should be {self.maxlen}")
            self.isend = True
        if bombs < 1:
            messagebox.showwarning("Invalid Input", f"minimum bombs should be 1")
            self.isend = True
        if bombs > rows*columns-2:
            messagebox.showwarning("Invalid Input", f"maximum bombs should be {rows*columns-2}")
            self.isend = True

    def placebombs(self):
        while len(self.bomb_tiles) != self.bombs:
            r = random.randint(0, self.rows-1)
            c = random.randint(0, self.columns-1)
            self.bomb_tiles.append((r,c))
            self.bomb_tiles = list(set(self.bomb_tiles))


    def generate(self):
        """0 -> no bomb\n
        1 -> bomb"""
        if self.isend:
            return False

        rawboard = []
        self.placebombs()
        # making board with bombs
        for i in range(self.rows):
            temp = []
            for j in range(self.columns):
                if (i,j) in self.bomb_tiles: # bomb cell
                    temp.append(1)
                else:
                    temp.append(0)
            rawboard.append(temp)

        return rawboard

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# gameboard
class GameBoard:
    def __init__(self, rawboard):
        self.rawboard = rawboard
        self.row = len(rawboard)
        self.col = len(rawboard[0])


    def check_one_neighbourbomb(self, curr_r, curr_c, direction):
        """Returning:\n
        \tTrue   -> Target found\n
        \tFalse  -> target not found"""

        _r = curr_r-1 if 'n' in direction else curr_r+1 if 's' in direction else curr_r
        _c = curr_c-1 if 'w' in direction else curr_c+1 if 'e' in direction else curr_c

        try:
            if _r in range(0, self.row) and _c in range(0, self.col):
                if self.rawboard[_r][_c] == 1:
                    return True
            else:
                return False
        except IndexError:
            return False
        except Exception as e:
            messagebox.showinfo("Developer bad Exception Handling", "function: check_onedir", f"error: {e}")
        return False


    def count_all_neighboursbombs(self, curr_r, curr_c):
        num = 0
        directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        for direction in directions:
            num += 1 if self.check_one_neighbourbomb(curr_r, curr_c, direction) else 0
        return num

    def translate(self):
        """
        returning board:\n
        \tnull tile      -> 	0\n
        \tbomb tile      -> 	-1\n
        \tnumbered tile  -> 	number
        """
        gameboard = []
        for r in range(self.row):
            temp = []
            for c in range(self.col):

                if self.rawboard[r][c] == 1: # current tile is a bomb tile
                    temp.append(-1)

                else: # rawboard[r][c] == 0: # current tile is not a bomb tile
                    neighbour_bombs = self.count_all_neighboursbombs(r, c)

                    if neighbour_bombs == 8:
                        messagebox.showinfo("bomb island", f"the bomb at {r} {c} is fully surrounded by bombs")
                    temp.append(neighbour_bombs)

            gameboard.append(temp)
        return gameboard

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class timer
class Timer:
    def __init__(self, label:Label):
        self.label = label
        self.countdown = 0
        self.isrunning = False # start/pause:False; started:True; end:None

    def pause(self):
        """to pause timer"""
        self.isrunning = False

    def stop(self):
        """to stop timer, resets timer at back end; and pauses at front end"""
        self.isrunning = None
        self.countdown = 0

    def resume(self):
        """to continue from where u left"""
        self.isrunning = True
        self._update_after_sec()

    def reset(self):
        """to reset timer"""
        self.countdown = 0
        self.display_update(0)

    def start(self):
        """to play timer from start"""
        self.reset()
        self.isrunning = True
        self._update_after_sec()

    def display_update(self, running:bool=True):
        time = to_strdigits(int(self.countdown%1000), 3)
        self.label.config(text=time)
        if running:
            self.label.after(1000, func=self._update_after_sec)
        
    def _update_after_sec(self):
        """to make timer keep running and regular update of display"""
        if self.isrunning:
            self._update()
            self.display_update(1)

    def _update(self, val:int=1):
        """increment countdown by 1"""
        self.countdown += val

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class mines
class MinesCountDisplay:
    def __init__(self, label:Label):
        self.label = label
        self.mines_display_count = 0

    def reset(self):
        self.mines_display_count = 0
        self.mines_original_count = 0
        self.label.config(text='000')

    def update(self, increment:int):
        self.mines_display_count += increment
        self.display()
    
    def display(self):
        display = to_strdigits(self.mines_display_count, 3)
        self.label.config(text=display)
    
    def setcount(self, count):
        self.mines_original_count = count
        self.mines_display_count = count
        self.display()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# task manager class
class TaskManager:
    def __init__(self, minedisplay:MinesCountDisplay, timer:Timer, emojibtn):
        """It manages task of producing sound, managin display of mines and handling timer"""
        self.minedisp = minedisplay
        self.timer = timer
        self.emojibtn = emojibtn
        self.isgameend = False
        self.slt_clk = 0
        self.srt_clk = 0
        self.dlt_clk = 0
        self.win_gamewon = GamewonWindow()

    def reset(self):
        self.slt_clk = 0
        self.srt_clk = 0
        self.dlt_clk = 0
        self.timer.reset()
        self.minedisp.reset()

    def left_click(self):
        if self.timer.isrunning == False:
            self.timer.start()
        self.slt_clk += 1

    def right_click(self, val:int):
        self.mine_update(val)
        self.srt_clk += 1

    def double_left_click(self):
        self.dlt_clk += 1

    def gameended(self):
        self.isgameend = True
        self.pause_timer()
        self.timer.isrunning = False
        self.minedisp.reset()
    
    def pause_timer(self):
        self.timer.pause()

    def resume_timer(self):
        if self.timer.isrunning:
            self.timer.resume()

    def mine_update(self, increment:int):
        if self.timer.isrunning is not None:
            self.minedisp.update(increment)

    def game_end(self, won:bool):
        self.gameended()
        if won:
            self.emojibtn.display('win')
            self.win_gamewon.create(self.timer.countdown, self.slt_clk+self.dlt_clk)
        else:
            self.emojibtn.display('sad')
    
    def destroy_winWIN(self):
        self.win_gamewon.destroy()

    def reset_buttons(self, tileboard):
        tileboard.reset()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# tiles <Main>
class TileBoard:
    def __init__(self, root:Tk, taskmanager:TaskManager, gameboard:list, images:dict, tiles_fr:Frame, mines_loc):
        # bind
        root.bind('<Double-Button-1>', self.mannual_double_click)

        self.root = root
        self.taskmanager = taskmanager
        self.board = copy.deepcopy(gameboard)
        self.images = images
        self.frame = tiles_fr
        self.minesloc = mines_loc
        self.isfirstclick = True
        self.buttons = [] # 2d array with cell [(Button)/Label, (True/False)/None]
        self.HIGHLIGHT = []
        self.isgameend = False


    def reset(self):
        """resets button, highlight, gameboard"""
        self.delete_buttons()
        self.buttons.clear()
        self.HIGHLIGHT.clear()
        self.board.clear()
        self.isfirstclick = True

    def delete_buttons(self):
        for r in range(len(self.buttons)):
            for c in range(len(self.buttons[r])):
                btn = self.buttons[r][c][0]
                btn.destroy()

    # settings functions
    def update_info(self):
        pass

    def get_buttons_list(self):
        return self.buttons

    def playagain_reset(self):
        self.isfirstclick = True

    def gameend(self, won:bool):
        self.isfirstclick = None
        self.isgameend = True
        self.taskmanager.game_end(won)

    # checking functions
    def update_gameboard(self, updated:list):
        self.board = copy.deepcopy(updated)

    def type(self, r:int, c:int):
        return type(self.buttons[r][c][0])
    
    def isflaged(self, r:int, c:int):
        return self.buttons[r][c][1]==False

    def get_image(self, row, col, isclicked):
        val = self.board[row][col]
        if val == -1:
            return "tile_blast" if isclicked else "tile_bomb"
        else:
            return f"tile_{val}"

    def check_gamewon(self):
        tiles_left = 0
        if self.isgameend is not True:
            for i in range(len(self.buttons)):
                for j in range(len(self.buttons[i])):
                    if self.type(i, j) == Button:
                        tiles_left += 1
                    if tiles_left>self.taskmanager.minedisp.mines_original_count:
                        return False
            if tiles_left==self.taskmanager.minedisp.mines_original_count:
                return True
            else:
                return False

    # hover functions
    def highlight(self, event:Event):
        if not self.isgameend:
            wid = self.root.winfo_containing(event.x_root, event.y_root)
            if wid is not None and isinstance(wid, Button):
                loc = wid.grid_info()
                r, c = loc['row'], loc['column']
                if self.buttons[r][c][1] != False:
                    self.buttons[r][c][0].config(image=self.images['tile_highlight'])
                    self.HIGHLIGHT.clear()
                    self.HIGHLIGHT = [r, c]

    def unhighlight(self, event:Event):
        if not self.isgameend:
            if self.HIGHLIGHT:
                r,c = self.HIGHLIGHT
                if isinstance(self.buttons[r][c][0], Button):
                    if self.buttons[r][c][1] == True:
                        self.buttons[r][c][0].config(image=self.images['tile_default'])
                    elif self.buttons[r][c][1] == False:
                        self.buttons[r][c][0].config(image=self.images['tile_flag'])

    # create tile
    def create(self, rows:int, cols:int):
        """creating tiles only"""
        for r in range(rows):
            temp = []
            for c in range(cols):
                btn = Button(self.frame, image=self.images["tile_default"], bd=0, highlightthickness=0, command=lambda i=r, j=c: self.click(i, j, 0))
                btn.grid(row=r, column=c)
                btn.tk_focusFollowsMouse()
                btn.bind('<Button-3>', self.flag)
                btn.bind('<Enter>', self.highlight)
                btn.bind('<Leave>', self.unhighlight)
                temp.append([btn, True])
            self.buttons.append(temp)

    # click functions
    def flag(self, event:Event):
        """flags the unflaged button or unflags the flag button"""
        if not self.isgameend:
            wid = self.root.winfo_containing(event.x_root, event.y_root)
            if wid is not None and isinstance(wid, Button):
                loc = wid.grid_info()
                row = loc['row']
                col = loc['column']
                if self.buttons[row][col][1] == True: # flag unflaged tile
                    wid.config(image=self.images["tile_flag"])
                    self.buttons[row][col].pop(1)
                    self.buttons[row][col].insert(1, False)
                    self.taskmanager.right_click(-1)
                else: # buttons[row][col][1] == False # unflag flaged tile
                    wid.config(image=self.images["tile_default"])
                    self.buttons[row][col].pop(1)
                    self.buttons[row][col].insert(1, True)
                    self.taskmanager.right_click(+1)

    def click(self, row, col, auto:bool=1):
        """thie method being called when a button is clicked"""
        if self.isfirstclick:
            self.isfirstclick = False
            updated_board = board_manipulate(row, col, self.board, self.minesloc)
            self.update_gameboard(updated_board)
        if self.isgameend: # if game has ended
            pass
        else:
            # clicked
            if self.buttons[row][col][1] is True: # unflaged btn
                tile_val = self.board[row][col]
                if tile_val == -1: # mine
                    if not auto:
                        self.taskmanager.left_click()
                    self.unhidemines(row, col)
                    '''declaration of game end'''
                elif tile_val in range(1, 9): # number
                    if not auto:
                        self.taskmanager.left_click()
                    self.showtile(row, col, f"tile_{tile_val}")
                elif tile_val == 0: # null
                    self.taskmanager.left_click()
                    self.explorenull(row, col)
            # checking game won
            if self.check_gamewon():
                self.gameend(1)


    def mannual_double_click(self, event:Event):
        if self.isgameend==False:
            wid = self.root.winfo_containing(event.x_root, event.y_root)
            if wid is not None and isinstance(wid, Label):
                loc = wid.grid_info()
                row, col = loc['row'], loc['column']
                if self.board[row][col] != 0:
                    if self.double_click_valid(row, col):
                        self.taskmanager.double_left_click()
                        self.explore_adj(row, col)

    def auto_double_click(self, row, col):
        if self.board[row][col] != 0:
            if self.double_click_valid(row, col):
                self.explore_adj(row, col)

    def explore_adj(self, row, col):
        dirs = ['n', 'e', 's', 'w', 'ne', 'se', 'sw', 'nw']
        for dir in dirs:
            _r = row-1 if 'n' in dir else row+1 if 's' in dir else row
            _c = col-1 if 'w' in dir else col+1 if 'e' in dir else col
            try:
                if type(self.buttons[_r][_c][0]) == Button and _r>=0 and _c>=0:
                    if self.buttons[_r][_c][1] == True:
                        if self.board[_r][_c] == 0:
                            self.explorenull(_r, _c)
                        else:
                            self.click(_r, _c)
                            try:
                                self.auto_double_click(_r, _c)
                            except:
                                pass
            except IndexError:
                pass
            except Exception as e:
                messagebox.showinfo("Unexpected", ("function: check_onedir", f"error: {e}"))

    def double_click_valid(self, row, col):
        val = self.board[row][col]
        adj_flag_count = 0
        dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        for dir in dirs:
            _r = row-1 if 'n' in dir else row+1 if 's' in dir else row
            _c = col-1 if 'w' in dir else col+1 if 'e' in dir else col
            try:
                if type(self.buttons[_r][_c][0]) == Button and _r>=0 and _c>=0:
                    if self.buttons[_r][_c][1] == False:
                        adj_flag_count += 1
            except IndexError:
                pass
            except Exception as e:
                messagebox.showinfo("Unexpected", ("function: check_onedir", f"error: {e}"))
            if adj_flag_count>val:
                return False
        return True if val==adj_flag_count else False

    def showtile(self, r:int, c:int, img):
        """shows the tile on click"""
        lb = Label(self.frame, image=self.images[img], highlightthickness=0, bd=0)
        lb.grid(row=r, column=c)
        self.buttons[r][c][0].destroy()
        self.buttons[r][c].pop(0)
        self.buttons[r][c].insert(0, lb)
        self.buttons[r][c][1] = None

    def unhidemines(self, clicked_row:int, clicked_col:int):
        """shows all hidden+untouched mine tiles;\n
        tiles which are flaged and are mine remains as it is;\n
        the wrong flaged tile result in cross over them"""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]==-1: # mine tile
                    if i==clicked_row and j==clicked_col:
                        self.showtile(i, j, "tile_blast")
                    elif self.buttons[i][j][1] is True:
                        self.showtile(i, j, "tile_bomb")
                elif self.buttons[i][j][1] is False: # non mine tile flaged
                    self.showtile(i, j, "tile_cross")
        self.gameend(0)

    # null BFS explore
    def explorenull(self, row, col):
        prev_tiles = [(row, col)] 
        while len(prev_tiles) != 0:
            next_tiles = set()

            for r,c in prev_tiles:
                cell_val = self.board[r][c]
                # null cell
                if cell_val == 0:
                    self.showtile(r, c, "tile_0")
                    x = self._search_all_adj(r, c)
                    if x is not None:
                        next_tiles = next_tiles.union(x)

                # numbered cell
                elif cell_val != 0:
                    self.showtile(r, c, f"tile_{cell_val}")
                
                # unexpected condition
                else:
                    messagebox.showinfo("Unexpected",
                    ("Unexcepted behaviour in clicked_null function",
                    f"the cell {r},{c} value {cell_val} cant be able to convert to int"))

            # modification
            prev_tiles.clear()
            prev_tiles.extend(list(next_tiles))

    def _search_all_adj(self, r, c):
        dirs = ['n', 'e', 's', 'w', 'ne', 'se', 'sw', 'nw']
        neighbour_tiles = []
        for dir in dirs:
            x = self._search_one_adj(r, c, dir)
            if x is not None:
                neighbour_tiles.append(x)
        return neighbour_tiles if len(neighbour_tiles) != 0 else None

    def _search_one_adj(self, row, col, dir):
        _r = row-1 if 'n' in dir else row+1 if 's' in dir else row
        _c = col-1 if 'w' in dir else col+1 if 'e' in dir else col

        try:
            btn = self.buttons[_r][_c]
            if type(btn[0]) == Button and _r>=0 and _c>=0 and btn[1] is True:
                if self.board[_r][_c] in range(0, 9):
                    return (_r, _c)
        except IndexError:
            pass
        except Exception as e:
            messagebox.showinfo("Unexpected", ("function: check_onedir", f"error: {e}"))
        return None

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# images
class TileImages:
    def __init__(self, jsonfile):
        self.file = jsonfile

    def get_json2pydict(self):
        """returns result as dictionary"""
        f = open(self.file, 'r')
        data = f.read()
        return dict(json.loads(data))

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# check custom input
class custom_val():
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.names = ['Rows', 'Columns', 'Mines']
        self.approve = None
    
    def msg(self, message):
        messagebox.showerror("Invalid Input", (message))

    def check_val(self, x, name):
        try:
            x = int(x)
        except ValueError:
            self.msg((f"{name} input having inappropriate value"))
            self.approve = False
        except Exception as e:
            self.msg((e))
            self.approve = False
        else:
            if x>RawBoard.maxlen:
                self.msg((f"{name} input exceeded max value limit ie {RawBoard.maxlen}"))
                self.approve = False
            else:
                self.approve = True
    
    def check(self):
        vals = (self.rows, self.cols, self.mines)
        for i in range(3):
            self.check_val(vals[i], self.names[i])
            if self.approve is False:
                return self.approve
        if self.approve is True:
            return int(self.rows), int(self.cols), int(self.mines)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# game won window pop-up
class GamewonWindow():
    def create(self, time, clicks):
        self.top = Toplevel()
        self.top.title("Game Won!")
        self.top.iconbitmap(r'E:\ui based img\icon_boomer.ico')
        self.top.config(bg='black')
        self.top.resizable(0, 0)

        text1 = f"YOU WIN!"
        text2 = f"Congratulations on Winning Minesweeper!"
        text3 = f"Game Time: {time}"
        text4 = f"Number of Clicks: {clicks}"

        bgcol = '#0000AA'
        fgcol = 'white'
        pd = 10

        bg_fr = Frame(self.top, relief=RAISED, border=10, bg=bgcol)
        bg_fr.pack(fill=BOTH, expand=1, padx=10, pady=10)
        fnt = ('Imapct ', 10, 'bold')

        lb1 = Label(bg_fr, text=text1, bg=bgcol, fg=fgcol, justify=CENTER, wraplength=200, font=('Bubblegum', 20))
        lb2 = Label(bg_fr, text=text2, bg=bgcol, fg=fgcol, justify=CENTER, wraplength=200, font=fnt)
        lb3 = Label(bg_fr, text=text3, bg=bgcol, fg=fgcol, justify=CENTER, wraplength=200, font=fnt)
        lb4 = Label(bg_fr, text=text4, bg=bgcol, fg=fgcol, justify=CENTER, wraplength=200, font=fnt)

        lb1.pack(padx=pd, pady=(pd, pd//2))
        lb2.pack(padx=pd, pady=pd//2)
        lb3.pack(padx=pd, pady=pd//2)
        lb4.pack(padx=pd, pady=(pd//4, pd))

        self.top.mainloop()

    def destroy(self):
        try:
            self.top.destroy()
        except:
            pass

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# manipulation
def board_manipulate(row_clicked, col_clicked, board:list, mines):

    def _manipulate(r, c, val_change, board):
        dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        count = 0
        for dir in dirs:
            _r = r-1 if 'n' in dir else r+1 if 's' in dir else r
            _c = c-1 if 'w' in dir else c+1 if 'e' in dir else c
            try:
                if _r in range(0, len(board)) and _c in range(0, len(board[0])):
                    if board[_r][_c] == -1: # bomb tile
                        count += 1
                    if board[_r][_c] in range(1,9): # numbered tile other than 0
                        board[_r][_c] += val_change
            except IndexError:
                pass
            except Exception as e:
                messagebox.showinfo("Developer bad Exception Handling", "function: check_onedir", f"error: {e}")
        return board, count

    # first click mine
    if board[row_clicked][col_clicked] == -1:
        _r = row_clicked
        _c = col_clicked

    else: # first click safe
        _r,_c = mines[0]

    board, count = _manipulate(_r, _c, -1, board)
    board[_r][_c] = count
    return board

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# int to n digit strint
def to_strdigits(value:int, digits:int=2):
    num = str(abs(value))
    req_len = digits-len(num)
    req_len -= 1 if value<0 else 0
    if req_len<0:
        raise Exception(f"can\'t reduce the value:{value} lower than original digits")
    else:
        if req_len==0:
            return str(value)
        else:
            add = ''
            if value>=0:
                for _ in range(req_len):
                    add += '0'
                return add+num
            elif value<0:
                for _ in range(req_len):
                    add += '0'
                return '-'+add+num

