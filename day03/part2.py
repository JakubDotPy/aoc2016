import argparse
import os.path
from itertools import chain

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
"""


def valid_triangle(sides):
    s1, s2, s3 = sorted(sides)
    return s1 + s2 > s3


def grouper(iterable, n):
    # grouper('ABCDEFG', 3) --> ABC DEF
    args = [iter(iterable)] * n
    return zip(*args)


def transform_lines(sides):
    triplets = chain(grouper(sides, 3))
    return chain.from_iterable(tuple(zip(*t)) for t in triplets)


def compute(s: str) -> int:
    sides_old = [tuple(map(int, line.split())) for line in s.splitlines()]
    sides = transform_lines(sides_old)
    return sum(map(valid_triangle, sides))


@pytest.mark.complete
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 0),
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
