#!/usr/bin/env python3
import math
import statistics

def cost_to_move_to(positions, destination):
    cost = 0
    for position in positions:
        cost += abs(destination - position)
    return cost

def cost_to_move2(positions, destination):
    cost = 0
    for position in positions:
        diff = abs(destination - position)
        cost += int(((diff + 1)) * diff / 2)
    return cost

def divide_and_conquer(positions):
    min_value = min(positions)
    max_value = max(positions)
    mean_value = statistics.mean(positions)

    cost_min = cost_to_move2(positions, min_value)
    cost_mean1 = cost_to_move2(positions, math.floor(mean_value))
    cost_mean2 = cost_to_move2(positions, math.ceil(mean_value))
    cost_max = cost_to_move2(positions, max_value)

    best = min(cost_min, cost_mean1, cost_mean2, cost_max)
    return best

if '__main__' == __name__:
    line = input()
    positions = [int(x) for x in line.split(',')]
    print(statistics.mean(positions), statistics.median(positions), statistics.mode(positions))
    print(cost_to_move_to(positions, int(statistics.median(positions))))

    print(divide_and_conquer(positions))
