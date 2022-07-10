import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""
EXPECTED = 42


class Computer:
    def __init__(self):
        self.registers = dict.fromkeys('abcd', 0)

    def eval_instruction(self, parts):
        match parts:
            case ['cpy', _from, _to]:
                try:
                    self.registers[_to] = self.registers[_from]
                except KeyError:
                    self.registers[_to] = int(_from)
            case ['inc', reg]:
                self.registers[reg] += 1
            case ['dec', reg]:
                self.registers[reg] -= 1
            case _:
                print(parts)
                raise ValueError('unknown instruction')


def compute(s: str) -> int:
    cmp = Computer()

    pointer = 0
    instructions = s.splitlines()

    while True:
        try:
            current_instr = instructions[pointer]
        except IndexError:
            # halting condition
            break
        inst_parts = current_instr.split()
        # process "jnz" instruction
        if inst_parts[0] == 'jnz':
            try:
                jmp_cond = cmp.registers[inst_parts[1]]
            except KeyError:
                jmp_cond = int(inst_parts[1])
            if jmp_cond != 0:  # jump
                pointer += int(inst_parts[2])
            else:  # progress
                pointer += 1
            continue

        cmp.eval_instruction(inst_parts)
        pointer += 1

    return cmp.registers['a']


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
