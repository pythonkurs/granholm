#!/usr/bin/env python

import sys, os
from granholm.session3 import courseRepo, repoDir

def main():
    index = 1
    if sys.argv[index][-13:] == 'check_repo.py':
        index += 1
    abs_path = sys.argv[index]  # Absolute path to repository (make sure there's no trailing slash)
    surname = os.path.basename(abs_path)

    with repoDir(abs_path):
        repo = courseRepo(surname)
        if repo.check():
            print('PASS')
        else:
            print('FAIL')

if __name__ == '__main__':
    main()
