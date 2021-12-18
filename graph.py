#!/usr/bin/env python3

class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.edges = {}

    def add_edge(self, edge, destination):
        self.edges[destination.name] = edge

    def __str__(self):
        return f'{self.name} - {self.value} - {list(self.edges.keys())}'
    
    def __repr__(self):
        return str(self)

class Edge:
    def __init__(self, node_1, node_2, weight=0):
        self.node_1 = node_1
        self.node_2 = node_2
        self.weight = 0

    def __str__(self):
        return f'{self.node_1.name} --{self.weight}-- {self.node_2.name}'

    def __repr__(self):
        return str(self)

    def other_node(self, node):
        if node == self.node_1:
            return self.node_2
        if node == self.node_2:
            return self.node_1
        return None

class Graph:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = {node.name:node for node in nodes}
        self.edges = edges
    
    def add_node(self, node):
        self.nodes[node.name] = node
    
    def add_edge(self, edge):
        self.edges.append(edge)
        edge.node_1.add_edge(edge, edge.node_2)
        edge.node_2.add_edge(edge, edge.node_1)

    def node(self, name):
        if name in self.nodes:
            return self.nodes[name]
        return None
    
    @classmethod
    def from_grid(self, grid, node_class=Node, edge_class=Edge, diagonals=False):
        graph = Graph()
        for y in range(len(grid)):
            row = grid[y]
            for x in range(len(row)):
                node = node_class((x,y), row[x])
                graph.add_node(node)
        
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                node = graph.node((x,y))
                neighbors = [(x,y-1), (x,y+1), (x+1,y), (x-1,y)]
                for neighbor in neighbors:
                    destination = graph.node(neighbor)
                    if destination:
                        edge = edge_class(node, destination)
                        graph.add_edge(edge)
        return graph

    def __str__(self):
        output = ''
        for node in self.nodes.values():
            output += str(node)
            output += '\n'
        return output

if '__main__' == __name__:
    grid = []
    done = False
    while not done:
        try:
            line = input()
            grid.append(list(line))
        except:
            done = True

    graph = Graph.from_grid(grid)
    print(graph)
