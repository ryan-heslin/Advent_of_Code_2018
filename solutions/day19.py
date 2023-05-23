from utils.timecode import Program


def sum_divisors(x):
    return sum((not x % i) * i for i in range(2, x // 2)) + 1 + x


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
target = program.registers[1]
part2 = sum_divisors(target)
print(part2)
