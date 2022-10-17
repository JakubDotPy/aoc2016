import argparse
import os.path
from copy import copy

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
20 10000
"""
EXPECTED = '01100'


def do_rolover(a):
    b = copy(a)
    b = b[::-1]
    b = ''.join('1' if c == '0' else '0' for c in b)
    return a + '0' + b


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args, strict=True)


def reduce_checksum(str_in):
    return ''.join(
        '1' if a == b else '0'
        for a, b in grouper(str_in, 2)
    )


def compute(s: str) -> int:
    disk_size_str, initial = s.split()
    disk_size = int(disk_size_str)

    while len(initial) <= disk_size:
        initial = do_rolover(initial)

    disk_chars = initial[:disk_size]

    while True:
        try:
            disk_chars = reduce_checksum(disk_chars)
        except ValueError:
            break

    return disk_chars


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
