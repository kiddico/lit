#!/usr/bin/env python3
import curses
import numpy
from utils import pp
from collections import namedtuple
from sys import exit
import cv2

# Aligns rgb values to multiples of 16.
# Initializes colors for those new values.
# Then returns 2 dim tuple with each cell being replaced by it's color pair value
# Said value is the same as calling color_pair for the color that we create.
# (all it does internally is bitshift left 8 times.
def clamp_and_init(cells):
    clamp = lambda x: int(int((x/255)*16)/16*255)
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
        # If it fails maybe we can try again with one less 'step' (16 -> 15 -> 14)
        # if we add it to the parameter list we can make it recursive.
        raise Exception('Cannot reduce color space with clamping method.')


def resize_image(cv2_image, x_res, y_res, half_height=True):
    y_res = int(y_res/2) if half_height else y_res
    new_res = (x_res, y_res)
    return cv2.resize(cv2_image, new_res)






def iterative_clamp(cells, align_on=16):
    clamp = lambda x: int(int((x/255)*align_on)/align_on*255)+5
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
        # If it fails maybe we can try again with one less 'step' (16 -> 15 -> 14)
        # if we add it to the parameter list we can make it recursive.
        raise Exception('Cannot reduce color space with clamping method.')


resolution = namedtuple('resolution', ['y', 'x'])
def main():
    image_in = cv2.imread('hats_on_hats_on_hats.jpg', cv2.IMREAD_COLOR)
    #image_in = numpy.load('60_80_hats.dump', allow_pickle=True)
    #ires = resolution(*image.shape[:2])
    try:
        scr = prep_curses()
        height, width = scr.getmaxyx()
        sres = resolution(height, width)
        image = resize_image(image_in, width, height-1, half_height = False)
        #image = resize_image(image_in, width-int(0.01 * width), height-int(0.01*height), half_height = False)
        #image = resize_image(image_in, width-int(0.1 * width), height-int(0.1*height), half_height = False)

        cells = clamp_and_init(image)
        #qprint(cells[0])
        #qprint(len(cells))
        #cprint(len(cells[0]))
        while True:
            for y, row in enumerate(cells):
                for x, cell in enumerate(row):
                    scr.addstr(y,x,' ', cell)
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
