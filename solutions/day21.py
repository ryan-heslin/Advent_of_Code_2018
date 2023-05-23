from utils import timecode

with open("inputs/day21.txt") as f:
    raw_input = f.read().splitlines()

loop_start = 18
loop_end = 26
offset = 1
instruction_register = int(raw_input[0].split(" ")[1])
loop_multiplier = int(raw_input[loop_start + 2].split(" ")[2])
pointer_reset = int(raw_input[loop_end].split(" ")[1])
exit_line = [i for i, line in enumerate(raw_input) if "0" in line.split(" ")][-1] - 1


class CountedProgram(timecode.Program):
    def exec(self):
        pointer = 0
        stop = len(self.code)
        instruction_register = self.instruction_register
        states = set()

        new = previous = oldest = None
        first_seen = False
        part1 = None

        while 0 <= pointer < stop:
            if pointer == loop_start:
                self.registers[2] = 1
                self.registers[instruction_register] = pointer_reset
                self.registers[5] = self.registers[1] // loop_multiplier
                pointer = loop_end
            else:
                if pointer == exit_line:
                    # The one before the last new insertion - what?
                    # This doesn't make sense, and yet
                    new = self.registers[4]
                    record = (self.registers[1], new)
                    if not first_seen:
                        part1 = new
                        first_seen = True
                    if record in states:
                        return part1, oldest
                    states.add(record)
                    oldest = previous
                    previous = new
                self.registers[self.instruction_register] = pointer
                self.registers = self.code[pointer](self.registers)
                pointer = self.registers[instruction_register] + 1


program = CountedProgram(n_registers=6)
program.compile(raw_input)

program.registers[0] = None
part1, part2 = program.exec()
print(part1)
print(part2)
