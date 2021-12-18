#!/usr/bin/env python3

def validate_line(line):
    validity = {
        ')': '(',
        ']': '[',
        '}': '{',
        '>': '<',
    }
    closer = {value:key for (key, value) in validity.items()}

    stack = []
    for c in list(line):
        if c in '([{<':
            stack.append(c)
        elif c in ')]}>':
            last_open = stack.pop()
            if last_open != validity[c]:
                return c

    if stack:
        closes = [closer[c] for c in stack]
        closes.reverse()
        return closes
    
    return None

if '__main__' == __name__:
    done = False

    corrupted_lines = []
    corrupted_characters = []
    incomplete_lines = []
    valid_lines = []
    while not done:
        try:
            line = input()
            validity = validate_line(line)
            if None == validity:
                valid_lines.append(line)
            elif list == type(validity):
                incomplete_lines.append(validity)
            else:
                corrupted_lines.append(line)
                corrupted_characters.append(validity)
        except:
            done = True

    scoring = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    print(valid_lines)
    print(incomplete_lines)
    print(corrupted_lines)
    print(corrupted_characters)

    score = 0
    for c in corrupted_characters:
        score += scoring[c]
    print(score)

    scoring2 = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    scores = []
    for line in incomplete_lines:
        score2 = 0
        for c in line:
            score2 = score2 * 5 + scoring2[c]
        scores.append(score2)

    print(scores)
    scores.sort()
    print(scores[len(scores)//2])
