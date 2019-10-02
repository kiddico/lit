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

# makes numpy's repr send everything
np.set_printoptions(threshold=sys.maxsize)



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
    width = width
    #width = width-1

    state = full( (height, width), 0, dtype=int)
    #state = np.vstack((state, full((1, width), len(colors)-1, dtype=intc)))

    # Pre Compute Decay Masks
    cache_len    = intc(10)
    decay_weight = intc(70)
    decay_index  = intc(0)
    decay_cache  = generate_decay(height, width, decay_weight, cache_len)

    # (prefix + cell_value)<<8 == color_pair(color_map(cell_value))
    prefix = intc(100)

    def_attr = prefix<<8
    for y in range(0, height):
        for x in range(0, width):
            #scr.chgat(y, x, def_attr)
            try:
                scr.addstr(y, x, ' ', (100)<<8 )
            except:
                pass
    scr.refresh()

    # Re-Ordering Array used to shift the state around.
    ordering = np.asarray([*list(range(1, height)),0])


    with open('log.txt', 'w') as out:

        t = time.time
        while(True):

            #state = np.roll(state, -1, axis=0)
            #state[-1].fill(len(color_map)-1)

            old_state = state.__deepcopy__(state)
            state = state - decay_cache[ decay_index ]
            decay_index = 0 if decay_index == cache_len-1 else decay_index + 1

            # Need to figure out the nump-y way to do this.
            for y in range(0, len(state)):
                clipped = state[y].clip(min=0)
                state[y] = clipped

            #state = np.roll(state, -1, axis=0)
            state = state[ordering]
            state[-1].fill(len(color_map)-1)

            # Calculate render mask, indexes that needs redrawn are true.
            render_mask = old_state != state

            #render_mask = np.roll(render_mask, -1, axis=0)
            #render_mask[-1].fill(True)


            #for y in range(0, height-1):
                #for x in range(0, width):
                    #if render_mask[y][x]:
                    #if state[y][x] != old_state[y+1][x]:
                    #    scr.chgat(y, x, (prefix + state[y][x])<<8)
                #if old_state[y] != state[y]:
                #if any([ x[0] != x[1] for x in zip(old_state[y], state[y]) ]) and y < 13:
                    #out.write('({},{}) of ({},{})\n'.format(y,x, height-1, width-1))
                    #out.write('{}\n'.format(str(repr(state))))
                    #out.write('{}\n'.format(str(repr(old_state))))
                    #out.write('\n\n')
                    #exit()
                    #else:
                        #scr.chgat(y, x, (prefix + old_state[y][x]) <<8)

            for y, row in enumerate(zip(state, render_mask)):
                for x, cell in enumerate(zip(*row)):
                    #out.write(f'{y}{x}\n')
                    #out.write('{}\n'.format(str(repr(row))))
                    #out.write('{}\n---------\n\n'.format(str(repr(cell))))
                    # If render mask @ cell is true...  do the things.
                    #if cell[1] :
                        #out.write('{0:x} : '.format(cell[0]))
                        #out.write('{0:b}\n'.format(cell[0]))
                        #scr.addstr(y, x, '{0:x}'.format(cell[0]), (prefix+cell[0])<<8 )
                        #scr.chgat(y, x, (prefix+cell[0])<<8)
                        #scr.chgat(y, x, (prefix+state[y][x])<<8)

                    #scr.chgat(y, x, (prefix+state[y][x])<<8)
                    if cell[1] :
                        try:
                            scr.addstr(y, x, ' ', (prefix+cell[0])<<8 )
                            #scr.addstr(y, x, '{0:x}'.format(cell[0]), (prefix+cell[0])<<8 )
                        except curses.error: pass
                            #out.write('{},{}\n'.format( y, x ))
                            #out.write('{},{}\n'.format( height-1, width-1 ))
                            #out.write(str(repr(state)))

                    #scr.chgat(y, x, (prefix+cell[0])<<8)

#            for y in range(0, len(state)):
#                for x in range(0, len(state[y])):

                    # If decay went below zero bring it back up.
                    #if state[y][x] < 0:
                    #    state[y][x] = 0

                    #if old_state[y][x] != state[y][x]:

            scr.refresh()
            scr.timeout(50)
            #out.write('{}/{}\n'.format(dem_right_writes, dem_wrong_writes))
            scr.getch()


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
            #rngs = [ rint(0, h + (2*weight)) for col in range(0,w) ]
            rngs = [ rint(0, h + (4*weight)) for col in range(0,w) ]
            temp.append([ 0 if val< sr else ( 1 if val > sr_diff else 2 ) for val in rngs ])
            #temp.append([ 0 if val< sr else ( 1 if val > sr_diff else 2 ) for val in rngs ])

        masks.append(np.array(temp, dtype=intc))

    # remove source row from decay mask.
    #for mask in masks:
    #    mask[-1].fill(0)

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
