#!/usr/bin/env python3

def reproduce(fish):
    output = {}
    for i in range(1,9):
        output[i-1] = fish[i]
    output[6] += fish[0]
    output[8] = fish[0]
    return output

if '__main__' == __name__:
    done = False
    fish = {num:0 for num in range(9)}

    while not done:
        try:
            line = input()
            for state in line.split(','):
                fish[int(state)] += 1
        except:
            done = True

    # print(fish)
    for i in range(256):
        fish = reproduce(fish)
        # print(fish)

    print(sum(fish.values()))
