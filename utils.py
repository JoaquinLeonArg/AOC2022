from typing import Callable, List

def parse_input(file_name: str, transformation_function: Callable[[str], any] = int) -> List[List[int]]:
    with open(file_name, "r") as file:
        return [[transformation_function(calories) for calories in elf.split("\n")] for elf in file.read().split("\n\n")]

def format_output(day: int, part: int, result: any):
    print(f'[AOC 2022 / DAY {day} / PART {part}] Response: {result}')