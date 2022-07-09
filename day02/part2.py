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
EXPECTED = '5DB3'

#     1
#   2 3 4
# 5 6 7 8 9
#   A B C
#     D
keypad = {
    (0, 2)  : '1',
    (-1, 1) : '2',
    (0, 1)  : '3',
    (1, 1)  : '4',
    (-2, 0) : '5',
    (-1, 0) : '6',
    (0, 0)  : '7',
    (1, 0)  : '8',
    (2, 0)  : '9',
    (-1, -1): 'A',
    (0, -1) : 'B',
    (1, -1) : 'C',
    (0, -2) : 'D',
    }

diffs = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1),
    }

position = (-2, 0)


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
