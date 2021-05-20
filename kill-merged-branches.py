#!/usr/bin/env python3

from argparse import ArgumentParser
import subprocess
import locale
import sys

enc = locale.getpreferredencoding()
default_exclusions = 'main,master'


def grab(cmd_parts):
    res = subprocess.run(cmd_parts, capture_output=True, check=True,
                         encoding=enc)
    return res.stdout


def get_args():
    top = ArgumentParser('kill-merged-branches')
    top.add_argument('-x', '--exclude',
                     default=default_exclusions,
                     help=('Branches to ignore, separated by commas. '
                           f'Defaults to "{default_exclusions}".'))
    return top.parse_args()


def main(args):
    branches = grab(['git', 'branch', '--merged'])
    exclusions = [e.strip() for e in args.exclude.split(',') if len(e) > 0]
    print(f'Excluding these branches: {exclusions}')
    deletable = [b.strip() for b in branches.split('\n')
                 if not (b.startswith('*')
                         or len(b) < 1
                         or b.strip() in exclusions)]
    if len(deletable) < 1:
        print('No branches found for cleanup')
        sys.exit(0)
    print('Found these merged branches to delete:')
    for branch in deletable:
        print(branch)

    if (input('Continue? [y/n]: ') == 'y'):
        for branch in deletable:
            if (len(branch) < 1):
                continue
            cmd = ['git', 'branch', '-d', branch]
            subprocess.run(cmd, capture_output=False, check=True)
    else:
        print('No changes were made')


if __name__ == '__main__':
    main(get_args())
