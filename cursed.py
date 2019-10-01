#!/usr/bin/env python3

import sys
import curses
from utils import *


import numpy as np

from numpy import full
from numpy import array
from numpy import arange

from numpy import intc
from numpy import random

# makes numpy's repr send it all
#np.set_printoptions(threshold=sys.maxsize)



def main():
    scr = prep_curses()
    color_map = prep_colors(colors, font_color)

    try:
        loop(scr, color_map)

    # Should get us back to normality. ~~s h o u l d~~
    except Exception as e:
        scr.clear()
        curses.endwin()
        pp(e)
    finally:
        scr.clear()
        curses.endwin()



render_times = []

def loop(scr, color_map):
    scr.clear()
    get_pair = curses.color_pair


    height, width = scr.getmaxyx()
    width = width-1

    max_value = len(color_map) - 1

    state = full( (height-1, width), 0, dtype=int)
    state = np.vstack((state, full((1, width), len(colors)-1, dtype=intc)))
    #state = random.randint(0,12,size=(height, width))

    #decay_idx = 0
    cache_len = 25
    decay_cache = generate_decay(height, width, 50, cache_len)

    # Array with reindexing values.
    # https://stackoverflow.com/q/26194389
    ordering = np.asarray([*list(range(1, height)),0])

    t = time.time
    with open('log.txt','w') as out:
        #try:
        while(True):
            out.write(' \n\n')

            start_time = t()
            out.write('\n\n---------------\n\n')
            out.write('Starting State\n\n')
            out.write(str(repr(state))+'\n\n')


            state = state[ordering]
            state[-1].fill(len(color_map)-1)
            #out.write('\n\n')
            out.write(str(repr(state))+'\n\n')
            state = state - decay_cache[ random.randint(0, cache_len) ]
            #state = [ row.clip(0) for row in state - decay_cache[ random.randint(0, cache_len) ] ]
            #if decay_idx == (len(decay_cache)-1):
            #    np.random.shuffle(decay_cache)
            #out.write(repr(state))
            scr.clear()
            for idy, row in enumerate(state):
                for idx, cell in enumerate(row):
                    if cell < 0 or cell > max_value:
                        #out.write('({},{}) from {} to {}\n\n'.format(idy, idx, cell, 0))
                        state[idy][idx] = 0
                    #scr.attroff(idy,idx, 112)
                    scr.chgat(idy, idx, color_map[cell])

            out.write(str(repr(state))+'\n')
            # Shoot for <60hz, assume we've got at least 4ms of processing (lol)
            scr.refresh()
            t1 = scr.inch(0,0)
            t2 = scr.inch(len(state)-1,0)

            out.write( '{0:b}\n'.format( t1 ))
            out.write( '{0:b}\n'.format( t1 >>8))
            out.write(  '{}\n\n'.format( t1 >>8))
            out.write( '{0:b}\n'.format( t2 ))
            out.write( '{0:b}\n'.format( t2 >>8))
            out.write(      '{}'.format( t2 >>8))
            #scr.timeout(300)
            #scr.getch()
            #render_times.append(t() - start_time)
            #raise Exception('        {}'.format(t() - start_time))
        #except:
        #    return


# Good lord this is ugly.
# also super slow....
def generate_decay(h, w, weight=50, cache_count=100):
    rint = random.randint
    masks = [ ]
    for x in range(0, cache_count):
        temp = []
        for row in range(0, h):
            sr = int( (row/h) * 100 )
            sr_diff = 2*(h-sr)
            rngs = [ rint(0, h + (2*weight)) for col in range(0,w) ]
            temp.append([ 0 if val< sr else ( 1 if val > sr_diff else 2 ) for val in rngs ])

        masks.append(np.array(temp, dtype=intc))

    # remove source row from decay mask.
    for mask in masks:
        mask[-1].fill(0)

    return masks

# Initialize all the things that curses.wrapper() does (but better)
def prep_curses():
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        scr.keypad(True)
        curses.curs_set(0)
        curses.start_color()
        return scr

# tuples of color_num, and RGB values
font_color = (99 , (500, 700, 1000))
colors = (
         (100, (0, 0, 0)),
         (101, (372, 0, 0)),
         (102, (529, 0, 0)),
         (103, (686, 0, 0)),
         (104, (843, 0, 0)),
         (105, (1000, 0, 0)),
         (106, (1000, 372, 0)),
         (107, (1000, 529, 0)),
         (108, (1000, 686, 0)),
         (109, (1000, 843, 0)),
         (110, (1000, 1000, 0)),
         (111, (1000, 1000, 529)),
         (112, (1000, 1000, 1000))
         )


# Our colors will go from 100 to 112, defaults are the no-no zone.
# 99 is used as a fg which can (for the most part) be read on our colors.
def prep_colors(colors, font_color):
    init_c = curses.init_color
    init_p = curses.init_pair

    init_c(font_color[0], *font_color[1])

    for color_num, color_values in colors:
        init_c(color_num, *color_values)
        init_p(color_num, 99, color_num)

    color_map = tuple(curses.color_pair(x) for x in range(100, 100+len(colors)))
    return color_map



if __name__ == '__main__':
    main()




# shame corner

#state = random.randint(0,12,size=(scr_y_dim, scr_x_dim-1))
#'·'
