from math import ceil

from utils.timecode import Program


def sum_divisors(x):
    return sum((not x % i) * i for i in range(2, ceil(x / 2) + 1)) + 1 + x


with open("inputs/day19.txt") as f:
    raw_input = f.read().splitlines()

n_registers = 6

program = Program(n_registers)
program.compile(raw_input)
program.exec()
part1 = program.registers[0]
print(part1)

program.reset()
program.registers[0] = 1
program.exec(stop_val=2)
# Yes, it varies by input
register = int(raw_input[19].split(" ")[-1])
target = program.registers[register]
part2 = sum_divisors(target)
print(part2)
