#!/usr/bin/env python

import sys, os
from granholm.session3 import courseRepo, repoDir

abs_path = sys.argv[1]  # Absolute path to repository
surname = os.path.basename(abs_path)

with repoDir(abs_path):
    repo = courseRepo(surname)
    if repo.check():
        print('PASS')
    else:
        print('FAIL')
