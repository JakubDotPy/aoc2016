import argparse
import os.path
import re

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""
EXPECTED = 2

abba_re = re.compile(r'(.)(.)\2(?!\2)\1')
bracket_ra = re.compile(r'\[(\w+)\]')


def check_line(line):
    abbas = tuple((m.start(0), m.end(0)) for m in re.finditer(abba_re, line))
    bracket_strs = tuple((m.start(1), m.end(1)) for m in re.finditer(bracket_ra, line))

    if not abbas:
        raise ValueError

    # check overlaps
    for abba_start, abba_end in abbas:
        for br_str_start, br_str_end in bracket_strs:
            if br_str_start <= abba_start <= br_str_end:
                # abba is in brackets
                raise ValueError


def compute(s: str) -> int:
    num_ok_lines = 0
    lines = s.splitlines()
    for line in lines:
        try:
            check_line(line)
            num_ok_lines += 1
        except ValueError:
            continue

    return num_ok_lines


# @pytest.mark.solved
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
