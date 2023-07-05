from utils import timecode

with open("inputs/day21.txt") as f:
    raw_input = f.read().splitlines()


def read_register(line):
    return int(line.split(" ")[-1])


loop_start = 18
loop_end = 26
offset = 1
instruction_register = int(raw_input[0].split(" ")[1])
loop_multiplier = int(raw_input[loop_start + 2].split(" ")[2])
pointer_reset = int(raw_input[loop_end].split(" ")[1])
exit_line = [i for i, line in enumerate(raw_input) if "0" in line.split(" ")][-1] - 1
increment_register = read_register(raw_input[20])
data_register = read_register(raw_input[25])
check_register = read_register(raw_input[exit_line - 1])
final_register = read_register(raw_input[1])


class CountedProgram(timecode.Program):
    def __init__(
        self,
        instruction_register,
        increment_register,
        data_register,
        check_register,
        final_register,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.instruction_register = instruction_register
        self.increment_register = increment_register
        self.data_register = data_register
        self.check_register = check_register
        self.final_register = final_register

    def exec(self):
        pointer = 0
        stop = len(self.code)
        instruction_register = self.instruction_register
        increment_register = self.increment_register
        data_register = self.data_register
        check_register = self.check_register
        final_register = self.final_register

        states = set()

        new = previous = oldest = None
        first_seen = False
        part1 = None

        while 0 <= pointer < stop:
            if pointer == loop_start:
                self.registers[increment_register] = 1
                self.registers[instruction_register] = pointer_reset
                self.registers[data_register] = (
                    self.registers[check_register] // loop_multiplier
                )
                pointer = loop_end
            else:
                if pointer == exit_line:
                    # The one before the last new insertion - what?
                    # This doesn't make sense, and yet
                    new = self.registers[final_register]
                    record = (self.registers[check_register], new)
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


program = CountedProgram(
    instruction_register=instruction_register,
    increment_register=increment_register,
    data_register=data_register,
    check_register=check_register,
    final_register=final_register,
    n_registers=6,
)
program.compile(raw_input)

program.registers[0] = None
part1, part2 = program.exec()
print(part1)
print(part2)
