#!/usr/bin/env python
'''
Man like fire.
Man make fire.
Man make number box.
Man no like fire no in number box.
Man want number box make fire.
Man bad make program.
Number box be fire.
---
Made using blessed, and the included worms.py[0] as an example.
Because I lack ingenuity I also stole most of the logic from Sabglard's blog[1], and failed to properly implement his challenge.

0 - https://github.com/jquast/blessed/blob/master/bin/worms.py
1 - http://fabiensanglard.net/doom_fire_psx/
'''
import time
from sys import exit
from functools import partial
from random import random, randrange

from blessed import Terminal
from blessed.formatters import FormattingString
from blessed.formatters import ParameterizingString

'''
Things that still need done:
    * The wind is terrible
        * make it less terrible.
    * Multithreaded would be nice.
        * Rows only need to know about the previous row
        * If we made a function take a tuple and return a tuple we could throw each in a thread.
    * Speaking of tuples, might be cheaper to use one for the bottom row.
        * Avoid create/delete loop when the source is toggled.
    * Better state handling would be good.
        * Maybe put that inside time_tick()
        * No need to pass them out to pass them back in, and then in again.
        * Though with that logic I could shove all this in main() and call it a day.
'''


term = Terminal()
color = ParameterizingString(term.color, term.normal, 'color')
color_list = [16,52,88,124,160,196,202,208,214,220,226,228,231]

f_cols = [ FormattingString(term.on_color(c), term.normal) for c in color_list ]
bg = FormattingString(term.on_color(16), term.normal)

def main():

    clear()
    u_in = None

    wind = 0
    speed = 0.0025
    weight_seed = 1.25
    source = True

    state = clean_state()
    with term.hidden_cursor(), term.cbreak(), term.location():
        while u_in not in ('Q','q'):
            if u_in:
                state, wind, speed, weight_seed, source = handle_input(
                    u_in,
                    state,
                    wind,
                    speed,
                    weight_seed,
                    source
                    )

            draw_fire(state)
            state = time_tick(state, source, weight_seed, wind)
            u_in = term.inkey(timeout=speed)

        clean_up()


def handle_input(u_in, state, wind, speed, weight_seed, enable_source):
    seed_keys = {
                'KEY_UP'   : -0.25,
                'KEY_DOWN' : 0.25
                }

    speed_keys = {
                'KEY_PGUP'   : -0.0025,
                'KEY_PGDOWN' : 0.0025
                }

    wind_keys = {
                'KEY_LEFT'  : -1,
                'KEY_RIGHT' : 1
                }

    if u_in == ' ':
        enable_source = not enable_source
        if enable_source:
            state[0] = [ len(f_cols)-1 for col in range(0,len(state[0])) ]
        else:
            state[0] = [ 0 for col in range(0,len(state[0])) ]

    if u_in.name in seed_keys:
        new = weight_seed + seed_keys[u_in.name]
        weight_seed = new if new >= 0 else 0

    if u_in.name in speed_keys:
        new = speed + speed_keys[u_in.name]
        speed = new if 0 <= new <= 1.0 else speed

    if u_in.name in wind_keys:
        new = wind + wind_keys[u_in.name]
        wind = new if -3 <= new <= 3 else wind
    return state, wind, speed, weight_seed, enable_source



def draw_fire(state):
    def row_values_to_str(row):
        return ''.join([ str(f_cols[x](' ')) for x in row ])

    row_strs = [ row_values_to_str(r) for r in state ]
    for y_index in range(term.height-1, 0, -1):
        with term.location(0, y_index):
            echo(row_strs.pop(0))


def clean_state():
    h=term.height
    w=term.width
    state = [[ len(f_cols)-1 for x in range(0,w) ]]
    state.extend([ [0 for x in range(0,w)] for y in range(1,h) ])
    return state


def time_tick(state, enable_source, weight_seed, wind):
    goal_height = int(len(state) * 0.95)
    height = term.height
    width  = term.width

    for y in range(height-1, 0, -1):
        decay_weight = weight_seed * (y/goal_height)
        # Trying to skip over rows where nothing can happen...
        if any((c>0 for c in state[y-1])) or any((c>0 for c in state[y])):

            for x in range(0,width):
                decay = ((int(random()*3)&3)&1) + int(decay_weight)

                t_x = x
                if wind != 0:
                    t_x = x - wind
                    if wind > 0:
                        t_x = t_x if t_x >= 0 else 0
                    else:
                        t_x = t_x if t_x < (width-1) else (width-1)

                # Chance to just decay instead of inherit + decay
                # lets the initial growth vary
                in_a_row = 3
                if sum([randrange(0, in_a_row) for i in range(0, in_a_row)]) == in_a_row:
                    new = state[y][t_x] - decay
                    state[y][x] = new if new >= 0 else 0
                else:
                    direction = randrange(-1,1)
                    new = state[y-1][t_x+direction] - decay
                    state[y][x] = new if new >= 0 else 0

    return state


def clear():
    echo(term.move(0, 0))
    echo(bg(term.clear))

def clean_up():
    echo(term.move(0, 0))
    echo(term.ed)



echo = partial(print, end='', flush=True)

if __name__ == '__main__':
    main()
