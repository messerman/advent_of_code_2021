#!/usr/bin/env python3

import math

from tree import Tree

DEBUG=False
# DEBUG=True

def dprint(*args):
    if DEBUG:
        print(*args)

class SnailfishTree(Tree):
    def __init__(self, left=None, right=None, value=None, depth=0):
        super().__init__(left, right, value)
        self.depth=depth

    def find_root(self):
        if self.is_root():
            return self
        return self.parent.find_root()

    def set_depth(self, depth=0):
        self.depth = depth
        max_depth = self.depth
        if self.left:
            max_depth = max(max_depth, self.left.set_depth(self.depth + 1))
        if self.right:
            max_depth = max(max_depth, self.right.set_depth(self.depth + 1))
        return max_depth

    @classmethod
    def from_list(cls, list_tree):
        if list != type(list_tree):
            return SnailfishTree(value=list_tree)
        (l, r) = list_tree
        left = SnailfishTree.from_list(l)
        right = SnailfishTree.from_list(r)
        return SnailfishTree(left, right)

    def to_list(self):
        return eval(str(self)) # TODO - be more efficient

    def explode(self):
        dprint(f'explode({self} - {self.depth})')
        if self.is_leaf() or not (self.left.is_leaf() and self.right.is_leaf()):
            print("this explode shouldn't happen")
            raise Exception
        
        left = self.left.left_of()
        right = self.right.right_of()

        if left:
            left.value += self.left.value
        if right:
            right.value += self.right.value

        self.left = None
        self.right = None
        self.value = 0

    def split(self):
        dprint(f'split({self})')
        if not self.is_leaf():
            print("this split shouldn't happen")
            raise Exception
        self.add_left(SnailfishTree(value=math.floor(self.value/2), depth=self.depth+1))
        self.add_right(SnailfishTree(value=math.ceil(self.value/2), depth=self.depth+1))
        self.value = None

    def reduce(self):
        # dprint(f'reduce({self})')
        dprint('---------------')
        while True:
            max_depth = self.set_depth()
            first = next = self.leftmost()
            dprint(self)

            # DFS, if depth > 4, explode
            if max_depth > 4:
                while next and next.depth <= 4:
                    next = next.right_of()
                if next:
                    next.parent.explode()
                    continue
            
            # DFS, if value > 9, split
            next = first
            while next and next.value <= 9:
                next = next.right_of()
            if next and next.value > 9:
                next.split()
                continue

            break

        return self

    def __add__(self, other):
        tree = SnailfishTree.from_list([self.to_list(), other.to_list()])
        return tree.reduce()

    def __radd__(self, other):
        self.reduce()
        return self

    def magnitude(self):
        if self.is_leaf():
            return self.value
        pop_pop = 3 * self.left.magnitude() + 2 * self.right.magnitude()
        return pop_pop

if '__main__' == __name__:
    done = False

    nums = []
    while not done:
        try:
            line = input()
            nums.append(SnailfishTree.from_list(eval(line)))
        except:
            done = True

    # for num in nums:
    #     print(num)

    # print(SnailfishTree.from_list([[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]).magnitude())

    total = sum(nums)
    print(total)
    print(total.magnitude())

    max_magnitude = 0
    for num1 in nums:
        for num2 in nums:
            if num1 == num2:
                continue
            max_magnitude = max(max_magnitude, (num1 + num2).magnitude())
            max_magnitude = max(max_magnitude, (num2 + num1).magnitude())
    print(max_magnitude)
