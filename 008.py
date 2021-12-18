#!/usr/bin/env python3

def count_unique(output_values):
    print(output_values)
    ones = len(list(filter(lambda x: 2 == len(x), output_values)))
    fours = len(list(filter(lambda x: 4 == len(x), output_values)))
    sevens = len(list(filter(lambda x: 3 == len(x), output_values)))
    eights = len(list(filter(lambda x: 7 == len(x), output_values)))

    return ones + fours + sevens + eights

class SevenSegmentDisplay:
    def __init__(self, signal_patterns):
        self.signal_patterns = [''.join(sorted(pattern)) for pattern in signal_patterns]

        self.nums = {}
        self.segments = {}
        self.segment_map = {}

        self.nums[1] = set(list(filter(lambda x: 2 == len(x), self.signal_patterns))[0])
        self.segment_map[''.join(sorted(self.nums[1]))] = 1

        self.nums[4] = set(list(filter(lambda x: 4 == len(x), self.signal_patterns))[0])
        self.segment_map[''.join(sorted(self.nums[4]))] = 4

        self.nums[7] = set(list(filter(lambda x: 3 == len(x), self.signal_patterns))[0])
        self.segment_map[''.join(sorted(self.nums[7]))] = 7

        self.nums[8] = set(list(filter(lambda x: 7 == len(x), self.signal_patterns))[0])
        self.segment_map[''.join(sorted(self.nums[8]))] = 8

        others = {
            5: [set(pattern) for pattern in filter(lambda x: 5 == len(x), self.signal_patterns)],
            6: [set(pattern) for pattern in filter(lambda x: 6 == len(x), self.signal_patterns)],
        }

        self.segments['a'] = self.nums[1] ^ self.nums[7]

        # figure out 0, 6, 9
        almost_nine = self.nums[4] | self.nums[7]
        for six in others[6]:
            tmp = almost_nine ^ six
            if 1 == len(tmp):
                self.segments['g'] = tmp
                self.segment_map[''.join(sorted(six))] = 9
                self.nums[9] = six
            tmp2 = self.nums[1] & six
            if 1 == len(tmp2):
                self.segments['c'] = self.nums[1] ^ tmp2
                self.segment_map[''.join(sorted(six))] = 6
                self.nums[6] = six

        others[6].remove(self.nums[9])
        others[6].remove(self.nums[6])
        self.nums[0] = others[6][0]
        self.segment_map[''.join(sorted(self.nums[0]))] = 0

        self.segments['e'] = self.nums[8] ^ self.nums[9]
        self.segments['d'] = self.nums[8] ^ self.nums[0]

        self.segments['b'] = self.nums[4] ^ (self.nums[1] | self.segments['d'])
        self.segments['f'] = self.nums[1] - self.segments['c']

        # figure out 2,3,5
        self.nums[2] = self.segments['a'] | self.segments['c'] | self.segments['d'] | self.segments['e'] | self.segments['g']
        self.segment_map[''.join(sorted(self.nums[2]))] = 2

        self.nums[3] = self.segments['a'] | self.segments['c'] | self.segments['d'] | self.segments['f'] | self.segments['g']
        self.segment_map[''.join(sorted(self.nums[3]))] = 3

        self.nums[5] = self.nums[6] - self.segments['e']
        self.segment_map[''.join(sorted(self.nums[5]))] = 5

        # print(self.nums)
        # print(self.segments)
        # print(self.segment_map)

    def decode(self, output_values):
        # print(output_values)
        values = [self.segment_map[''.join(sorted(value))] for value in output_values]
        # print(values)
        return int(''.join([str(value) for value in values]))

if '__main__' == __name__:
    done = False
    data = {}

    while not done:
        try:
            line = input()
            (signal_patterns, output_values) = line.split(' | ')
            signal_patterns = signal_patterns.split(' ')
            output_values = output_values.split(' ')
            data[tuple(signal_patterns)] = output_values

        except:
            done = True

    total = 0
    #v print(data)
    for (signal_patterns, output_values) in data.items():
        # total += count_unique(output_values)
        ssd = SevenSegmentDisplay(signal_patterns)
        total += ssd.decode(output_values)
    print(total)
