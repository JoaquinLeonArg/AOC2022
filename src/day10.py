"""
--- Day 10: Cathode-Ray Tube ---

You avoid the ropes, plunge into the river, and swim to shore.

The Elves yell something about meeting back up with them upriver, but the river is too loud to tell exactly what they're saying. They finish crossing the bridge and disappear from view.

Situations like this must be why the Elves prioritized getting the communication system on your handheld device working. You pull it out of your pack, but the amount of water slowly draining from a big crack in its screen tells you it probably won't be of much immediate use.

Unless, that is, you can design a replacement for the device's video system! It seems to be some kind of cathode-ray tube screen and simple CPU that are both driven by a precise clock circuit. The clock circuit ticks at a constant rate; each tick is called a cycle.

Start by figuring out the signal being sent by the CPU. The CPU has a single register, X, which starts with the value 1. It supports only two instructions:

    addx V takes two cycles to complete. After two cycles, the X register is increased by the value V. (V can be negative.)
    noop takes one cycle to complete. It has no other effect.

The CPU uses these instructions in a program (your puzzle input) to, somehow, tell the screen what to draw.

Consider the following small program:

noop
addx 3
addx -5

Execution of this program proceeds as follows:

    At the start of the first cycle, the noop instruction begins execution. During the first cycle, X is 1. After the first cycle, the noop instruction finishes execution, doing nothing.
    At the start of the second cycle, the addx 3 instruction begins execution. During the second cycle, X is still 1.
    During the third cycle, X is still 1. After the third cycle, the addx 3 instruction finishes execution, setting X to 4.
    At the start of the fourth cycle, the addx -5 instruction begins execution. During the fourth cycle, X is still 4.
    During the fifth cycle, X is still 4. After the fifth cycle, the addx -5 instruction finishes execution, setting X to -1.

Maybe you can learn something by looking at the value of the X register throughout execution. For now, consider the signal strength (the cycle number multiplied by the value of the X register) during the 20th cycle and every 40 cycles after that (that is, during the 20th, 60th, 100th, 140th, 180th, and 220th cycles).

For example, consider this larger program:

addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop

The interesting signal strengths can be determined as follows:

    During the 20th cycle, register X has the value 21, so the signal strength is 20 * 21 = 420. (The 20th cycle occurs in the middle of the second addx -1, so the value of register X is the starting value, 1, plus all of the other addx values up to that point: 1 + 15 - 11 + 6 - 3 + 5 - 1 - 8 + 13 + 4 = 21.)
    During the 60th cycle, register X has the value 19, so the signal strength is 60 * 19 = 1140.
    During the 100th cycle, register X has the value 18, so the signal strength is 100 * 18 = 1800.
    During the 140th cycle, register X has the value 21, so the signal strength is 140 * 21 = 2940.
    During the 180th cycle, register X has the value 16, so the signal strength is 180 * 16 = 2880.
    During the 220th cycle, register X has the value 18, so the signal strength is 220 * 18 = 3960.

The sum of these signal strengths is 13140.

Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles. What is the sum of these six signal strengths?

"""

from typing import List
from utils import format_output, parse_input
from abc import ABC, abstractmethod


class Operation(ABC):
    def __init__(self, cycles: int = 1):
        self.cycles = cycles

    def tick(self) -> bool:
        if self.cycles > 0:
            self.cycles -= 1
        if self.cycles == 0:
            return True

    @abstractmethod
    def execute(self, cycle, value) -> int:
        raise NotImplementedError


class NoopOperation(Operation):
    def __init__(self):
        super().__init__(1)

    def execute(self, cycle, value) -> int:
        return 0


class AddxOperation(Operation):
    def __init__(self, amount):
        super().__init__(2)
        self.amount = amount

    def execute(self, cycle, value) -> int:
        return self.amount


def simulate(operations: List[Operation], target_cycles: List[int]) -> int:
    cycle = 1
    value = 1
    result = 0

    while operations:
        current_operation = operations[0]
        if any([cycle == target for target in target_cycles]):
            result += cycle * value
            print(cycle, value, cycle*value)
        if current_operation.tick():
            value += current_operation.execute(cycle, value)
            operations.pop(0)
        cycle += 1

    return result


def draw_pixels(operations: List[Operation]) -> str:
    cycle = 0
    value = 1
    result = '\n'
    x_counter = 0
    y_counter = 0
    while not (y_counter == 5 and x_counter == 39):
        # Draw
        if abs(value - x_counter) <= 1:
            result += "#"
        else:
            result += '.'
        x_counter = (x_counter + 1) % 40
        y_counter = y_counter + (x_counter == 0)
        if x_counter == 0:
            result += '\n'

        # Operate
        current_operation = operations[0]
        if current_operation.tick():
            value += current_operation.execute(cycle, value)
            operations.pop(0)

    return result


def runA() -> int:
    # Simulate the operations and check signal strength on the given cycles
    lines = parse_input("day10.txt", [str, int], ' ')[0]
    operations = []
    for line in lines:
        if line[0] == 'noop':
            operations.append(NoopOperation())
        elif line[0] == 'addx':
            operations.append(AddxOperation(line[1]))
    return simulate(operations, target_cycles=[20, 60, 100, 140, 180, 220])


def runB() -> int:
    # Simulate the operations and draw the sprite
    lines = parse_input("day10.txt", [str, int], ' ')[0]
    operations = []
    for line in lines:
        if line[0] == 'noop':
            operations.append(NoopOperation())
        elif line[0] == 'addx':
            operations.append(AddxOperation(line[1]))
    return draw_pixels(operations)


if __name__ == "__main__":
    format_output(day=10, part=1, result=runA())
    format_output(day=10, part=2, result=runB())
