import argparse
import itertools
import os.path
from hashlib import md5

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
abc
"""
EXPECTED = '05ace8e3'


def compute(s: str) -> int:
    password = [None] * 8
    s = s.strip()

    cnt = itertools.count()
    while None in password:
        hash = md5(f'{s}{next(cnt)}'.encode('utf-8')).hexdigest()
        if hash[:5] != '00000':
            continue
        try:
            position = int(hash[5])
            char = hash[6]
            if password[position] == None:
                password[position] = char
        except (IndexError, ValueError):
            pass

    return ''.join(password)


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
