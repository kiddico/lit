#!/usr/bin/env python3

import curses
from sys import exit
from curses import wrapper, color_pair
from pprint import PrettyPrinter as PP
pp = PP(indent=4).pprint

from time import time as t


def main(scr, c_range):
    scr.clear()
    get_pair = curses.color_pair

    while(True):
        for idx, c_num in enumerate(range(c_range[0], c_range[1])):
            scr.addstr(idx, 0,
                        '{:<3}:{:>4}'.format(idx, c_num),
                        get_pair(c_num)
                        )

        scr.refresh()
        #scr.getkey()

def initatron_5000():
    try:
        # Initialize all the things that curses.wrapper() does.
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        scr.keypad(True)
        curses.curs_set(0)
        curses.start_color()

        # Our colors will go from 100 to 112, defaults are the no-no zone.
        # 99 is used as a fg which can (for the most part) be read on our colors.
        #curses.init_color(99, 500, 700, 1000)
        for color_num, color_values in colors:
            curses.init_color(color_num, *color_values)
            curses.init_pair(color_num, 99, color_num)
        scr.bkgdset(' ', curses.color_pair(100))

        main(scr, c_range=(100,112))

    # Should get us back to normality. ~~Should.~~
    except Exception as e:
        curses.endwin()
        print(e)
    finally:
        curses.endwin()


colors = ((99 , (500, 700, 1000)),
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
         (112, (1000, 1000, 1000)))


if __name__ == '__main__':
    initatron_5000()


