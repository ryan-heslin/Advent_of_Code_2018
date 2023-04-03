from collections import deque
from math import ceil
from math import inf

from utils import timecode


class CountedProgram(timecode.Program):
    def exec(self):
        pointer = 0
        stop = len(self.code)
        instruction_register = self.instruction_register
        states = set()

        new = previous = oldest = None
        counter = 0
        while 0 <= pointer < stop:
            # if pointer == 28:
            #     breakpoint()
            counter += 1
            if pointer == 18:
                self.registers[2] = 1
                self.registers[3] = 17
                self.registers[5] = self.registers[1] // 256
                pointer = 26
            else:
                if pointer == 28:
                    # first = False
                    # The one before the last new insertion - what?
                    # This doesn't make sense, and yet
                    new = self.registers[4]
                    record = (self.registers[1], new)
                    if record in states:
                        return oldest
                    states.add(record)
                    oldest = previous
                    # print(new)
                    # if record in states:
                    #     return counter
                    previous = new
                self.registers[self.instruction_register] = pointer
                self.registers = self.code[pointer](self.registers)
                pointer = self.registers[instruction_register] + 1
        return counter


def find_shortest(program):
    best = inf
    integer = None
    # (641049, 8164934)
    for i in range(1000):
        program.reset()
        program.registers[0] = i
        result = program.exec()
        print(result)

    return integer


with open("inputs/day21.txt") as f:
    raw_input = f.read().splitlines()

program = CountedProgram(n_registers=6)
program.compile(raw_input)

part1 = find_shortest(program)
print(part1)

# Loop 18-25
# Only runs once if register 0 > 256
# 33 sets 4 to 1 if reg 0 == reg4; probable loop
# 3 incremented by 1 on line 3,then zeroed
# 4 zeroed
# Register 0 read only once in program, line 31
# Loop break line :
# seti 27 8 3
# 0 must be smallest number greater than whatever 4 ends up as
# 14738375 too high
