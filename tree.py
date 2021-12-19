#!/usr/bin/env python3

DEBUG=False
# DEBUG=True

def dprint(*args):
    if DEBUG:
        print(*args)

class Tree:
    def __init__(self, left=None, right=None, value=None):
        self.value = value

        self.parent = None
        self.is_left = False
        self.is_right = False
        self.add_left(left)
        self.add_right(right)
    
    def add_left(self, left):
        self.left = left
        if self.left:
            self.left.parent = self
            self.left.is_left = True
            self.left.is_right = False

    def add_right(self, right):
        self.right = right
        if self.right:
            self.right.parent=self
            self.right.is_right = True
            self.right.is_left = False

    def is_root(self):
        return None == self.parent

    def is_leaf(self):
        return None == self.left and None == self.right
    
    def leftmost(self):
        if self.is_leaf():
            return self
        return self.left.leftmost() if self.left else self.right.leftmost()

    def rightmost(self):
        if self.is_leaf():
            return self
        return self.right.rightmost() if self.right else self.left.rightmost()

    def left_of(self):
        if self.is_right:
            return self.parent.left.rightmost()
        if self.parent.is_root():
            return None
        return self.parent.left_of()

    def right_of(self):
        if self.is_left:
            return self.parent.right.leftmost()
        if self.parent.is_root():
            return None
        return self.parent.right_of()

    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        if self.value:
            return str([self.left, self.value, self.right])
        return str([self.left, self.right])
        
    def __repr__(self):
        return str(self)

if '__main__' == __name__:
    leaves = {key:Tree(value=key) for key in range(11)}
    print(leaves[0])

    # [[0,[[1,2],[3,[4,5]]]],[[[6,7],8],[9,10]]]
    tree = Tree(
        Tree(
            leaves[0],
            Tree(
                Tree(
                    leaves[1],
                    leaves[2]
                ),
                Tree(
                    leaves[3],
                    Tree(
                        leaves[4],
                        leaves[5]
                    )
                )
            )
        ),
        Tree(
            Tree(
                Tree(
                    leaves[6],
                    leaves[7]
                ),
                leaves[8]
            ),
            Tree(
                leaves[9],
                leaves[10]
            )
        )
    )

    print(tree)
    for i in range(11):
        print(leaves[i].left_of(), leaves[i].right_of())
