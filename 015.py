#!/usr/bin/env python3

import copy
import sys

from graph import *

class FloorNode(Node):
    def __init__(self, name, value):
        super().__init__(name, value)
        self.risk = sys.maxsize

    def visit_neighbors(self):
        to_visit = []
        cost_out = self.risk + self.value
        # print("---")
        # print(self.name, cost_out)
        for edge in self.edges.values():
            node = edge.other_node(self)
            # print(node.name, edge.weight)
            if cost_out < edge.weight:
                edge.weight = cost_out
                to_visit.append(node)
                node.visit(cost_out)
                # print(f'added {node.name}')
            # else:
        #         print(f'skipped {node.name}')
        # print("---")
        return to_visit

    def visit(self, risk):
        self.risk = min(risk, self.risk)

def new_grid(old_grid, to_add):
    grid = copy.deepcopy(old_grid)
    for row in range(len(old_grid)):
        for col in range(len(old_grid[row])):
            new_value = (old_grid[row][col] - 1 + to_add) % 9 + 1
            grid[row][col] = new_value
    return grid

if '__main__' == __name__:
    grid = []
    done = False

    build_graph = False
    while not done:
        try:
            line = input()
            if 'x5' == line:
                build_graph = True
                continue
            grid.append([int(i) for i in list(line)])
        except:
            done = True

    if build_graph:
        grids = {}
        for i in range(9):
            grids[i] = new_grid(grid, i)

        # print(grids)

        big_grid = []
        for j in range(5):
            for i in range(len(grid[0])):
                big_grid.append(grids[j+0][i] + grids[j+1][i] + grids[j+2][i] + grids[j+3][i] + grids[j+4][i])
            
        # for row in big_grid:
        #     for val in row:
        #         print(val, end='')
        #     print()

        grid = big_grid

    graph = Graph.from_grid(grid, node_class=FloorNode)
    for edge in graph.edges:
        edge.weight = sys.maxsize
    # print(graph)

    # for edge in graph.edges:
    #     print(edge)

    start_node = graph.node((0,0))
    start_node.risk = 0
    start_node.value = 0
    to_visit = [start_node]
    while to_visit:
        # print([node.name for node in to_visit])
        next_visits = []
        for node in to_visit:
            next_visits += node.visit_neighbors()
        to_visit = list(set(next_visits))

    width = len(grid[0])
    height = len(grid)
    # for y in range(height):
    #     for x in range(width):
    #         print(f'{graph.node((x,y)).risk:02d} ', end='')
    #     print()

    end_node = graph.node((width-1, height-1))
    print(end_node.risk + end_node.value)
