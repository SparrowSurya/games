from tkinter import *

if __name__ == '__main__':
    from game_functools import *

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class frame variables
class FR:
    bgcol = '#C0C0C0'
    padd = 10
    bd = 4
    pad = 4
    wd = 3
    cstmbg='#C0C0C0'

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class main frame
class MainFrame:
    def __init__(self, root:Tk):
        self.root = root
        self._create()

    def _create(self):
        self.main_fr = Frame(self.root, border=FR.bd, relief=RAISED, bg=FR.bgcol)

    def pack(self):
        self.main_fr.pack(fill=BOTH, expand=1)

    def forget(self):
        self.main_fr.pack_forget()
    
    def id_var(self):
        return self.main_fr

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class stats frame
class StatsFrame:
    def __init__(self, frame:Frame):
        self.frame = frame
        self._create()

    def _create(self):
        self.stats_fr = Frame(self.frame, border=FR.bd, relief=SUNKEN, height=60, bg=FR.bgcol)

    def pack(self):
        self.stats_fr.pack(fill=X, padx=FR.padd, pady=(FR.padd, FR.padd//2))

    def forget(self):
        self.stats_fr.pack_forget()
    
    def id_var(self):
        return self.stats_fr

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class content frame
class ContentFrame:
    def __init__(self, frame:Frame):
        self.frame = frame
        self._create()

    def _create(self):
        self.content_fr = Frame(self.frame, border=FR.bd, relief=SUNKEN, height=60, bg=FR.bgcol)

    def pack(self):
        self.content_fr.pack(fill=BOTH, expand=True, padx=FR.padd, pady=(FR.padd//2, FR.padd))

    def forget(self):
        self.content_fr.pack_forget()
    
    def id_var(self):
        return self.content_fr

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class mines label
class MinesLabel:
    font = ('Digital Dismay', 20, 'bold')
    fgcol = 'red'
    bgcol = 'black'
    def __init__(self, frame:Frame):
        self.frame = frame
        self._create()

    def _create(self):
        self.mines_lb = Label(self.frame, text='000', width=FR.wd, justify=CENTER, bg=self.bgcol, fg=self.fgcol, font=self.font)

    def pack(self):
        self.mines_lb.pack(side=LEFT, fill=Y, padx=FR.pad, pady=FR.pad//2, anchor='w')

    def forget(self):
        self.mines_lb.pack_forget()
    
    def id_var(self):
        return self.mines_lb
    
    def display(self, txt:str):
        self.mines_lb.config(text=txt)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class timer label
class TimerLabel:
    font = ('Digital Dismay', 20, 'bold')
    fgcol = 'red'
    bgcol = 'black'

    def __init__(self, frame:Frame):
        self.frame = frame
        self._create()

    def _create(self):
        self.timer_lb = Label(self.frame, text='000', width=FR.wd, justify=CENTER, bg=self.bgcol, fg=self.fgcol, font=self.font)

    def pack(self):
        self.timer_lb.pack(side=RIGHT, fill=Y, padx=FR.pad, pady=FR.pad//2, anchor='e')

    def forget(self):
        self.timer_lb.pack_forget()
    
    def id_var(self):
        return self.timer_lb
    
    def display(self, txt:str):
        self.timer_lb.config(text=txt)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class quick start button
class QuickStartButton:
    def __init__(self, frame:Frame, images:dict):
        self.frame = frame
        self.images = images
        self._create()
    
    def _create(self):
        self.quick_start_btn = Button(self.frame, image=self.images['face_smile'], border=1)
    
    def pack(self):
        self.quick_start_btn.pack(anchor='center', pady=FR.pad, padx=FR.pad)
    
    def forget(self):
        self.quick_start_btn.pack_forget()
    
    def id_var(self):
        return self.quick_start_btn
    
    def display(self, stats:str='smile' or 'sad' or 'win'):
        if stats=='smile':
            self.quick_start_btn.config(image=self.images['face_smile'])
        elif stats=='sad':
            self.quick_start_btn.config(image=self.images['face_sad'])
        elif stats=='win':
            self.quick_start_btn.config(image=self.images['face_won'])
        else:
            messagebox.showerror("Invalid Literal",
             "arg stats takes only 3 input values as string: 'smile', 'sad' or 'win'")

    def reset(self):
        self.quick_start_btn.config(image=self.images['face_smile'])

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class tiles frame
class TilesFrame:
    def __init__(self, frame:Frame):
        self.frame = frame
        self._create()

    def _create(self):
        self.tiles_fr = Frame(self.frame)

    def pack(self):
        self.tiles_fr.pack(anchor=CENTER)

    def forget(self):
        self.tiles_fr.pack_forget()
    
    def id_var(self):
        return self.tiles_fr

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class non game frame
class NonGameFrame:
    def __init__(self, frame:Frame):
        self.frame = frame
        self._create()

    def _create(self):
        self.non_game_fr = Frame(self.frame, border=FR.bd, relief=SUNKEN, bg=FR.bgcol)

    def pack(self):
        self.non_game_fr.pack(fill=BOTH, padx=FR.padd, pady=FR.padd)

    def forget(self):
        self.non_game_fr.pack_forget()
    
    def id_var(self):
        return self.non_game_fr

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class custom frame
class CustomFrame:
    def __init__(self, frame:Frame):
        self.frame = frame
        self._create()

    def _create(self):
        self.custom_fr = Frame(self.frame, relief=SUNKEN, border=10, bg=FR.cstmbg)

    def pack(self):
        self.custom_fr.pack(fill=BOTH, padx=FR.padd, pady=FR.padd, expand=1, ipadx=10, ipady=10)

    def forget(self):
        self.custom_fr.pack_forget()
    
    def id_var(self):
        return self.custom_fr

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# class custom frame widgets
class CustomFrameWidgets:
    def __init__(self, frame:Frame):
        self.frame = frame
        self._create()
    
    def _create(self):
        self.row_lb = Label(self.frame, text='Rows:', bg=FR.cstmbg)
        self.col_lb = Label(self.frame, text='Columns:', bg=FR.cstmbg)
        self.mine_lb = Label(self.frame, text='Mines:', bg=FR.cstmbg)

        self.row_en = Entry(self.frame, border=4)
        self.col_en = Entry(self.frame, border=4)
        self.mine_en = Entry(self.frame, border=4)

        self.back_btn = Button(self.frame, text='Back', border=4)
        self.submit_btn = Button(self.frame, text='Create', border=4)
    
    def pack(self):
        self.row_lb.pack(pady=(10, 5), padx=10)
        self.row_en.pack(pady=(5, 0), padx=10)

        self.col_lb.pack(pady=(10, 5), padx=10)
        self.col_en.pack(pady=(5, 0), padx=10)

        self.mine_lb.pack(pady=(10, 5), padx=10)
        self.mine_en.pack(pady=(5, 0), padx=10)

        self.back_btn.pack(side=LEFT, padx=(10, 0), pady=(20, 10))
        self.submit_btn.pack(side=RIGHT, padx=(0, 10), pady=(20, 10))

    def forget(self):
        self.row_lb.pack_forget()
        self.col_lb.pack_forget()
        self.mine_lb.pack_forget()

        self.row_en.pack_forget()
        self.col_en.pack_forget()
        self.mine_en.pack_forget()

        self.back_btn.pack_forget()
        self.submit_btn.pack_forget()

    def clear_entries(self):
        self.row_en.delete(0, END)
        self.col_en.delete(0, END)
        self.mine_en.delete(0, END)
    
    def get_entries(self):
        return (self.row_en.get(), self.col_en.get(), self.mine_en.get())
    
    def id_var_btn(self):
        return (self.back_btn, self.submit_btn)
    
    def id_var_lb(self):
        return (self.row_lb, self.col_lb, self.mine_lb)
    
    def id_var_en(self):
        return (self.row_en, self.col_en, self.mine_en)

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# testing
if __name__ == '__main__':
    root = Tk()
    root.title('test ui')

    img = TileImages("images_path.json").get_json2pydict()
    images = {k:PhotoImage(file=v) for k,v in img.items()}

    main_fr = MainFrame(root)
    main_fr.pack()

    stats_fr = StatsFrame(main_fr.id_var())
    stats_fr.pack()

    content_fr = ContentFrame(main_fr.id_var())
    content_fr.pack()

    mine_lb = MinesLabel(stats_fr.id_var())
    mine_lb.pack()

    timer_lb = TimerLabel(stats_fr.id_var())
    timer_lb.pack()

    emoji_btn = QuickStartButton(stats_fr.id_var(), images)
    emoji_btn.pack()

    tiles_fr = TilesFrame(content_fr.id_var())
    tiles_fr.pack()

    btn_fr = tiles_fr.id_var()
    for i in range(5):
        for j in range(5):
            bt = Button(btn_fr, text=f'r{i}c{j}', height=2, width=4)
            bt.grid(row=i, column=j)

    root.mainloop()