import argparse
import collections
import os.path
from itertools import chain
from itertools import product

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""
EXPECTED = 6


class Display:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.grid = [[False] * width for _ in range(height)]

    def light_rect(self, w, h):
        coords = product(range(w), range(h))
        for x, y in coords:
            self.grid[y][x] = True

    def rot_row(self, row_n, rot_n):
        d = collections.deque(self.grid[row_n])
        d.rotate(rot_n)
        self.grid[row_n] = list(d)

    def rot_col(self, col_n, rot_n):
        d = collections.deque(row[col_n] for row in self.grid)
        d.rotate(rot_n)
        for row, deque_val in zip(self.grid, d):
            row[col_n] = deque_val

    @property
    def total_on(self):
        return sum(chain.from_iterable(self.grid))

    def __str__(self):
        return '\n'.join(
            ''.join('#' if c else '.' for c in row)
            for row in self.grid
            )


def compute(s: str) -> int:
    disp = Display(50, 6)
    # print(disp)

    for line in s.splitlines():
        match line.split():
            case ['rect', dims]:
                disp.light_rect(*map(int, dims.split('x')))
            case ['rotate', ('column' | 'row') as part, num_str, 'by', rot_str]:
                part_to_method = {
                    'column': disp.rot_col,
                    'row'   : disp.rot_row,
                    }
                part_num = int(num_str.split('=')[-1])
                rot_num = int(rot_str)
                part_to_method[part](part_num, rot_num)
            case _:
                raise ValueError('Unknown command')
    print(disp)

    return disp.total_on


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
