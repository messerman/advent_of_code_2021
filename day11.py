#!/usr/bin/env python3

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str((self.x, self.y))
    
    def __repr__(self):
        return str(self)
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def valid(self):
        return not (self.x < 0 or self.y < 0 or self.x > 9 or self.y > 9)
    
    def index(self):
        return (10 * self.y) + self.x

potential_neighbors = {
    'NW':Position(-1,-1),  'N':Position( 0,-1), 'NE':Position( 1,-1),
    'W':Position(-1, 0),                         'E':Position( 1, 0),
    'SW':Position(-1, 1),  'S':Position( 0, 1), 'SE':Position( 1, 1),
}

class Octopus:
    def __init__(self, pos, energy):
        self.pos = pos
        self.energy = int(energy)
        self.neighbors = []
        self.flashed = False
        self.flash_count = 0
    
    def find_neighbors(self, octopodes):
        for movement in potential_neighbors.values():
            potential = movement + self.pos
            # print(self.pos, movement, potential, potential.valid())
            if potential.valid():
                self.neighbors.append(octopodes[potential.index()])
            # print(self.neighbors)
        

    def __str__(self):
        return str(self.energy)
    
    def __repr__(self):
        return str(self)
    
    @classmethod
    def print_all(self, octopodes):
        x = 0
        for octopus in octopodes:
            print(octopus, end='')
            x += 1
            if x >= 10:
                x = 0
                print()

    def increase(self):
        self.energy += 1

    def flash(self):
        if not self.flashed:
            if self.energy > 9:
                self.flashed = True
                self.flash_count += 1
                for neighbor in self.neighbors:
                    neighbor.flash()
            else:
                self.increase()
                if self.energy > 9:
                    self.flash()
        return self

    def reset(self):
        if self.energy > 9:
            self.flashed = False
            self.energy = 0
        return self

if '__main__' == __name__:
    done = False

    octopodes = []
    y = 0
    while not done:
        try:
            line = list(input())
            for x in range(len(line)):
                octopodes.append(Octopus(Position(x,y), line[x]))
            y += 1
        except:
            done = True

    Octopus.print_all(octopodes)
    for octopus in octopodes:
        octopus.find_neighbors(octopodes)

    print()

    i = 0
    while True:
        octopodes = list(map(lambda x: x.flash(), octopodes))
        octopodes = list(map(lambda x: x.reset(), octopodes))
        if len(list(filter(lambda x: x.energy == 0, octopodes))) == 100:
            print(i+1)
            break
        i += 1
        if i == 100:
            total = 0
            for octopus in octopodes:
                total += octopus.flash_count
            print(total)
            Octopus.print_all(octopodes)
            print()
