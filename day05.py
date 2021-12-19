#!/usr/bin/env python3

def find_vents(line):
    xy1, xy2 = line
    x1,y1 = xy1
    x2,y2 = xy2

    vents = []

    if x1 == x2:
        starting = min(y1, y2)
        ending = max(y1, y2) + 1
        for y in range(starting, ending):
            vents.append((x1, y))
    elif y1 == y2:
        starting = min(x1, x2)
        ending = max(x1, x2) + 1
        for x in range(starting, ending):
            vents.append((x, y1))
    elif is_diagonal(x1,y1,x2,y2):
        x = x1
        y = y1

        delta_x = -1 if x1 > x2 else 1
        delta_y = -1 if y1 > y2 else 1

        while (x, y) != (x2, y2):
            vents.append((x,y))
            x += delta_x
            y += delta_y

        vents.append((x2, y2))

    return vents

def is_diagonal(x1,y1,x2,y2):
    x_diff = abs(x1 - x2)
    y_diff = abs(y1 - y2)
    return x_diff == y_diff

def print_ocean(ocean_floor, width):
    for i in range(width):
        for j in range(width):
            spot = ocean_floor[(j, i)]
            if spot == 0:
                spot = '.'
            print(spot, end='')
        print()
    print()

def count_intersections(ocean_floor):
    count = len([x for x in ocean_floor.values() if x > 1])
    return count

if '__main__' == __name__:
    done = False
    lines = []
    max_val = 0

    while not done:
        try:
            line = input()
            x1,y1,x2,y2 = [int(x) for x in ','.join(line.split(' -> ')).split(',')]
            
            lines.append([(x1,y1),(x2,y2)])

            max_val = max(max_val, x1, x2, y1, y2)
        except:
            done = True

    max_val += 1
    # print(lines, max_val)

    ocean_floor = {}
    for i in range(max_val):
        for j in range(max_val):
            ocean_floor[(i,j)] = 0

    # print_ocean(ocean_floor, max_val)
    
    for line in lines:
        vents = find_vents(line)
        # print(line, vents)
        for vent in vents:
            ocean_floor[vent] += 1

    # print_ocean(ocean_floor, max_val)

    print(count_intersections(ocean_floor))
