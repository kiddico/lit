#!/usr/bin/env python3

import sys
import time
import numpy
import curses
from utils import pp
from math import ceil
from collections import defaultdict

from numpy import intc


scr = None
def main():
    img = numpy.load('test_out.numpy_dump', allow_pickle=True)
    # Try to 'compress' the image down to our displayable area.
    # Find LCD of images h/w
    ih, iw, _ = img.shape
    ires = (ih, iw)

    try:
        global scr
        scr = prep_curses()
        height, width = scr.getmaxyx()
        # In reality we have twice the number of vertical pixels.
        # Virtual sizes, width is left out of the modification party. SAD.
        #vh, vw = height, width
        vh, vw = height*2, width
        vres = (vh, vw)

        color_dict = {}
        #np.ndenumerate(a)
        if ih <= vh and iw <=vw:
            cprint('Holy balls')
            to_display = img
        else:
            # Find aspect rations
            h_ratio = ceil(ih/vh)
            w_ratio = ceil(iw/vw)
            # our scaling blocks are going to be X^2 for whichever is larger
            blocksize = max(h_ratio, w_ratio)
            new_h = int(ih/blocksize)
            new_w = int(iw/blocksize)
            qprint('img: {}x{}'.format(ih,iw))
            qprint('scr: {}x{}'.format(vh,vw))
            qprint('new: {}x{}'.format(new_h,new_w))
            qprint('bs: {}'.format(blocksize))
            frame = numpy.zeros((new_h, new_w, 3))
            for y, row in enumerate(frame):
                trow = []
                for x, _ in enumerate(row):
                    # os = original section
                    os = img[y*blocksize:((y+1)*blocksize), x*blocksize:((x+1)*blocksize)]
                    qprint(os)
                    # Need to cast to int to we don't overflow uint8
                    lined_up = os.flatten().reshape((-1,3)).astype(intc)
                    qprint(lined_up)
                    avg = (sum(lined_up) / blocksize**2).astype(intc)
                    frame[y][x] = avg
                    qprint(avg)

                    # reshuffle to rgb (from bgr)
                    # align on intervals of 1000/16, from 0 to 992
                    rgb = [ color for color in avg[::-1]]
                    qprint(rgb)
                    rgb = [ int((color/255)*16)/16*1000 for color in avg[::-1]]
                    cprint(rgb)

                    # declare this as a color
                    if t in color_dict:
                        color_index = color_dict[t]
                    else:
                        # declare color and 'pair', add ref in dict.
                        if len(color_dict):
                            # grab the last used color index
                            color_index = color_dict.setdefault(t, max(color_dict.values())+1)
                            qprint('set color index to {}'.format(color_index))
                        else:
                            color_index = 1
                            color_dict[t] = 1
                        cprint('{} : {}, {}, {}'.format(color_index, *t))
                        cprint('{} : {}'.format(y,x))
                        trow.append(tuple([color_index,t]))
                        curses.init_color(color_index, *t)
                        curses.init_pair(color_index, color_index, color_index)
                    scr.addstr(y, x, ' ', color_index<<8)
                cprint(trow)




        #qprint(frame)
        #qprint(blocksize)
        #cprint(frame.shape)

        #color_dict = defaultdict(int)
        #for row in frame:
        #    for cell in row:
        #        color_dict[tuple(cell)]+=1


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
