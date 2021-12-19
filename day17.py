#!/usr/bin/env python3

import math
import sys

def dprint(*args):
    DEBUG = False
    # DEBUG = True
    if DEBUG:
        print(*args)

class Probe:
    def __init__(self, x, y, x_range, y_range):
        self.x = 0
        self.y = 0
        self.velocity_x = x
        self.velocity_y = y
        self.x_range = x_range
        self.y_range = y_range
        self.find_max_height()
    
    def step(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.velocity_x > 0:
            self.velocity_x -= 1
        elif self.velocity_x < 0:
            self.velocity_x += 1
        self.velocity_y -= 1

    def in_range(self):
        if self.x in self.x_range and self.y in self.y_range:
            dprint('in_range')
            return True
        return False

    def too_left(self):
        if self.velocity_x <= 0 and self.x < min(self.x_range):
            dprint('too_left')
            return True
        return False

    def too_right(self):
        if self.velocity_x >= 0 and self.x > max(self.x_range):
            dprint('too_right')
            return True
        return False

    def too_low(self):
        if self.velocity_y <= 0 and self.y < min(self.y_range):
            dprint('too_low')
            return True
        return False

    def too_far(self):
        return self.too_low() or self.too_left() or self.too_right()

    def fell_through(self):
        if not self.too_low():
            return False

        if self.x in self.x_range:        
            dprint('fell_through')
            return True
        return False

    def __str__(self):
        return f'{(self.x, self.y)} {(self.velocity_x, self.velocity_y)} {self.max_height} {self.hits}'

    def __repr__(self):
        return str(self)

    def find_max_height(self):
        self.max_height = self.y
        self.hits = False

        dprint(self)

        if self.in_range():
            self.hits = True
            return
        
        while not self.too_far():
            self.step()
            dprint(self)
            self.max_height = max(self.y, self.max_height)
            if self.in_range():
                self.hits = True
                return

def hit_location(x_loc, y_loc):
    x = x_loc #math.sqrt(x_loc)
    y = y_loc #0
    x_range = [x_loc]
    y_range = [y_loc]
    probe = Probe(x, y, x_range, y_range)
    print((x_loc, y_loc))
    while not probe.hits:
        print('.', end='')
        if probe.too_low():
            y += 1
        elif probe.too_left():
            x += 1
        elif probe.too_right():
            x -= 1
        else:
            break
        probe = Probe(x, y, x_range, y_range)
    print()
    dprint(probe)
    return probe

if '__main__' == __name__:
    line = input()
    index = line.find(',')
    x_range = [int(x) for x in line[15:line.find(',')].split('..')]
    index += len(', y=')
    y_range = [int(y) for y in line[index:].split('..')]

    x_range = range(x_range[0], x_range[1]+1)
    y_range = range(y_range[0], y_range[1]+1)
    print(x_range, y_range)

    # print(Probe(0, 0, x_range, y_range))
    # print(Probe(6, 9, x_range, y_range))
    # print(Probe(27, -5, x_range, y_range))
    valid = [(23,-10),(25,-9),(27,-5),(29,-6),(22,-6),(21,-7),(9,0),(27,-7),(24,-5),(25,-7),(26,-6),(25,-5),(6,8),(11,-2),(20,-5),(29,-10),(6,3),(28,-7),(8,0),(30,-6),(29,-8),(20,-10),(6,7),(6,4),(6,1),(14,-4),(21,-6),(26,-10),(7,-1),(7,7),(8,-1),(21,-9),(6,2),(20,-7),(30,-10),(14,-3),(20,-8),(13,-2),(7,3),(28,-8),(29,-9),(15,-3),(22,-5),(26,-8),(25,-8),(25,-6),(15,-4),(9,-2),(15,-2),(12,-2),(28,-9),(12,-3),(24,-6),(23,-7),(25,-10),(7,8),(11,-3),(26,-7),(7,1),(23,-9),(6,0),(22,-10),(27,-6),(8,1),(22,-8),(13,-4),(7,6),(28,-6),(11,-4),(12,-4),(26,-9),(7,4),(24,-10),(23,-8),(30,-8),(7,0),(9,-1),(10,-1),(26,-5),(22,-9),(6,5),(7,5),(23,-6),(28,-10),(10,-2),(11,-1),(20,-9),(14,-2),(29,-7),(13,-3),(23,-5),(24,-8),(27,-9),(30,-7),(28,-5),(21,-10),(7,9),(6,6),(21,-5),(27,-10),(7,2),(30,-9),(21,-8),(22,-7),(24,-9),(20,-6),(6,9),(29,-5),(8,-2),(27,-8),(30,-5),(24,-7)]
    velocities = set()
    min_x = 9999
    max_x = -9999
    min_y = 9999
    max_y = -9999
    for (x,y) in valid:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        probe = Probe(x,y,x_range,y_range)
        if probe.hits:
            velocities.add((x, y))
        else:
            print(probe)
    print((min_x, min_y), (max_x, max_y))
    # print(velocities)
    print(len(velocities))

    velocities = set()
    missed = set()
    print(range(min(y_range), abs(min(y_range))))
    for x in range(max(x_range)+1):
        for y in range(min(y_range), abs(min(y_range))):
            probe = Probe(x, y, x_range, y_range)
            if probe.hits:
                velocities.add((x, y))
            else:
                missed.add((x, y))

    # print(velocities)
    # print(missed)
    print(len(velocities))

    # x = int(math.sqrt(max(x_range)))
    # y = 0

    # previous_max_height = y
    # max_height = y

    # while max_height >= previous_max_height:
    #     previous_max_height = max_height
    #     print(f'----- {max_height}')
    #     ## find box
    #     print(f'--- ? ({x}, {y})')
    #     probe = Probe(x, y, x_range, y_range)

    #     count = 0 # TODO - this is incorrect
    #     while not probe.hits:
    #         dprint(x, y)
    #         print(probe)
    #         if probe.too_low():
    #             y += 1
    #         if probe.too_left():
    #             x += 1
    #         if probe.too_right():
    #             x -= 1
    #         probe = Probe(x, y, x_range, y_range)

    #         # count += 1
    #         # if count > 25:
    #         #     print(max_height)
    #         #     sys.exit(1)
    #     print(probe)

    #     ## increase power until we're shooting too far
    #     print(f'--- > ({x}, {y})')
    #     while probe.hits:
    #         x += 1 # TODO - what if box is negative?
    #         probe = Probe(x, y, x_range, y_range)
    #         print(probe)
    #     x -= 1
    #     probe = Probe(x, y, x_range, y_range)
    #     print(probe)

    #     ## increase height until we miss???
    #     print(f'--- ^ ({x}, {y})')
    #     while probe.hits:
    #         max_height = max(max_height, probe.max_height)
    #         y += 1
    #         probe = Probe(x, y, x_range, y_range)
    #         print(probe)

    # print(previous_max_height)
