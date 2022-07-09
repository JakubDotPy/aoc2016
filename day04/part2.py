import argparse
import os.path
import re
import string

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
"""
EXPECTED = 1514

room_chars_re = re.compile(r'[a-z]+')
sector_re = re.compile(r'\d+')


def caesar_cipher(n):
    az = string.ascii_lowercase
    x = n % len(az)
    return str.maketrans(az, az[x:] + az[:x])


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        chars = ''.join(re.findall(room_chars_re, line))
        code = int(re.findall(sector_re, line)[0])
        rotated = chars.translate(caesar_cipher(code))
        if 'north' in rotated:
            return code


@pytest.mark.solved
@pytest.mark.skip('no test provided')
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
