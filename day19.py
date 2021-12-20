#!/usr/bin/env python3

import copy
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

    def __add__(self, other):
        return self.__class__(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return self.__class__(self.x-other.x, self.y-other.y, self.z-other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

class Beacon(Position):
    def pitch_up(self):
        return Beacon(-self.z, self.y, self.x)
    def pitch_down(self):
        return Beacon(self.z, self.y, -self.x)
    def roll_left(self):
        return Beacon(self.x, -self.z, self.y)
    def roll_right(self):
        return Beacon(self.x, self.z, -self.y)
    def yaw_left(self):
        return Beacon(-self.y, self.x, self.z)
    def yaw_right(self):
        return Beacon(self.y, -self.x, self.z)

    @classmethod
    def rotations(cls):
        return [
            [], #0

            [cls.yaw_left], #1
            [cls.yaw_right], #2
            [cls.pitch_up], #3
            [cls.pitch_down], #4
            [cls.roll_left], #5
            [cls.roll_right], #6

            [cls.yaw_left, cls.yaw_left], #7
            [cls.yaw_left, cls.pitch_up], #8
            [cls.yaw_left, cls.pitch_down], #9
            [cls.yaw_left, cls.roll_left], #10
            [cls.yaw_left, cls.roll_right], #11

            [cls.yaw_right, cls.pitch_up], #12
            [cls.yaw_right, cls.pitch_down], #13
            [cls.yaw_right, cls.roll_left], #14
            [cls.yaw_right, cls.roll_right], #15

            [cls.yaw_left, cls.yaw_left, cls.pitch_up], #16
            [cls.yaw_left, cls.yaw_left, cls.pitch_down], #17
            [cls.yaw_left, cls.yaw_left, cls.roll_left], #18
            [cls.yaw_left, cls.yaw_left, cls.roll_right], #19

            [cls.yaw_left, cls.pitch_up, cls.pitch_up], #20
            [cls.yaw_left, cls.roll_left, cls.roll_left], #21

            [cls.yaw_left, cls.pitch_up, cls.pitch_up, cls.yaw_left], #22
            [cls.yaw_left, cls.roll_left, cls.roll_left, cls.yaw_left], #23
        ]

    def rotate(self, operations):
        y = copy.deepcopy(self)
        for op in operations:
            y = op(y)
        return y

    def orientations(self):
        orientations = []
        for operations in self.rotations():
            orientations.append(self.rotate(operations))
        return orientations

class Scanner:
    def __init__(self, beacons, position=None):
        self.beacons = beacons
        self.position = position

    def __str__(self):
        return f'{self.position} - {self.beacons}'

    def __repr__(self):
        return str(self)

    def beacon_rotations(self):
        return [beacon.orientations() for beacon in self.beacons]
    
    def all_distances(self):
        distances = {}
        for i in range(len(self.beacons)):
            beacon1 = self.beacons[i]
            for j in range(i+1,len(self.beacons)):
                beacon2 = self.beacons[j]
                distance = beacon2.distance(beacon1)
                if distance not in distances:
                    distances[distance] = []
                distances[distance].append((i,j))
        return distances

    def overlap(self, other):
        beacons = {i:[] for i in range(24)}

        rotations = other.beacon_rotations()

        for i in range(len(self.beacons)):
            for j in range(i+1,len(self.beacons)):
                a = self.beacons[i]
                b = self.beacons[j]
                delta = b - a
                for k in range(len(other.beacons)):
                    for l in range(k+1,len(other.beacons)):
                        for rotation in range(24):                            
                            c = rotations[k][rotation]
                            d = rotations[l][rotation]
                            delta2 = d - c
                            if delta == delta2:
                                beacons[rotation].append((a,c))
                                beacons[rotation].append((b,d))
        return beacons

    def rotate(self, rotations):
        new_beacons = []
        for beacon in self.beacons:
            new_beacons.append(beacon.rotate(rotations))
        self.beacons = new_beacons

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
                scanner_num = int(line.split(' ')[2])
                continue
            scanner.append(Beacon(*[int(num) for num in line.split(',')]))
        except:
            scanners[scanner_num] = Scanner(scanner)
            done = True

    scanners[0].position = Beacon(0,0,0)

    #scanners = {4:scanners[4], 19:scanners[19], 25:scanners[25]}
    #scanners[4].position = Beacon(0,0,0)
    tried = []
    needs_pos = [i for i in scanners.keys() if not scanners[i].position]
    while [i for i in scanners.keys() if not scanners[i].position]:
        found = 0
        # for i in range(len(scanners)):
        #     scanner1 = scanners[i]
        for i,scanner1 in scanners.items():
            if not scanner1.position:
                continue
            # for j in range(len(scanners)):
            #     scanner2 = scanners[j]
            for j,scanner2 in scanners.items():
                if scanner1 == scanner2:
                    continue
                if scanner2.position:
                    continue
                if (i,j) in tried:
                    continue
                print(f'Trying {(i,j)}')
                tried.append((i,j))
                overlap = scanner1.overlap(scanner2)
                max_len = 0
                for k in range(24):
                    pairs = list(set(overlap[k]))
                    max_len = max(max_len, len(pairs))
                    if len(pairs) >= 11: # TODO - should be 12
                        delta = pairs[0][0] - pairs[0][1]
                        scanner2.position = scanner1.position + delta
                        scanner2.rotate(Beacon.rotations()[k])
                        print(f'Found {j}!')
                        print(scanner2.position)
                        found += 1
                print(max_len)
        if not found:
            break #scanners[4].position = Beacon(500000,500000,500000)

    beacons = []
    for scanner in scanners.values():
        if scanner.position:
            beacons += [scanner.position + beacon for beacon in scanner.beacons]
    print(len(list(set(beacons))))

    # i = 0
    # j = 1
    # scanner1 = scanners[i]
    # scanner2 = scanners[j]
    # overlap = scanner1.overlap(scanner2)
    # # print(overlap)
    # print(f'Trying {(i,j)}')
    # for k in range(24):
    #     pairs = list(set(overlap[k]))
    #     if len(pairs) >= 12:
    #         print(k)
    #         # print(pairs)
    #         print(len(pairs))
    #         print(pairs[0])
    #         delta = pairs[0][0] - pairs[0][1]
    #         # print()
    #         # print(pairs[0][1])
    #         # for rotation in Beacon.rotations():
    #         #     print(pairs[0][1].rotate(rotation))
    #         # print()
    #         print(delta)
    #         scanner2.position = scanner1.position + delta
    #         scanner2.rotate(Beacon.rotations()[k])
    #         print(f'Found {j}!')
    #         print(scanner2.position)

    # i = 1
    # j = 4
    # scanner1 = scanners[i]
    # scanner2 = scanners[j]
    # overlap = scanner1.overlap(scanner2)
    # print(f'Trying {(i,j)}')
    # for k in range(24):
    #     pairs = list(set(overlap[k]))
    #     if len(pairs) >= 12:
    #         print(k)
    #         # print(pairs)
    #         print(len(pairs))
    #         print(pairs[0])
    #         delta = pairs[0][0] - pairs[0][1]
    #         print(delta)
    #         scanner2.position = scanner1.position + delta
    #         scanner2.rotate(Beacon.rotations()[k])
    #         print(f'Found {j}!')
    #         print(scanner2.position)
