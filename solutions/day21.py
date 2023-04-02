from math import inf

from utils import timecode


class CountedProgram(timecode.Program):
    def exec(self):
        breakpoint()
        pointer = counter = 0
        stop = len(self.code)
        instruction_register = self.instruction_register

        while 0 <= pointer < stop:
            print(pointer)
            print(self.registers)
            self.registers[self.instruction_register] = pointer
            self.registers = self.code[pointer](self.registers)
            pointer = self.registers[instruction_register] + 1
            counter += 1

        return counter


def find_shortest(program):
    best = inf
    integer = None
    for i in range(1, 1000):
        print(i)
        program.reset()
        program.registers[0] = i
        print(program.registers)
        result = program.exec()
        if result < best:
            integer = i
            best = result

    return integer


with open("inputs/day21.txt") as f:
    raw_input = f.read().splitlines()

program = CountedProgram(n_registers=4)
program.compile(raw_input)

part1 = find_shortest(program)
print(part1)

# Loop 18-25
# 33 sets 4 to 1 if reg 0 == reg4; probable loop
# 3 incremented by 1 on line 3,then zeroed
# 4 zeroed
