from __future__ import annotations

import argparse
import contextlib
import re
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Generator


@contextlib.contextmanager
def timing(name: str = '') -> Generator[None, None, None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = 'ms'
        if t < 100:
            t *= 1000
            unit = 'μs'
        if name:
            name = f' ({name})'
        print(f'> {int(t)} {unit}{name}')


def get_input(year: int, day: int) -> str:
    with open('../../.env') as f:
        contents = f.read()

    url = f'https://adventofcode.com/{year}/day/{day}/input'
    req = urllib.request.Request(url, headers={'Cookie': contents.strip()})
    return urllib.request.urlopen(req).read().decode()


def download_input() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int)
    parser.add_argument('day', type=int)
    args = parser.parse_args()

    for i in range(5):
        try:
            s = get_input(args.year, args.day)
        except urllib.error.URLError as e:
            print(f'zzz: not ready yet: {e}')
            time.sleep(1)
        else:
            break
    else:
        raise SystemExit('timed out after attempting many times')

    with open('input.txt', 'w') as f:
        f.write(s)

    lines = s.splitlines()
    if len(lines) > 10:
        for line in lines[:10]:
            print(line)
        print('...')
    else:
        print(lines[0][:80])
        print('...')

    return 0


def new_day() -> None:
    print(' Creating new advent day '.center(50, '-'))

    temp_dir = Path('day00').absolute()

    # find number of last day
    last_day = sorted(
        folder.name
        for folder in Path().iterdir()
        if folder.is_dir() and folder.name.startswith('day')
        )[-1]

    print(f'Last day is {last_day}.')

    # prepare the paths
    last_day_num = int(re.findall(r'\d+', last_day)[0])
    new_day_num = last_day_num + 1
    new_day_folder_name = f'day{new_day_num:02}'
    new_path = Path(new_day_folder_name).absolute()

    # copy folder
    print(f"Creating folder '{new_day_folder_name}'.")
    shutil.copytree(temp_dir, new_path)

    # edit run configurations
    print('Editing run configuration.')
    for file in Path('.run').iterdir():
        print(f' - editing {file}')
        with open(file, 'r') as f:
            contents = f.read()
            new_contents = re.sub(
                fr'{last_day}', fr'{new_day_folder_name}', contents
                )
        with open(file, 'w') as f:
            f.write(new_contents)

    print(' Finished '.center(50, '-'))
