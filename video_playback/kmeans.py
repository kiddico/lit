#!/usr/bin/env python3

# For some reason my version of the standard library is missing a lot of the math lib...
#from math import dist

from utils import pp
from math import sqrt
from sys import exit


#def multi_frame_cluster(frames):
def kmeans(frames):
    '''
    Frames are from opencv IM_READ.
    Not sure if I want to do this pre or post resize...
    Post would obviously be a LOT faster...
    We'll figure things out as we go.
    '''
    colors = set()
    for frame in frames:
        # Reverse opencv fuckery to rgb color.
        colors = colors | { tuple( pixel[::-1] ) for pixel in frame }

    print(len(colors))
    exit()

# Distance between two color values.
def color_distance(c1, c2):
    # The assumption is made that colors are a tuple in rgb order.
    #return sqrt( () + () + ())**2
    # JFM man
    return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(c1, c2)))

# Get the distance between a single color (c1) and a list of colors (l1).
# return the distance, color, and index (in a tuple) of the closes color in l1.
def color_distances(c1, l1):
    pass



# No touchy.
def main(): pass
if __name__ == '__main__':
    main()
