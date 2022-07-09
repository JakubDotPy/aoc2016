import argparse
import os.path
from collections import deque

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""


def expand_diff(diff, mul):
    return diff[0] * mul, diff[1] * mul


def apply_move(pos, diff):
    x, y = pos
    dx, dy = diff
    return x + dx, y + dy


def compute(s: str) -> int:
    diffs = deque((
        (0, 1),  # facing north
        (1, 0),
        (0, -1),
        (-1, 0)
        ))

    rotations = {
        'R': -1,
        'L': 1
        }

    pos = (0, 0)  # starting pos

    for instruction in s.strip().split(', '):
        rot = instruction[0]
        mul = int(instruction[1:])

        diffs.rotate(rotations[rot])
        diff = expand_diff(diffs[0], mul)
        pos = apply_move(pos, diff)

    return abs(pos[0]) + abs(pos[1])


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('R2, L3', 5),
            ('R2, R2, R2', 2),
            ('R5, L5, R5, R3', 12),
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
