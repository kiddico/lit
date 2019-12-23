#!/usr/bin/env python3

import cv2
import numpy
import curses
from utils import pp
from sys import exit, argv
from collections import namedtuple

from os import listdir
from os.path import isfile, join

from kmeans import kmeans


# Iterative clamp is expensive, so I'll stick to constant alignment intervals during video playback.
def clamp_and_init(cells):
    #clamp = lambda x: int(int((x/255)*24)/24*1000)
    clamp = lambda x: int(int((x/255)*14)/14*1000)
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


def resize_frame(cv2_frame, x_res, y_res, half_height=False):
    y_res = int(y_res/2) if half_height else y_res
    new_res = (x_res, y_res)
    return cv2.resize(cv2_frame, new_res)

def get_frame_paths(folder):
    return ['{}/{}'.format(folder, f) for f in listdir(folder) if isfile(join(folder, f))]


def clamp(frames):
    clamp = lambda x: int(int((x/255)*32)/32*1000)
    #clamp = lambda x: int(int((x/255)*32)/32*1000)

    clamped_frames = []
    clamped_colors = set()
    for cells in frames:
        clamped_frames.append(tuple(tuple(tuple(clamp(val) for val in cell[::-1]) for cell in row) for row in cells))
        clamped_colors |= { x for y in clamped_cells for x in y }

    return clamped_frames, clamped_colors

def color_init():
    pass

def main():
    if len(argv) > 1:
        frame_paths = get_frame_paths(argv[1].replace('/',''))
    else:
        frame_paths = get_frame_paths('ghost_sample_2_frames')


    ####
    #
    # dict (clamped_color) -> attribute_number
    # iterate over clamped_cells
    #     change val -> dict(cell_value)
    #

    #kmeans( (cv2.imread(frame_paths[0], cv2.IMREAD_COLOR)) )
    # clamped_cells, clamped_colors = clamp()
    # [cells]      , set(colors)
    # kmeans(
    try:
        scr = prep_curses()
        h, w = scr.getmaxyx()
        frames = tuple( resize_frame(cv2.imread(p, cv2.IMREAD_COLOR),w, h-1)  for p in frame_paths )
        ccells, ccolors = clamp(frames)


        for frame in frames:
            cells = clamp_and_init(frame)

            for y, row in enumerate(cells):
                for x, cell in enumerate(row):
                    scr.addstr(y, x, ' ', cell)
            scr.refresh()
            #curses.napms(2000)

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
