#!/usr/bin/env python3

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class FloorSpace:
    def __init__(self, x, y, height, neighbors=[]):
        self.x = x
        self.y = y
        self.height = height
        self.neighbors = []

    def north(self):
        return (self.x, self.y+1)

    def south(self):
        return (self.x, self.y-1)

    def east(self):
        return (self.x+1, self.y)

    def west(self):
        return (self.x-1, self.y)

    def find_neighbors(self, floor):
        possible_neighbor_coords = [self.north(), self.south(), self.east(), self.west()]
        for coord in possible_neighbor_coords:
            if coord in floor:
                self.neighbors.append(floor[coord])

    def is_lowest(self):
        for neighbor in self.neighbors:
            if self.height >= neighbor.height:
                return False
        return True

    def risk_level(self):
        return self.height + 1

    def location(self):
        return (self.x, self.y)

    def find_basin(self, basin=set()):
        if 9 == self.height:
            return basin

        basin = basin | {self.location(),}
        for neighbor in self.neighbors:
            if neighbor.location() not in basin:
                basin = basin | neighbor.find_basin(basin)

        return basin

    def __str__(self):
        return f'({self.x}, {self.y}, {self.height})'

    def __repr__(self):
        return str(self)

if '__main__' == __name__:
    done = False

    floor = {}
    y = 0
    width = 0
    while not done:
        try:
            line = input()
            heights = [int(height) for height in list(line)]
            for x in range(len(heights)):
                floor[(x,y)] = FloorSpace(x, y, heights[x])
            y += 1
            width = len(heights)
        except:
            done = True

    height = y

    # print(width, height)

    for space in floor.values():
        space.find_neighbors(floor)

    lows = []
    for y in range(height):
        for x in range(width):
            space = floor[(x, y)]
            # print(space, ' - ', space.neighbors)
            if space.is_lowest():
                lows.append(space)
                print(color.RED + str(space.height) + color.END, end='')
            elif 9 == space.height:
                print(space.height, end='')
            else:
                print(color.GREEN + str(space.height) + color.END, end='')
        print()

    basins = []
    for low in lows:
        basin = low.find_basin()
        # print(sorted(basin))
        basins.append(basin)

    total = 1
    basin_sizes = [len(basin) for basin in basins]
    for basin_size in sorted(basin_sizes)[-3:]:
        total *= basin_size
    print(total)
