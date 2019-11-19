#!/usr/bin/env python3

import cv2
import numpy
import curses
from utils import pp
from sys import exit, argv
from collections import namedtuple

from os import listdir
from os.path import isfile, join

def clamp_and_init(cells):
    # + 35 to brighten things up a bit.
    clamp = lambda x: int(int((x/255)*14)/14*255)
    clamped_cells = tuple(tuple(tuple(clamp(val) for val in cell[::-1]) for cell in row) for row in cells)
    clamped_colors = { x for y in clamped_cells for x in y }

    color_nums = {}
    if len(clamped_colors) <= 255:
        # For now just create the color number dictionary.
        # Each for loop is at most 255 iterations.
        for idx, color in enumerate(clamped_colors):
            color_nums[color] = (idx+1)<<8

        # Assign values for cells BEFORE creating color pairs
        # (this will take longer than either loop by 2 orders of magnitude.
        new_cells = tuple( tuple( color_nums[x] for x in row ) for row in clamped_cells )

        # Do the same loop again, this time only make the colors/pairs.
        # The longer we can delay this the less pronounced the artifacting will be.
        for idx, color in enumerate(clamped_colors):
            t_idx = idx + 1
            curses.init_color(t_idx, *color)
            curses.init_pair(t_idx, t_idx, t_idx)
        return new_cells
    else:
        # If it fails maybe we can try again with one less 'step' (16 -> 15 -> 14)
        # if we add it to the parameter list we can make it recursive.
        raise Exception('Cannot reduce color space with clamping method.')


def resize_frame(cv2_frame, x_res, y_res, half_height=True):
    y_res = int(y_res/2) if half_height else y_res
    new_res = (x_res, y_res)
    return cv2.resize(cv2_frame, new_res)

def get_frame_paths(folder):
    return ['{}/{}'.format(folder, f) for f in listdir(folder) if isfile(join(folder, f))]



resolution = namedtuple('resolution', ['y', 'x'])
def main():

    frame_paths = get_frame_paths('ghost_sample_2_frames')
    try:
        scr = prep_curses()
        height, width = scr.getmaxyx()
        sres = resolution(height, width)

        for frame_path in frame_paths:
            numpy_frame = cv2.imread(frame_path, cv2.IMREAD_COLOR)
            frame = resize_frame(numpy_frame, width, height-1, half_height = False)


            cells = clamp_and_init(frame)

            for y, row in enumerate(cells):
                for x, cell in enumerate(row):
                    scr.addstr(y, x, ' ', cell)
            scr.refresh()

    except Exception as e:
        scr.clear()
        curses.endwin()
        print('\n')
        pp(e.args)
        raise e
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
