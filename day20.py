#!/usr/bin/env python3

class ImageEnhancementAlgorithm:
    def __init__(self, bits):
        self.bits = bits

    def decode(self, pixels):
        # convert to bits
        bits = ['0' if '.' == pixel else '1' for pixel in pixels]
        # convert from binary
        value = int(''.join(bits), 2)
        # print(pixels, value, self.bits[value])
        # return relevant character in self.bits
        return self.bits[value]

    def __str__(self):
        return self.bits
    
    def __repr__(self):
        return str(self)

class Trench:
    def __init__(self, rows, algorithm, pad_bit='.'):
        # print(rows)
        self.rows = rows
        self.algorithm = algorithm
        self.padded = 0
        self.pad_bit = pad_bit
        self.pad()
        self.pad()
    
    def pad(self):
        self.padded += 1
        self.rows.insert(0, self.pad_bit * len(self.rows[0]))
        self.rows.append(self.pad_bit * len(self.rows[0]))
        for i in range(len(self.rows)):
            self.rows[i] = f'{self.pad_bit}{self.rows[i]}{self.pad_bit}'

    def get(self, x, y):
        # print(x,y)
        if y not in range(len(self.rows)):
            return self.pad_bit
        if x not in range(len(self.rows[y])):
            return self.pad_bit
        return self.rows[y][x]
        
    def surrounding(self, x, y):
        return \
            self.get(x-1,y-1) + self.get(x,y-1) + self.get(x+1,y-1) + \
            self.get(x-1,y)   + self.get(x,y)   + self.get(x+1,y)   + \
            self.get(x-1,y+1) + self.get(x,y+1) + self.get(x+1,y+1) 

    def enhance(self):
        rows = []

        ignore = 1

        for y in range(len(self.rows)):
            row = ''
            for x in range(len(self.rows[y])):
                row += self.algorithm.decode(self.surrounding(x,y))
            rows.append(row[ignore:len(row)-ignore])
        return Trench(rows[ignore:len(rows)-ignore], self.algorithm, rows[0][0])

    def count_lit(self):
        count = 0
        for y in range(len(self.rows)):
            count += self.rows[y].count('#')
        return count

    def __str__(self):
        return '\n'.join(self.rows)
    
    def __repr__(self):
        return self.rows

if '__main__' == __name__:
    done = False

    algorithm = None
    trench_rows = []
    while not done:
        try:
            line = input()
            if not line:
                continue
            if not algorithm:
                algorithm = ImageEnhancementAlgorithm(line)
                continue
            trench_rows.append(line)
        except:
            done = True

    #print(algorithm)
    #print()
    trench = Trench(trench_rows, algorithm)

    print(trench)
    print(trench.count_lit())
    print()

    # print(trench.get(0,0))
    # print(trench.get(-10,-10))
    # print(trench.surrounding(0,0))
    # print(trench.surrounding(-10,-10))

    for i in range(50):
        trench = trench.enhance()
        # print(trench)
        print(trench.count_lit())
        # print()

    # trench = trench.enhance()
    # print(trench)
    # print(trench.count_lit())

    # print(algorithm.decode('...#...#.'))

    # print(trench.get(2,2))
    # print(trench.surrounding(2,2))

