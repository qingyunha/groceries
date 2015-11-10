import os, stat, time
from random import random

current_time = time.time()
_7days = 7 * 24 * 3600

def modify_files_mtime(path):
    files = os.listdir(path)
    for f in files:
        next_file = path + '/' + f
        st_mode = os.stat(next_file).st_mode
        mtime = current_time - random() * _7days
        os.utime(next_file, (mtime, mtime))

        if stat.S_ISDIR(st_mode):
            modify_files_mtime(next_file)


def modify_files_mtime2(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in dirnames + filenames:
            next_file = dirpath + '/' + f
            mtime = current_time - random() * _7days
            os.utime(next_file, (mtime, mtime))


if __name__ == '__main__':
    modify_files_mtime2('.')
