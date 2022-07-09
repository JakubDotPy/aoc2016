import argparse
import collections
import os.path
import re

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


def check_room(room_str):
    """return code, if room ok, 0 otherwise"""

    code_as_sep = re.findall(sector_re, room_str)[0]
    room_chars, code, check_str = room_str.partition(code_as_sep)

    code = int(code)
    check_str = check_str[1:-1]
    room_chars = ''.join(re.findall(room_chars_re, room_chars))
    room_chars = ''.join(sorted(room_chars))
    most_common_chars = collections.Counter(room_chars).most_common(5)
    most_common_str = ''.join(t[0] for t in most_common_chars)

    return code if most_common_str == check_str else 0


def compute(s: str) -> int:
    total_sum = 0
    lines = s.splitlines()
    for line in lines:
        total_sum += check_room(line)

    return total_sum


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
