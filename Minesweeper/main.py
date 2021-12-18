from tkinter import *
from game_functools import *
from game_ui_layout import *


#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# setup
root = Tk()
root.title("Minesweeper")
root.iconbitmap(r'light_theme\icon.ico')
root.resizable(0, 0)


img = TileImages("images_path.json").get_json2pydict()
images = {k:PhotoImage(file=v) for k,v in img.items()}
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# constant/variables

# default
DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_MINES = 8, 8, 8

# easy
EASY_ROWS, EASY_COLS, EASY_MINES = 7, 10, 10

# medium
MEDIUM_ROWS, MEDIUM_COLS, MEDIUM_MINES = 11, 17, 35

# hard
HARD_ROWS, HARD_COLS, HARD_MINES = 16, 24, 75

MINES_LOC = []
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# creating ui templates
main_fr = MainFrame(root)
main_fr.pack()

stats_fr = StatsFrame(main_fr.id_var())
content_fr = ContentFrame(main_fr.id_var())

mine_lb = MinesLabel(stats_fr.id_var())
timer_lb = TimerLabel(stats_fr.id_var())
emoji_btn = QuickStartButton(stats_fr.id_var(), images)

mine_lb.pack()
timer_lb.pack()
emoji_btn.pack()

tiles_fr = TilesFrame(content_fr.id_var())
tiles_fr.pack()

btn_fr = tiles_fr.id_var()

custom_fr = CustomFrame(main_fr.id_var())
custom_wid_fr = CustomFrameWidgets(custom_fr.id_var())


# display mines/timer
mine_display = MinesCountDisplay(mine_lb.id_var())
timer_display = Timer(timer_lb.id_var())

# task manager
task_manager = TaskManager(mine_display, timer_display, emoji_btn)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# functions

# ui loading/unloading functions-----#-----#-----#-----#-----#-----#

# game platform-----
def game_platform(place:bool):
    if place:
        stats_fr.pack()
        content_fr.pack()
    else:
        stats_fr.forget()
        content_fr.forget()

# custom game platform-----
def custom_platform(place:bool):
    if place:
        custom_fr.pack()
        custom_wid_fr.clear_entries()
        custom_wid_fr.pack()
    else:
        custom_fr.forget()
        custom_wid_fr.forget()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# creating tiles-----
def change_default(nrow, ncol, nmines):
    global DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_MINES
    DEFAULT_ROWS = nrow
    DEFAULT_COLS = ncol
    DEFAULT_MINES = nmines

def startgame_reset():
    global tile_board
    try:
        tile_board.reset()
    except NameError:
        pass
    task_manager.destroy_winWIN()
    game_platform(1)
    custom_platform(0)
    task_manager.reset()
    emoji_btn.reset()

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# start game
def startgame(Rows:int=0, Columns:int=0, Mines:int=0):
    global DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_MINES, MINES_LOC, tile_board

    # clearing modified changes
    startgame_reset()

    # setting values
    rows = Rows if Rows else DEFAULT_ROWS
    columns = Columns if Columns else DEFAULT_COLS
    mines = Mines if Mines else DEFAULT_MINES

    # changing default row col mine vals
    change_default(rows, columns, mines)

    # generating
    rb = RawBoard(rows, columns, mines)
    gb = rb.generate()
    
    MINES_LOC = rb.bomb_tiles
    gameboard = GameBoard(gb).translate()
    tile_board = TileBoard(root, task_manager, gameboard, images, btn_fr, MINES_LOC)
    tile_board.create(rows, columns)
    mine_display.setcount(mines)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# play again
def playagain(rows, cols, mines):
    task_manager.reset_buttons(tile_board)
    startgame(rows, cols, mines)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# menu functions

# file menu functions-----#-----#-----#-----#-----#-----#

# custom new game
def New_filemenu():
    task_manager.pause_timer()
    custom_platform(1)
    game_platform(0)

# exit custom
def exit_custom():
    custom_platform(0)
    game_platform(1)
    task_manager.resume_timer()

def submit_custom():
    r,c,m = custom_wid_fr.get_entries()
    val = custom_val(r,c,m).check()
    if type(val) is tuple:
        startgame(val[0], val[1], val[2])

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# menus
Game_menu = Menu(root)

# declaring items in sdk_menu ribbon-----
file_menu = Menu(Game_menu, tearoff=False)
options_menu = Menu(Game_menu, tearoff=False)
help_menu = Menu(Game_menu, tearoff=False)

# adding commands in file_menu-----
file_menu.add_command(label='New', command=New_filemenu)
file_menu.add_separator()
file_menu.add_command(label='Easy', command=lambda : playagain(EASY_ROWS, EASY_COLS, EASY_MINES))
file_menu.add_command(label='Medium', command=lambda : playagain(MEDIUM_ROWS, MEDIUM_COLS, MEDIUM_MINES))
file_menu.add_command(label='Hard', command=lambda : playagain(HARD_ROWS, HARD_COLS, HARD_MINES))
file_menu.add_separator()
file_menu.add_command(label='Quit', command=root.quit)

# adding commands in option_menu-----
options_menu.add_checkbutton(label='*Mute')
options_menu.add_command(label='*Sound')

# adding commands in help_menu-----
help_menu.add_command(label='*About')

# displaying file and edit menu-----
Game_menu.add_cascade(label="File", menu=file_menu)
Game_menu.add_cascade(label="Options", menu=options_menu)
Game_menu.add_cascade(label="Help", menu=help_menu)

# displaying menubar in the root-----
root.config(menu=Game_menu)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# post configurations

back_btn, submit_btn = custom_wid_fr.id_var_btn()
back_btn.config(command=exit_custom)
submit_btn.config(command=submit_custom)
emoji_btn.id_var().config(command=lambda: playagain(DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_MINES))

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# start main
game_platform(1)
startgame(DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_MINES)


if __name__ == '__main__':
    root.mainloop()

#-----#-----#-----END-----#-----#-----#