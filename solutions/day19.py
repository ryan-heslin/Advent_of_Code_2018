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


# Inner loop counts up once per iteration
# from 1 to 10551383
# One of these likely breaks loop
# Last instruction sets pointer to 0, so loop only terminates with pointer setting
# Inner loop runs 983 times, counting
# from 10551383 to 10550400
# Outer loop runs inner loop 10551383 times
# Loop runs 10551383 ^2 times in all before exiting
# SO how many times does addr 2 0 0 in inner loop run?
# FInal break comes on skipping seti here:

# gtrr 2 1 3
# addr 3 5 5
# seti 1 1 5
# mulr 5 5 5
# Presume it counts primes, composites, or divisors up to 10551383
# 10551383 too low
# Summing numbers up to that number?
