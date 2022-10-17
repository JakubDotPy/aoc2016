import argparse
import os.path
import re
from collections import deque
from itertools import count

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""
EXPECTED = 5


def compute(s: str) -> int:
    # parse lines
    lines = s.splitlines()

    disks = []
    for line in lines:
        disk_num, num_positions, time, init_pos = tuple(map(int, re.findall(r'\d+', line)))
        # prepare disk
        disk = deque(range(num_positions))
        # advance to initial pos
        disk.rotate(-init_pos)

        # move back position places
        disk.rotate(-disk_num)

        disks.append(disk)

    # disc 11
    disk = deque(range(11))
    disk.rotate(-(disk_num + 1))
    disks.append(disk)

    for i in count(0):
        nums = [d[0] for d in disks]
        if all(num == 0 for num in nums):
            return i
        for disk in disks:
            disk.rotate(-1)

    return 0


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
