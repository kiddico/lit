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

def init_colors(color_map, centroids):
    cent_indexes = { cent:idx+1 for idx, cent in enumerate(centroids) }

    for cent, idx in cent_indexes.items():
        curses.init_color(idx, *cent)
        curses.init_pair(idx, idx, idx)
    attr_map = { color:cent_indexes[cent]<<8 for color, cent in color_map.items() }

    return attr_map

def resize_frame(cv2_frame, x_res, y_res, half_height=False):
    y_res = int(y_res/2) if half_height else y_res
    new_res = (x_res, y_res)
    return cv2.resize(cv2_frame, new_res)

def get_frame_paths(folder):
    return ['{}/{}'.format(folder, f) for f in listdir(folder) if isfile(join(folder, f))]


def clamp(frames):
    clamp_val = lambda x: int(int((x/255)*32)/32*1000)
    return [ tuple(tuple(tuple(clamp_val(value) for value in  cell[::-1]) for cell in row) for row in f) for  f in frames ]



def main():
    if len(argv) > 1:
        frame_paths = get_frame_paths(argv[1].replace('/',''))
    else:
        frame_paths = get_frame_paths('ghost_sample_2_frames')

    # Alright gents. Let's get some order in this chaos.
    # Turns out videos look like videos when the frames are in the right order.
    # Filenames need to follow the "<whatever>_f<frame number>.<extension>" rule.
    frame_paths.sort(key=lambda x: int(x.split('_f')[1].split('.png')[0]))
    try:
        scr = prep_curses()
        h, w = scr.getmaxyx()

        frames = tuple( resize_frame(cv2.imread(p, cv2.IMREAD_COLOR),w, h-1)  for p in frame_paths )
        clamped_cells = clamp(frames)
        color_map, centroids = kmeans( clamped_cells )
        attr_map = init_colors(color_map, centroids)


        for frame in clamped_cells:
            for y, row in enumerate(frame):
                for x, cell in enumerate(row):
                    scr.addstr(y, x, ' ', attr_map[cell])
            scr.refresh()
            # this will lock to ~24fps. Adjust accordingly.
            curses.napms(40)

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
