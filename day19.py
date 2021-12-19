#!/usr/bin/env python3

import math

class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def distance(self, other):
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2 + (other.z - self.z)**2)

    def __str__(self):
        return str((self.x, self.y, self.z))

    def __repr__(self):
        return str(self)

class Beacon:
    def __init__(self, position):
        self.position = position
        zero = Position(0,0,0)
        self.distance = self.position.distance(zero)

    def __str__(self):
        return str(self.position)

    def __repr__(self):
        return str(self)

class Scanner:
    def __init__(self, beacons, position=None):
        self.beacons = beacons
        self.position = position

    def __str__(self):
        return f'{self.position} - {self.beacons}'

    def __repr__(self):
        return str(self)

if '__main__' == __name__:
    done = False

    scanners = {}
    scanner = []
    scanner_num = -1
    while not done:
        try:
            line = input()
            if not line:
                scanners[scanner_num] = Scanner(scanner)
                scanner = []
                continue
            if '---' == line[0:3]:
                print(line)
                scanner_num = int(line.split(' ')[2])
                continue
            scanner.append(Beacon(Position(*[int(num) for num in line.split(',')])))
        except:
            scanners[scanner_num] = scanner
            done = True

    # print(scanners)

    # for beacon in scanners[0].beacons:
    #     print(f'{beacon} - {beacon.distance}')

    
