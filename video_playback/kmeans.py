#!/usr/bin/env python3

from utils import pp


def multi_frame_cluster(frames):
    '''
    Frames are from opencv IM_READ.
    Not sure if I want to do this pre or post resize...
    Post would obviously be a LOT faster...
    We'll figure things out as we go.
    '''
    cvolors = {}
    for frame in frames:
        # Reverse opencv fuckery to rgb color.
        colors = colors | { tuple( frame[::-1] ) for pixel in frame }
    pp(colors)



# No touchy.
def main(): pass
if __name__ == '__main__':
    main()
