#!/usr/bin/env python3

from math import sqrt
from collections import defaultdict

def kmeans(frames):
    color_set = set()
    for frame in frames:
        for row in frame:
            color_set |= { cell for cell in row }
    color_list = list(color_set)


    dist = lambda c1,c2: sqrt(sum((px - qx) ** 2.0 for px, qx in zip(c1, c2)))

    # Initialize Clusters
    centroids = color_list[:255]# lists from set have no order. Hopefully this is random enough. ¯\_(ツ)_/¯
    clusters  = defaultdict(list)
    for color in color_list:
        closest = min( ( (dist(color, cent), cent) for cent in centroids ), key=lambda x:x[0])
        clusters[closest[1]].append(color)


    # Iterate to taste.
    for _ in range(0, 7):
        centroids = []
        for colors in clusters.values():
            # Find the average of all colors in a cluster and use that as a new centroid.
            d = len(colors) # Cache instead of len()-ing 3 times.
            centroids.append((
                int(sum(t[0] for t in colors)/d),
                int(sum(t[1] for t in colors)/d),
                int(sum(t[2] for t in colors)/d)
                ))

        # Wipe out centroids from last iteration.
        # For some reason calling a default dict's clear() will break it defaultiness
        clusters  = defaultdict(list)
        for color in color_list:
            closest = min( ( (dist(color, cent), cent) for cent in centroids ), key=lambda x:x[0])
            clusters[closest[1]].append(color)

    # Now we need to invert the dict so we have a color to centroid mapping
    color_map = {}
    for center, colors in clusters.items():
        for color in colors:
            color_map[color] = center

    return color_map, list(clusters.keys())


def main(): pass
if __name__ == '__main__':
    main()
