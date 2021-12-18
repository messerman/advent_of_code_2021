#!/usr/bin/env python3

import math
import sys
import time

def insertion(polymer, rules):
    output = polymer[0]
    for i in range(1, len(polymer)):
        rule = polymer[i-1:i+1]
        output += rules[rule] + polymer[i]
    return output

def smarter_insertion(polymer, rules):
    # print('--> ' + polymer)
    if len(polymer) <= 1:
        # print("<-- no")
        return polymer
    if polymer in rules:
        # print('<-- ' + polymer + ': ' + rules[polymer])
        return polymer[0] + rules[polymer] + polymer[-1]
    # output = smarter_insertion(polymer[0:2], rules)[:-1] + smarter_insertion(polymer[1:-1], rules) + smarter_insertion(polymer[-2:], rules)[1:]
    # output = smarter_insertion(polymer[0:index+1], rules)[1:-1] + polymer[index] + smarter_insertion(polymer[index:], rules)[1:-1]
    output = polymer[0]
    for index in range(2, len(polymer)):
        rule = polymer[0:index]
        if rule in rules:
            output = polymer[0] + rules[rule]
            # print(f'{index}: found rule {rule}, new output is {output}')
        else:
            break

    output += smarter_insertion(polymer[len(output)-1:], rules)

    # print('<-- ' + polymer + ': ' + output)
    rules[polymer] = output[1:-1]
    return polymer[0] + rules[polymer] + polymer[-1]

def replace_insertion(polymer, rules):
    pairs = [polymer[i:i+2] for i in range(len(polymer)-1)]
    output = [pair[0] + rules[pair] for pair in pairs]
    output += polymer[-1]
    return ''.join(output)

def count_insertion(counts, rules, letter_counts):
    counts2 = {pair:0 for pair in counts.keys()}
    for pair,inside in rules.items():
        increase = counts[pair]
        letter_counts[inside] += increase
        counts2[pair[0] + inside] += increase
        counts2[inside + pair[1]] += increase
    return counts2

if '__main__' == __name__:
    done = False

    polymer = None
    rules = {}
    letters = ''
    while not done:
        try:
            line = input()
            if not line:
                continue
            elif polymer:
                a,b = line.split(' -> ')
                rules[a] = b #a[0] + b + a[1]
                letters += a
                letters += b
            else:
                polymer = line #list(line)
                letters += line
        except:
            done = True

    print(''.join(polymer))
    print(rules)

    pairs = [polymer[i:i+2] for i in range(len(polymer)-1)]
    counts = counts = {rule:pairs.count(rule) for rule in rules.keys()}
    letter_counts = {letter:polymer.count(letter) for letter in set(letters)}
    # print(counts)
    for i in range(40):
        counts = count_insertion(counts, rules, letter_counts)
        # print(counts)

    print(letter_counts)
    max_count = 0
    min_count = sys.maxsize
    for letter,count in letter_counts.items():
        max_count = max(max_count, count)
        min_count = min(min_count, count)
    print(max_count - min_count)

    # letter_counts = {letter:0 for letter in set(letters)}
    # for pair,count in counts.items():
    #     letter_counts[pair[0]] += count
    #     letter_counts[pair[1]] += count

    # totals = {letter:math.ceil(count/2) for (letter,count) in letter_counts.items()}
    # print(totals)
    # max_count = 0
    # min_count = sys.maxsize
    # for letter,count in totals.items():
    #     max_count = max(max_count, count)
    #     min_count = min(min_count, count)
    # print(max_count - min_count)


    # for i in range(0):
    #     start = time.time()
    #     print(i)
    #     # polymer = smarter_insertion(polymer, rules)
    #     # polymer = replace_insertion(polymer, rules)
    #     print(time.time() - start)
    #     # print(polymer)
    #     # print(rules)

    # max_count = 0
    # min_count = sys.maxsize
    # for c in set(letters):
    #     count = polymer.count(c)
    #     print(f'{c}: {count}')
    #     max_count = max(max_count, count)
    #     min_count = min(min_count, count)
    # print(max_count - min_count)
