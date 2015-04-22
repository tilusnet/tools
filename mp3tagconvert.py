#!/usr/bin/env python3

import sys
from thqpylib.mp3tag import Mp3Tag
from thqpylib.fileio import FileIO

    
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: {} <path>|<.mp3>'.format(sys.argv[0]))
        sys.exit(2)

    m3_flist = FileIO().getFileList(sys.argv[1], ext='.mp3', ignore_ext_case=True)
    m3_flist.sort()
    fc = 0
    for f in m3_flist:
        fc += 1
        print('\n[{}/{}] Processing "{}"...'.format(fc, len(m3_flist), f))
        mp3tag = Mp3Tag(f)
        # mp3tag.setLogLevel(logging.DEBUG)
        mp3tag.convert(backup=False)
        # print(mp3tag.getLyrics())
