#!/usr/bin/env python3
import curses
import numpy
from utils import pp
from collections import namedtuple
'''
passing thoughts :
    * Color compression before or after resize?
        * before -> averaged colors might now be near anything in the initial compression.
    * two pass yay or nay?
    * it would be interesting to pre-define a uniform color space, and 'cluster' around that.
        * In this case "clustering" is just finding the closest predefined color...

general approach description :
    1 Read image, determine dimensions.
    2 Inspect terminal -> get dimensions.
    3 K means color quantization
        3.1 Reduce to 256(255) colors
    4 two pass resize (horizontal then vertical)
        4.1 assign value of clusters centroid
'''

resolution = namedtuple('resolution', ['y', 'x'])
def main():

    image = numpy.load('test_out.numpy_dump', allow_pickle=True)
    ires = resolution(*image.shape[:2])
    try:
        scr = prep_curses()
        height, width = scr.getmaxyx()
        sres = resolution(height, width)

        reduction_ratio(ires, sres)
    except:
        scr.clear()
        curses.endwin()
        print('\n')
        pp(e.args)
        raise e
    finally:
        scr.clear()
        curses.endwin()


def reduction_ratio(ires, sres):
    # alright, lets start off with an easy target
    # finding the number of rows/cols that need to be compressed into each tixel

    pass

def prep_curses():
    scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    scr.keypad(True)
    curses.curs_set(0)
    curses.start_color()
    return scr

def reduce_color_space(image):
    pass

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
