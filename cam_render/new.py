#!/usr/bin/env python3
import curses
import numpy
from utils import pp
from collections import namedtuple
from sys import exit

# Aligns rgb values to multiples of 16.
# Initializes colors for those new values.
# Then returns 2 dim tuple with each cell being replaced by it's color pair value
# Said value is the same as calling color_pair for the color that we create.
# (all it does internally is bitshift left 8 times.
def clamp_and_init(cells):
    clamp = lambda x: int(int((x/255)*16)/16*255)
    clamped_cells = tuple(tuple(tuple(clamp(val) for val in cell[::-1]) for cell in row) for row in cells)
    clamped_colors = { x for y in clamped_cells for x in y }

    # Prototype used to derive above
    #clamped_colors = set()
    #clamped_cells = []
    # construct the new clamped multi dim array on the fly
    # make and append to temp list, add to master list at the end of row
    # I know it's ugly... shut up.
    #for y, row in enumerate(cells):
    #    tmp = []
    #    for x, cell in enumerate(row):
    #        col = tuple( int(int((val/255)*16)/16*255) for val in cell[::-1] )
    #        clamped_colors.add(col)
    #        tmp.append(col)
    #    clamped_cells.append(tmp)

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

    image = numpy.load('60_80_hats.dump', allow_pickle=True)
    ires = resolution(*image.shape[:2])
    try:
        scr = prep_curses()
        height, width = scr.getmaxyx()
        sres = resolution(height, width)

        cells = clamp_and_init(image)
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





def ignore_me():
    # Transform the ndarray to a flat (1 dim) tuple. 1 dim not including the rgb val tuple.
    flat = tuple( tuple(x) for y in cells for x in y )
    # Align rgb to every 16 values (reduces the color space)
    clamped = [ tuple( int(int((val/255)*16)/16*255) for val in cell ) for cell in flat ]
    colors = set( clamped )

    # Now we need to map the color to curses colors, and then to a color pair.
    # For now the fg and bg are going to be the same. We can do 1/2 height chars later.
    # we aren't allowed to touch color 0, so we'll do 1..255.
    color_nums = {}
    if len(colors) <= 255:
        for idx, color in enumerate(colors):
            # offset color index to align to 1..255
            t_idx = idx + 1
            curses.init_color(t_idx, *color)
            curses.init_pair(t_idx, t_idx, t_idx)
            color_nums[color] = t_idx<<8
        # return a tuple with the color index instead of the color values
        return color_nums, 
        #return tuple( color_nums[tup]<<8 for tup in clamped )
    else:
        raise Exception('Cannot reduce color space with clamping method.')


