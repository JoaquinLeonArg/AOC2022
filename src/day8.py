"""
--- Day 8: Treetop Tree House ---

The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

    The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
    The top-middle 5 is visible from the top and right.
    The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
    The left-middle 5 is visible, but only from the right.
    The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
    The right-middle 3 is visible from the right.
    In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

--- Part Two ---

Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

    Looking up, its view is not blocked; it can see 1 tree (of height 3).
    Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
    Looking right, its view is not blocked; it can see 2 trees.
    Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

    Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
    Looking left, its view is not blocked; it can see 2 trees.
    Looking down, its view is also not blocked; it can see 1 tree.
    Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?


"""

from typing import List
from utils import format_output, parse_input
from math import prod


def is_visible_from_side(iterable: List[int], height: int):
    for _, height_off in enumerate(iterable):
        if height_off >= height:
            break
    else:
        return True
    return False


def scenic_score_from_side(iterable: List[int], height: int):
    count = 0
    for _, height_off in enumerate(iterable):
        count += 1
        if height_off >= height:
            break
    else:
        return count
    return count


def is_visible(grid: List[List[int]], x: int, y: int, height: int) -> bool:
    return not all([not is_visible_from_side(iterable, height) for iterable in [
        grid[y][:x],
        grid[y][x+1:],
        [row[x] for _, row in enumerate(grid[:y])],
        [row[x] for _, row in enumerate(grid[y+1:])]
    ]])


def scenic_score(grid: List[List[int]], x: int, y: int, height: int) -> bool:
    return prod([scenic_score_from_side(iterable, height) for iterable in [
        grid[y][:x][::-1],  # Invert the list so we start from our current tree
        grid[y][x+1:],
        [row[x] for _, row in enumerate(grid[:y])][::-1],  # Same here
        [row[x] for _, row in enumerate(grid[y+1:])]
    ]])


def runA() -> int:
    # Count how many trees are visible from the sides of the grid
    grid = parse_input("day8.txt", transformation_functions=[
                       lambda x: [int(i) for i in x]])[0]
    grid = [x[0] for x in grid]  # Remove extra lists

    return sum([is_visible(grid, x, y, height) for y, row in enumerate(grid) for x, height in enumerate(row)])


def runB() -> int:
    # Get the highest scenic score possible
    grid = parse_input("day8.txt", transformation_functions=[
                       lambda x: [int(i) for i in x]])[0]
    grid = [x[0] for x in grid]  # Remove extra lists

    return max([scenic_score(grid, x, y, height) for y, row in enumerate(grid) for x, height in enumerate(row)])


if __name__ == "__main__":
    format_output(day=8, part=1, result=runA())
    format_output(day=8, part=2, result=runB())
