#!/usr/bin/env python3

def print_paper(max_x, max_y, dots):
    # print(max_x, max_y, dots)
    paper = []
    for y in range(max_y):
        row = []
        for x in range(max_x):
            row.append('#' if (x,y) in dots else ' ')
        paper.append(row)
    for row in paper:
        print(''.join(row))

    print()


if '__main__' == __name__:
    done = False

    dots = set()
    instructions = []
    all_coordinates_received = False
    max_x = 0
    max_y = 0
    while not done:
        try:
            line = input()
            if not line:
                all_coordinates_received = True
            elif all_coordinates_received:
                (direction,location) = line.split('=')
                direction = direction[-1]
                instructions.append((direction, int(location)))
            else:
                (x,y) = line.split(',')
                dots.add((int(x), int(y)))
                max_x = max(int(x), max_x)
                max_y = max(int(y), max_y)
        except:
            done = True

    # print(dots)
    # print(instructions)

    max_x += 1
    max_y += 1

    # print_paper(max_x, max_y, dots)

    print(len(dots))
    for (direction, value) in instructions:
        new_dots = set()
        if 'x' == direction:
            # fold horizontally
            for dot in dots:
                new_x = dot[0] if dot[0] < value else value - (dot[0] - value)
                new_dot = (new_x, dot[1])
                # print(dot, new_dot)
                new_dots.add(new_dot)
                max_x = value
        else:
            # fold vertically
            for dot in dots:
                new_y = dot[1] if dot[1] < value else value - (dot[1] - value)
                new_dot = (dot[0], new_y)
                # print(dot, new_dot)
                new_dots.add(new_dot)
                max_y = value
        dots = new_dots
        print(len(dots))
        # print_paper(max_x, max_y, dots)

    print_paper(max_x, max_y, dots)


