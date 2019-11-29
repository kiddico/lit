#!/usr/bin/env python3

import cv2
import numpy
import curses
from utils import pp
from sys import exit, argv
from collections import namedtuple


def resize_image(cv2_image, x_res, y_res, half_height=True):
    y_res = int(y_res/2) if half_height else y_res
    new_res = (x_res, y_res)
    return cv2.resize(cv2_image, new_res)


def iterative_clamp(cells, align_on=20):
    clamp = lambda x: int(int((x/255)*align_on)/align_on*1000)
    clamped_cells = tuple(tuple(tuple(clamp(val) for val in cell[::-1]) for cell in row) for row in cells)
    clamped_colors = { x for y in clamped_cells for x in y }

    color_nums = {}
    if len(clamped_colors) <= 255:
        for idx, color in enumerate(clamped_colors):
            # offset color index to align to 1..255
            t_idx = idx + 1
            curses.init_color(t_idx, *color)
            curses.init_pair(t_idx, t_idx, t_idx)
            color_nums[color] = t_idx<<8
        # return a two dim thing with the values already at the calculated attribute
        return tuple( tuple( color_nums[x] for x in row ) for row in clamped_cells )

    else:
        # If we go below 4 alignment steps... there's a problem.
        # Otherwise recurse our way into oblivion.
        if align_on > 4:
            return iterative_clamp(cells, align_on=align_on-1)
        raise Exception('Cannot reduce color space with clamping method.')


def main():
    if len(argv) > 1:
        image_name = argv[1]
    else:
        image_name = 'the_great_wave.jpg'
    image_in = cv2.imread(image_name, cv2.IMREAD_COLOR)

    try:
        scr = prep_curses()
        height, width = scr.getmaxyx()
        image = resize_image(image_in, width, height-1, half_height = False)

        cells = iterative_clamp(image)
        while True:
            for y, row in enumerate(cells):
                for x, cell in enumerate(row):
                    scr.addstr(y,x,' ', cell)
            scr.refresh()

    except:
        scr.clear()
        curses.endwin()
    finally:
        scr.clear()
        curses.endwin()



def prep_curses():
    scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    scr.keypad(True)
    curses.curs_set(0)
    curses.start_color()
    return scr

def qprint(strang):
    cprint(strang, quick=True)

def cprint(strang, quick=False):
    global scr
    curses.endwin()
    try:
        pp(strang)
    except:
        pp(str(repr(strang)))
    if not quick:
        input('↵!')
    scr = prep_curses()

if __name__ == '__main__':
    main()
