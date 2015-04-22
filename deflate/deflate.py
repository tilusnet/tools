#!/usr/bin/env python3

import zlib, os, sys
import argparse
import textwrap
from thqpylib.fileio import FileIO

def get_parsed_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent('''\
            Deflate a file from STDIN.
            Alternatively processes all files in a directory.
            Decompressed output is directed to STDOUT.
        ''')
    )
    parser.add_argument(
        '-d', '--input-dir', dest='input_dir',
        help=textwrap.dedent('''\
           All files in the folder will be processed.
           WARNING: Each individual file will be loaded entirely in memory!
        ''')
    )
    return parser.parse_args()


def deflate(fo):
    '''Deflate file object 'fo' and return its string form.
       Decoding is in utf-8.
    '''
    return zlib.decompress(fo.read()).decode()


if __name__ == '__main__':
    myargs = get_parsed_args()
    inputdir = myargs.input_dir
    if inputdir:
        flist = FileIO().getFileList(inputdir)
        for ff in flist:
            with open(ff, mode='rb') as f:
                sys.stderr.write('\nDeflating "{}"...'.format(ff))
                try:
                    print(deflate(f))
                except:
                    sys.stderr.write(' FAILED; skipped.')
                    continue
                sys.stderr.write(' DONE.')
    else:
        sys.stderr.write('[i] Input is STDIN...\n')
        try:
            print(deflate(sys.stdin.buffer))
        except:
            sys.stderr.write('\n  [!] Failed to decompress; skipped.\n')
            raise
