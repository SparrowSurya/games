# functions-------------------------


# soduko solver-------------------------
def emptycells(sudoku, showerror:bool=True):
    empty = []
    for r in range(len(sudoku)):
        for c in range(len(sudoku[r])):
            if sudoku[r][c] == 0:
                empty.append((r, c))

    if showerror and len(empty)==0:
        raise EOFError("soduko dont have any empty cells")
    else:
        return tuple(empty)


def value_range(sudoku):
    val = [v for v in range(len(sudoku)+1)]
    return set(val)


def rowvalues(sudoku, row):
    val = [sudoku[row][col] for col in range(len(sudoku)) if sudoku[row][col] != 0]
    val.append(0)
    return set(val)


def columnvalues(sudoku, column):
    val = [sudoku[row][column] for row in range(len(sudoku)) if sudoku[row][column] != 0]
    val.append(0)
    return set(val)
    

def blockvalues(sudoku, row, column, block_dim):
    st_r = abs(int(row - row%block_dim[1]))
    st_c = abs(int(column - column%block_dim[0]))
    val = [0]

    for r in range(st_r, st_r+block_dim[1]):
        for c in range(st_c, st_c+block_dim[0]):
            if sudoku[r][c] != 0:
                val.append(sudoku[r][c])
    return set(val)


def cellpsbvalues(sudoku, row, column, block_dim):
    r = rowvalues(sudoku, row)
    c = columnvalues(sudoku, column)
    b = blockvalues(sudoku, row, column, block_dim)
    m = value_range(sudoku)

    val = r.union(c.union(b))
    val = m.difference(val)
    return val


# solving--------------------------------------------------
def solve_sudoku(sudoku:list, block_dim:tuple=(3,3)):
    """block_dim = (vertical height, horizontal width)"""

    # cheking module-----
    try:
        solution = copy.deepcopy(sudoku)
    except NameError:
        import copy
        solution = copy.deepcopy(sudoku)


    # fetching data-----
    _emptycells = emptycells(sudoku, True)

    _m = value_range(sudoku)

    # starting index
    id = 0

    # looping throught empty cells list
    while True:

        # getting row and column of id-----
        _r = _emptycells[id][0]
        _c = _emptycells[id][1]
        _p = tuple(cellpsbvalues(solution, _r, _c, block_dim))
        _v = solution[_r][_c]

        # looping throught values in current cell
        while True:

            _v += 1

            # if possible values list is empty
            if len(_p) == 0:
                solution[_r][_c] = 0
                id -= 1
                break

            # if possible values list is not empty
            else:

                # if value is possible
                if _v in _p:
                    solution[_r][_c] = _v
                    id += 1
                    break
                
                # if value is out of range
                elif _v not in _m:
                    solution[_r][_c] = 0
                    id -= 1
                    break
                    
                # ie current val is not a possible value and current value is in range
                else:
                    continue

        if id==len(_emptycells):
            break
        elif id==0 and solution[_emptycells[0][0]][_emptycells[0][1]] == 0:
            break
        else:
            continue

    return solution

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# display functions
def horizontal_rule(n:int, doubling:bool=0, linestyle:str='-', ending:str='\n'):
    """Doubling makes = instead -"""
    if linestyle=='=':
        line = '==='
    if linestyle=='-':
        line = '---'

    for i in range(n):
        if doubling:
            if i%doubling==0:
                print('+', end='')
        print(f'+{line}', end='')
    print('+', end='')
    if doubling:
        print('+', end='')
    print(ending, end='')

def vertial_line(array_1D:list=[], doubling:int=0, ending:str='\n'):
    """Doubling makes extra | \n
    if -1 then does for all\n
    if 0 then dont does\n
    else makes doublin after every given value"""
    for i in range(len(array_1D)):
        if doubling:
            if doubling==-1 or i%doubling==0:
                print('|', end='')
        print(f'| {array_1D[i]} ', end='')
    print('|', end='')
    if doubling:
        print('|', end='')
    print(ending, end='')

def grid(array_2D:list, doubling:tuple=(3, 3)):
    """doubling (r, c)"""
    r = len(array_2D)
    c = len(array_2D[0])
    for i in range(r):
        if doubling[0]:
            if i%doubling[0]==0:
                horizontal_rule(c, doubling[1], '=')
            else:
                horizontal_rule(c, doubling[1], '-')
        vertial_line(array_2D[i], doubling[1])
    if doubling[0]:
        if doubling[0]:
            horizontal_rule(c, doubling[1], '=')
        else:
            horizontal_rule(c, doubling[1], '-')

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# getting all rows input one by one
def rows_input(rows:int):
    print("NOTE: Enter 0 for empty cells")
    array_2D = []
    for i in range(rows):
        r = input(f"Enter row-{i+1} values (seperate by ','): ")
        x = list(map(lambda x: int(x), r.split(',')))
        array_2D.append(x)
    return array_2D
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# asking response
def response():
    while True:
        temp = input("again?(y/n)... ")
        if temp=='y':
            return True
        elif temp=='n':
            return False
        else:
            print("Invalid Input")
            return response()
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#

def main(): 
    print("#-----#-----#-----Solve Soduko-----#-----#-----#")

    while True:
        try:
            sdk = rows_input(9)
            solution = solve_sudoku(sdk)
            print("Solution:\n")
            grid(solution, (3, 3))
            print('\n', end='')
            again = response()
            if again:
                continue
            else:
                break
        except Exception as e:
            print("Error:", e)
        finally:
            continue

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
if __name__ == '__main__':
    main()
