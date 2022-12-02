from typing import Callable, List


def parse_input(file_name: str, transformation_functions: List[Callable[[str], any]]) -> List[List[int]]:
    with open(file_name, "r") as file:
        return [[[transformation_functions[i](value) for i, value in enumerate(values.split(' '))]
                 for values in block.split("\n")]
                for block in file.read().split("\n\n")]


def format_output(day: int, part: int, result: any):
    print(f'[AOC 2022 / DAY {day} / PART {part}] Response: {result}')
