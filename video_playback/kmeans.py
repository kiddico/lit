#!/usr/bin/env python3

# For some reason my version of the standard library is missing a lot of the math lib...
#from math import dist

from utils import pp
from math import sqrt
from sys import exit
from collections import defaultdict

#def multi_frame_cluster(frames):
def kmeans(frames):
    colors = set()
    for frame in frames:
        # Reverse opencv fuckery to rgb color.
        colors |= { tuple( pixel[::-1] ) for pixel in frame }

    # So, lets think about how we're going to organize this thing.
    # We'll have a dict of centroids -> colors in that centroid (on the last iteration)
    #    Take note that with this approach we'll need to invert the dict at the end to make the color map (given color->displayable color)
    # First up, we need to have centroids, lets just choose 255 (not 256!) random colors.

    dist = lambda c1,c2: sqrt(sum((px - qx) ** 2.0 for px, qx in zip(c1, c2)))
    initialize_clustering(colors)

    # 
    print(len(colors))
    exit()

# Get the initial centers and make a dict mapping centers to colors.
def initialize_clustering(colors):
    # Does set have any type of ordering? I assume not because it just uses a has function.
    # So, if I just take the first N from a set, does that 

    # yuuuuppp. works perfectly
    centroids = list(colors)[:100]
    clusters  = defaultdict(list)
    # okay... not this gets computationally .... hard.
    
    for color in colors:
        #find clostest centroid

# Given a set of colors use kmeans to find the centroid.
# return as tuple of tuples
# this is meant to be ran post-clamping, so the bgr -> rgb conversion is already done.
# and in theory the color space is already fairly reduced so things **should** be a wee bit faster.
def find_centroids(colors):


    pass

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
