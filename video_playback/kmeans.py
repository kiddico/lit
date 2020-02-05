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
    color_list = list(colors)
    # "Random" centroids to start. Assumes set wont magially sort things.
    centroids = color_list[:100]
    clusters  = defaultdict(list)
    dist = color_distance
    for color in color_list[::-1]:
        # get a tuple of the closest ceontroid.
        #closest = min( [ (dist(color, cent), cent) for cent in centroids ], key=lambda x:x[0])
        distances = sorted([ (dist(color, cent), cent) for cent in centroids ], key=lambda x:x[0])
        pp(centroids)
        print('')
        pp(color)
        print('')
        pp(distances)
        exit()
        pass
        #find clostest centroid


# Distance between two color values.
#def color_distance(c1, c2):
#    return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(c1, c2)))

# Be sure to bring into local scope!
color_distance = lambda c1,c2: sqrt(sum((px - qx) ** 2.0 for px, qx in zip(c1, c2)))

# Get the distance between a single color (c1) and a list of colors (l1).
# return the distance, color, and index (in a tuple) of the closes color in l1.
def color_distances(c1, l1):
    pass



# No touchy.
def main(): pass
if __name__ == '__main__':
    main()
