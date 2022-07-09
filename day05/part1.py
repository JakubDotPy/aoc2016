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
EXPECTED = '18f47a30'


def compute(s: str) -> int:
    password = ''
    s = s.strip()

    cnt = itertools.count()
    while len(password) != 8:
        hash = md5(f'{s}{next(cnt)}'.encode('utf-8')).hexdigest()
        if hash[:5] == '00000':
            password += hash[5]

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
