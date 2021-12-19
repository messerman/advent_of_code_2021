#!/usr/bin/env python3

def list_to_int(l, base=10):
    value = ''.join(map(str, l))
    return int(value, base)

def compute_rates(diagnostics):
    zeroes = {}
    ones = {}
    num_bits = len(diagnostics[0])

    for bit in range(num_bits):
        zeroes[bit] = 0
        ones[bit] = 0

    for diagnostic in diagnostics:
        for bit in range(num_bits):
            if '0' == diagnostic[bit]:
                zeroes[bit] += 1
            else:
                ones[bit] += 1

    gamma = []
    epsilon = []
    for bit in range(num_bits):
        if zeroes[bit] > ones[bit]:
            gamma.append('0')
            epsilon.append('1')
        else:
            gamma.append('1')
            epsilon.append('0')

    return (list_to_int(gamma, 2), list_to_int(epsilon, 2))

def count_values(l, place):
    values = {'0':0, '1':0}
    for item in l:
        values[item[place]] += 1
    return values

def life_support_values(diagnostics):
    oxygen = diagnostics.copy()
    c02 = diagnostics.copy()
    num_bits = len(diagnostics[0])

    for bit in range(num_bits):
        if len(oxygen) <= 1:
            break
        values = count_values(oxygen, bit)
        if values['0'] > values['1']:
            oxygen = list(filter(lambda x: '0' == x[bit], oxygen))
        else:
            oxygen = list(filter(lambda x: '1' == x[bit], oxygen))

    for bit in range(num_bits):
        if len(c02) <= 1:
            break
        values = count_values(c02, bit)
        if values['0'] > values['1']:
            c02 = list(filter(lambda x: '1' == x[bit], c02))
        else:
            c02 = list(filter(lambda x: '0' == x[bit], c02))
        
        # print(oxygen, c02)

    return (int(oxygen[0], 2), int(c02[0], 2))

if '__main__' == __name__:
    done = False

    diagnostics = []
    while not done:
        try:
            line = input()
            diagnostics.append(line)
        except:
            done = True

    (gamma, epsilon) = compute_rates(diagnostics)
    print(gamma * epsilon)

    (oxygen, c02) = life_support_values(diagnostics)
    print(oxygen, c02)
    print(oxygen * c02)
