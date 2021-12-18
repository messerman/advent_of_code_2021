#!/usr/bin/env python3

from tree import Tree

DEBUG=False
#DEBUG=True

def dprint(*args):
    if DEBUG:
        print(*args)

class SnailfishTree(Tree):
    def __init__(self, left=None, right=None, value=None):
        super().__init__(left, right, value)
        self.depth = 0

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

    def reduce(self):
        dprint(self)
        max_depth = self.set_depth()
        first = next = self.leftmost()
        dprint(next.depth)

        # DFS, if depth > 4, explode
        while True:
            if max_depth > 4:
                while next.depth < 4:
                    next = next.right_of()
                print("TODO - explode!")
                dprint(next.find_root())
                # continue - TODO
            
            # DFS, if value > 9, split
            next = first
            while next and next.value < 9:
                next = next.right_of()
            if next and next.value > 9:
                print("TODO - split!")
                dprint(next)
                # continue - TODO
            break

        return self

    def __add__(self, other):
        tree = SnailfishTree.from_list([self.to_list(), other.to_list()])
        return tree.reduce()

    def __radd__(self, other):
        return self

    def magnitude(self):
        dprint(self)
        if self.is_leaf():
            return self.value
        pop_pop = 3 * self.left.magnitude() + 2 * self.right.magnitude()
        dprint(pop_pop)
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
