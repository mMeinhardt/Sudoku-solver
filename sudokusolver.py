#!/usr/bin/python3

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame as pg
import copy
import time
import sys



OFFSETX = 55
OFFSETY = 55

def read_sudoku_from_file(filename):
    errormsg = filename + ' is not a valid Sudoku-File'
    sudokufile = open(filename, 'r')
    sudoku = []
    lines = sudokufile.readlines()
    if len(lines) > 9:
        raise IOError(errormsg)
    i = 0

    for line in lines:
        sudokuarr = line.split(', ')
        if len(sudokuarr) > 9:
            raise IOError(errormsg)
        sudokuarr[8] = sudokuarr[8][0]
        sudokuline = []
        for digit in sudokuarr:
            if (not digit.isdigit()):
                raise IOError(errormsg)
            sudokuline.append(int(digit))
        sudoku.append(sudokuline)
    return sudoku



def is_valid(sudoku, x, y, num):
    # Checking Line
    for i in range(0, 9):
        if num == sudoku[y][i]:
            return False
    # Checking Row
    for i in range(0, 9):
        if num == sudoku[i][x]:
            return False
    columnstart = (x // 3) * 3
    rowstart = (y // 3) * 3
    for i in range(rowstart, rowstart+3):
        for j in range(columnstart, columnstart+3):
            if num == sudoku[i][j]:
                return False
    return True

def get_next_number(sudoku):
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku[i][j] == 0:
                return [i, j]
    return [-1, -1]

def solve_sudoku(sudoku, rendersudoku, visualize):
    nextnum = get_next_number(sudoku)
    if nextnum[0] == -1 and nextnum[1] == -1:
        return True
    y = nextnum[0]
    x = nextnum[1]
    for i in range(1, 10):
        if visualize:
            rendersudoku[y][x] = i
            update()
            render(rendersudoku)
        if is_valid(sudoku, x, y, i):
            sudoku[y][x] = i
            if solve_sudoku(sudoku, rendersudoku, visualize):
                return True
            sudoku[y][x] = 0
    rendersudoku[y][x] = 0
    return False

def main():
    nooptions = False
    if len(sys.argv) == 1:
        print('Usage: ./sudokusolver.py [-v] [FILE]')
        exit()
    if len(sys.argv) == 2:
        nooptions = True
    visualize = False
    if str(sys.argv[1]) == '-v':
        visualize = True

    filename = ''
    if nooptions:
        filename = sys.argv[1]
    else:
        filename = sys.argv[2]

    sudoku = read_sudoku_from_file(filename)
    rendersudoku = copy.deepcopy(sudoku)
    if visualize:
        pg.init()
        pg.font.init()
        screen = pg.display.set_mode((504, 504))
        pg.display.set_caption('Sudoku solver')
        render(rendersudoku)
        time.sleep(0.20)
    if solve_sudoku(sudoku, rendersudoku, visualize):
        if not visualize:
            for i in sudoku:
                print(i)
    else:
        print('No Solution!')
    while True and visualize:
        update()
        render(rendersudoku)

def render(rendersudoku):
    pg.display.get_surface().fill((0, 0, 0))
    grid = pg.image.load('res/sudoku_blank.png')
    pg.display.get_surface().blit(grid, (0, 0))
    myfont = pg.font.SysFont(pg.font.get_default_font(), 32)
    i = 0
    j = 0
    for line in rendersudoku:
        for num in line:
            num_display = myfont.render(str(num), False, (0, 0, 0))
            pg.display.get_surface().blit(num_display, (i*OFFSETX+25, j*OFFSETY+15))
            i = i+1
        j = j+1
        i = 0
    pg.display.flip()

def update():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    clock = pg.time.Clock()
    clock.tick(30)



if __name__ == "__main__":
    main()

