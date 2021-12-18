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

class Node:
    def __init__(self, weight, x, y):
        self.weight = int(weight)
        self.neighbors = []
        self.position = (x, y)
        self.risk = 0 if (0, 0) == self.position else None
        self.distance = x + y
    
    def find_neighbors(self, floor_map):
        x,y = self.position
        for delta_x,delta_y in ((0, -1), (0, 1), (1, 0), (-1, 0)):
            # for delta_y in (-1, 0, 1):
            new_y = y + delta_y
            if new_y not in range(len(floor_map)):
                continue
            # for delta_x in (-1, 0, 1):
            # if delta_x == 0 and delta_y == 0:
            #     continue
            new_x = x + delta_x
            if new_x not in range(len(floor_map[new_y])):
                continue
            self.neighbors.append(floor_map[new_y][new_x])
        
        self.neighbors = sorted(self.neighbors, key=lambda neighbor: neighbor.weight) # sort by weights

    def distance_to(self, destination, distances, review):
        if destination.position == self.position:
            distances[self.position] = self.weight
            return distances[self.position]
        
        if self.position in distances:
            # print(self.position, self.weight, distances[self.position])
            return distances[self.position]
        
        neighbors_with_distances = [neighbor for neighbor in self.neighbors if neighbor.position in distances]
        if len(neighbors_with_distances) != len(self.neighbors):
            review.append(self)

        min_distance = self.weight + min(list(map(lambda neighbor: neighbor.distance_to(destination, distances, review), neighbors_with_distances)))
        distances[self.position] = min_distance
        # print(self.position, self.weight, min_distance)
        return min_distance

    def path_to(self, destination, distances):
        if self == destination:
            return [self]
        min_neighbor = None
        for neighbor in self.neighbors:
            if not min_neighbor:
                min_neighbor = neighbor
            if distances[neighbor.position] < distances[min_neighbor.position]:
                min_neighbor = neighbor
        return [self] + min_neighbor.path_to(destination, distances)

    def __repr__(self):
        return f'{self.position} {self.weight}'

    def search(self):
        if None != self.risk:
            return self.risk

        risks = []
        unknowns = []
        for neighbor in self.neighbors:
            if None != neighbor.risk:
                risks.append(neighbor.risk)
            else:
                unknowns.append(neighbor.weight + neighbor.distance)
        
        if not risks:
            return None

        min_risk = min(risks)
        
        if unknowns and min_risk > sorted(unknowns)[0]:
            # print(self, min_risk, sorted(unknowns))
            return None

        self.risk = self.weight + min_risk
        return self.risk

def print_floor(floor_map, highlights = []):
    for row in floor_map:
        for node in row:
            if node in highlights:
                print(color.RED + str(node.weight) + color.END, end='')
            else:
                print(node.weight, end='')
            #print(len(node.neighbors), end='')
        print()

def print_floor2(floor_map, distances, highlights):
    for row in floor_map:
        for node in row:
            if node in highlights:
                print(color.RED + f'{distances[node.position]:03d} ' + color.END, end='')
            else:
                print(f'{distances[node.position]:03d} ', end='')
        print()

def print_floor3(floor_map):
    for row in floor_map:
        for node in row:
            print(f'{node.risk:03d} ', end='')
        print()

if '__main__' == __name__:
    done = False

    floor_map = []
    y = 0
    while not done:
        try:
            line = input()
            weights = list(line)
            row = []
            for x in range(len(weights)):
                row.append(Node(weights[x], x, y))
            floor_map.append(row)
            y += 1
        except:
            done = True

    for row in floor_map:
        for node in row:
            node.find_neighbors(floor_map)

    print_floor(floor_map)

    start = floor_map[0][0]
    end = floor_map[-1][-1]
    print(start.position, end.position)

    to_visit = start.neighbors
    found = [start]
    while to_visit:
        # print(to_visit)
        new_neighbors = []
        for neighbor in to_visit:
            if None == neighbor.search():
                new_neighbors.append(neighbor)
            else:
                found.append(neighbor)
                new_neighbors += neighbor.neighbors
        print(found)
        to_visit = list(set(new_neighbors))
        for neighbor in found:
            if neighbor in to_visit:
                to_visit.remove(neighbor)

    print_floor3(floor_map)
    print(end.risk)








    # to_visit = [end]
    # distances = {}

    # while to_visit:
    #     neighbors = []
    #     review = []
    #     for node in to_visit:
    #         distance = node.distance_to(end, distances, review)
    #         # print(node, distance)
    #         neighbors += node.neighbors
    #     # print('---')
    #     # print(neighbors)
    #     # print(distances)
    #     # print(review)
    #     for neighbor in review:
    #         distances.pop(neighbor.position)
    #     to_visit = review + [neighbor for neighbor in list(set(neighbors)) if neighbor.position not in distances.keys()]
    #     # print(to_visit)
    #     # print('---')
    #     review = []

    # path_to_end = start.path_to(end, distances)
    # print_floor(floor_map, path_to_end)
    # print(start.distance_to(end, distances, []) - start.weight)

    # print_floor2(floor_map, distances, path_to_end)
