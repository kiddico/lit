#!/usr/bin/env python3


import sys
import curses
from utils import *
import itertools

import numpy as np
from numpy import intc

# makes numpy's repr send everything
np.set_printoptions(threshold=sys.maxsize)



def main():
    with open('log.txt','w') as out:
        scr = prep_curses()
        mx_c = 6
        colors_raw  = list(itertools.product(range(0,mx_c), range(0,mx_c), range(0,mx_c)))
        colors = [ tuple( int((x/(mx_c-1))*1000) for x in t ) for t in colors_raw ]

        try:
            for num, color in enumerate(colors):
                out.write('{},{}\n'.format(num, str(repr(color))))
                curses.init_color(1+num, *color)
                curses.init_pair(1+num, 1+num, 1+num)
        except Exception as e:
            out.write(str(e.args))

        max_value = len(colors)+1
        out.write('{}'.format(str(max_value)))
        curses.init_color(250, 0,0,0,)
        curses.init_color(251, 1000,1000,1000,)
        curses.init_pair(250, 250, 251)

        try:
            loop(scr, max_value)

        except Exception as e:
            pp(e)
            out.write(str(e.args))
        finally:
            scr.clear()
            curses.endwin()

def color_gen(max_value):
    for color in range(1, max_value):
        yield color<<8
    return 250<<8

def loop(scr, max_value):
    scr.clear()

    height, width = scr.getmaxyx()

    prefix = intc(100)

    scr.addstr(0, 0, ' ' * width * ( height-1 ), 1<<8 )
    try: scr.addstr(height-1, 0, ' '*width, 1<<8 )
    except: pass
    scr.refresh()
    with open('err.txt','w') as err:
        while(True):
            colors = color_gen(max_value)
            for y in range(2, height-1):
                for x in range(0, 36):
                    try:
                        scr.addstr(y, x, '▓', next(colors) )
                        #scr.addstr(y, x, ' ', next(colors) )
                        #scr.addstr(y, x, '▄', next(colors) )
                    except Exception as e:
                        pass
                        #err.write(str(repr(e.args)))
                        #err.write(str(repr(e)))

            scr.addstr(0,0,'{}x{}'.format(height,width), 250<<8)


            scr.refresh()
            scr.timeout(300)
            scr.getch()


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

