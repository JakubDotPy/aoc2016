import argparse
import os.path
from collections import deque

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
"""

visited = set()
pos = (0, 0)  # starting pos


class Visited(Exception):
    pass


def expand_diff(diff, mul):
    return diff[0] * mul, diff[1] * mul


def apply_move(diff, n):
    global pos

    for _ in range(n):
        x, y = pos
        dx, dy = diff
        pos = x + dx, y + dy

        if pos in visited:
            raise Visited
        else:
            visited.add(pos)


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

    for instruction in s.strip().split(', '):
        rot = instruction[0]
        mul = int(instruction[1:])

        diffs.rotate(rotations[rot])
        try:
            apply_move(diffs[0], mul)
        except Visited:
            break

    return abs(pos[0]) + abs(pos[1])


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('R8, R4, R4, R8', 4),
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
