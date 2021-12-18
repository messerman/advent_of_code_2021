#!/usr/bin/env python3

class Sub:
    def __init__(self, depth=0, horizontal=0, aim=0):
        self.depth = depth
        self.horizontal = horizontal
        self.aim = aim
    
    def move(self, direction, distance):
        if 'forward' == direction:
            self.horizontal += distance
            self.depth += self.aim * distance
        elif 'up' == direction:
            # self.depth -= distance
            self.aim -= distance
        elif 'down' == direction:
            # self.depth += distance
            self.aim += distance

if '__main__' == __name__:
    done = False

    sub = Sub()
    while not done:
        try:
            line = input()
            (direction, distance) = line.split(' ')
            sub.move(direction, int(distance))
        except:
            done = True
    
    print(sub.horizontal * sub.depth)
