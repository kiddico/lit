#!/usr/bin/env python3

# For some reason my version of the standard library is missing a lot of the math lib...
#from math import dist

from utils import pp
from math import sqrt
from sys import exit
from collections import defaultdict

#def multi_frame_cluster(frames):
def kmeans(frames):
    color_set = set()
    for frame in frames:
        for row in frame:
            color_set |= { cell for cell in row }
    color_list = list(color_set)

    # We'll have a dict of centroids -> colors in that centroid (on the last iteration)
    #    Take note that with this approach we'll need to invert the dict at the end
    #    to make the color map (given color->displayable color)

    dist = lambda c1,c2: sqrt(sum((px - qx) ** 2.0 for px, qx in zip(c1, c2)))
    clusters = initialize_clustering(color_list)

    # I have no idea what a reasonable amount of iterations is.
    # We **should** have a metic to optimize for (avg/max dist of points from centroids?)
    # but it could run for an arbitrary length of time if we do that...

    #print('Before: ')
    #pp(sorted([k for k in clusters.keys()][:10], key=lambda x:x[0]))

    for _ in range(0, 42):
        centroids = []
        #for colors in clusters.values():
        for centroid, colors in clusters.items():
            print('before: {}'.format(repr(centroid)))
            d = len(colors)
            centroids.append((
                int(sum(t[0] for t in colors)/d),
                int(sum(t[1] for t in colors)/d),
                int(sum(t[2] for t in colors)/d)
                ))

            print('after: {}\n'.format(repr(centroids[-1])))
        clusters  = defaultdict(list)
        for color in color_list:
            closest = min( [ (dist(color, cent), cent) for cent in centroids ], key=lambda x:x[0])
            clusters[closest[1]].append(color)
        break

    #print('\n\n------\n')
    #print('after: ')
    #pp(sorted([k for k in clusters.keys()][:10], key=lambda x:x[0]))

    exit()

# Get the initial centers and make a dict mapping centers to colors.
def initialize_clustering(color_list):
    # "Random" centroids to start. Assumes set wont magially sort things.
    # Which is a somewhat dangerous approach with recent changes to dict sorting by default.
    centroids = color_list[:255]
    clusters  = defaultdict(list)
    dist = color_distance
    for color in color_list:
        closest = min( [ (dist(color, cent), cent) for cent in centroids ], key=lambda x:x[0])
        clusters[closest[1]].append(color)
        #pp(sorted( [ (dist(color, cent), cent) for cent in centroids ], key=lambda x:x[0]))
    return clusters

# First iteration
def get_next_cetroids(clusters):
    pass

# Be sure to bring into local scope!
color_distance = lambda c1,c2: sqrt(sum((px - qx) ** 2.0 for px, qx in zip(c1, c2)))


# No touchy.
def main(): pass
if __name__ == '__main__':
    main()
