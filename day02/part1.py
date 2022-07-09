import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
ULL
RRDDD
LURDL
UUUUD
"""
EXPECTED = '1985'

# 123
# 456
# 789
keypad = {
    (-1, 1) : '1',
    (0, 1)  : '2',
    (1, 1)  : '3',
    (-1, 0) : '4',
    (0, 0)  : '5',
    (1, 0)  : '6',
    (-1, -1): '7',
    (0, -1) : '8',
    (1, -1) : '9',
    }

diffs = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1),
    }

position = (0, 0)


def apply_move(diff):
    global position
    x, y = position
    dx, dy = diff
    new_pos = x + dx, y + dy
    if new_pos in keypad:
        position = new_pos


def compute(s: str) -> int:
    password = ''
    lines = s.splitlines()
    for line in lines:
        for move in line:
            apply_move(diffs[move])
        password += keypad[position]
    return password


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
