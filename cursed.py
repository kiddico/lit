#!/usr/bin/env python3


import sys
import curses
from utils import *


import numpy as np
from numpy import intc

# makes numpy's repr send everything
np.set_printoptions(threshold=sys.maxsize)



def main():
    scr = prep_curses()
    max_value = prep_colors(colors, font_color)
    try:
        loop(scr, max_value)

    except Exception as e:
        pp(e)
        pass
    finally:
        # Should get us back to normality.
        # ~~ s h o u l d ~~
        scr.clear()
        curses.endwin()

def loop(scr, max_value):
    scr.clear()

    height, width = scr.getmaxyx()
    state = np.full( (height, width), 0, dtype=int)

    # Pre Compute Decay Masks
    cache_len    = 50
    decay_weight = 70
    scr.addstr(0,0,'Computing {} decay masks...'.format(cache_len), 98<<8)
    scr.refresh()
    decay_cache  = generate_decay(
            height,
            width,
            decay_weight,
            cache_len)
    decay_index  = intc(0)

    # Common values for attrs cached. Bitshift outpaces an array index deref by ~2x.
    # (prefix + cell_value)<<8 == color_pair(color_map(cell_value))
    prefix = intc(100)

    # Pre-fill Frame
    scr.addstr(0, 0, ' ' * width * ( height-1 ), prefix<<8 )
    try: scr.addstr(height-1, 0, ' '*width, 98<<8 )
    except: pass
    scr.refresh()

    roll = np.roll

    while(True):

        old_state = state.__deepcopy__(state)
        state = state - decay_cache[ decay_index ]
        decay_index = 0 if decay_index == cache_len-1 else decay_index + 1

        # Need to figure out the nump-y way to do this.
        for y in range(0, len(state)):
            clipped = state[y].clip(min=0)
            state[y] = clipped

        state = roll(state, -1, axis=0)
        state[-1].fill(max_value)

        # Calculate render mask, indexes that needs redrawn are true.
        render_mask = old_state != state


        for y, row in enumerate(zip(state[:-1], render_mask[:-1])):
            if any(row[1]):
                for x, cell in enumerate(zip(*row)):
                    if cell[1] :
                        scr.addstr(y, x, '▄', (prefix+cell[0])<<8 )

        scr.refresh()
        scr.timeout(30)
        scr.getch()



def generate_decay(h, w, weight=50, cache_count=100):
    rint = np.random.randint
    arr  = np.array
    masks = [ ]
    for x in range(0, cache_count):
        temp = []
        for row in range(0, h):
            sr = int( (row/h) * 100 )
            sr_diff = 2*(h-sr)
            rngs = [ rint(0, h + (4*weight)) for col in range(0,w) ]
            temp.append([ 0 if val< sr else ( 1 if val > sr_diff else 2 ) for val in rngs ])
        masks.append( arr(temp, dtype=intc) )

    return masks


# Our colors are offset from 100. We want to avoid all the default colors/pairs.
# 99 is used as a fg which can (for the most part) be read on our colors.
# Pair 98 is black on white (Good for log messages in the bottom row.
def prep_colors(colors, font_color):
    init_c = curses.init_color
    init_p = curses.init_pair

    # The on-all-color font fg.
    init_c(font_color[0], *font_color[1])

    ## Experimenting with half height block as fg character for 2x vertical resolution.
    ## This guy : '▄'

    # For now make the max val just have 2x max
    cn = colors[0][0]
    init_c(cn, *colors[0][1])
    init_p(cn, cn, cn)
    # For fg == 1 lower.
    # BG is "actual" value.
    for color_num, color_values in colors[1:]:
        init_c(color_num, *color_values)
        init_p(color_num, color_num, color_num-1)

    # Real black on white even with weird terminal colors/themes.
    init_c(98, 0,0,0)
    init_p(98, 98, colors[-1][0])

    return intc(len(colors)-1)


# Tuples of color_num, and RGB values
# RGB values scale from 0-1000. ff->255->1000
font_color = (99 , (500, 700, 1000))
colors = (
        (100, (0, 0, 0)),
        (101, (243, 0, 0)),
        (102, (372, 0, 0)),
        (103, (529, 0, 0)),
        (104, (686, 0, 0)),
        (105, (843, 0, 0)),
        (106, (909, 0, 0)),
        (107, (1000, 0, 0)),
        (108, (1000, 372, 0)),
        (109, (1000, 227, 0)),
        (110, (1000, 529, 0)),
        (111, (1000, 686, 0)),
        (112, (1000, 843, 0)),
        (113, (1000, 1000, 0)),
        (114, (1000, 1000, 529)),
        (115, (1000, 1000, 1000)),
        )


# Initialize all the things that curses.wrapper() does.
# Avoids wrapping our event loop in a function call.
def prep_curses():
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        scr.keypad(True)
        curses.curs_set(0)
        curses.start_color()
        return scr


if __name__ == '__main__':
    main()

