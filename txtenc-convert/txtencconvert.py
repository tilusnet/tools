#!/usr/bin/env python3

from __future__ import print_function
import os
import argparse
import json
from subprocess import check_output
from thqpylib.fileio import FileIO
from thqpylib.txtencoding import TxtEncoding


def get_parsed_args():
    parser = argparse.ArgumentParser(description='Yet another file encoding converter.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')

    # display subcommand
    subparsers.add_parser('display', aliases=['d', 'disp'],
                          formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                          help='Display detected file encodings.',
                          description='Display detected file encodings.'
    )

    # conversion subcommand
    conv_p = subparsers.add_parser('convert', aliases=['c', 'co'],
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                   help='Convert file encodings.',
                                   description='Convert file encodings.'
    )
    group_detect = conv_p.add_mutually_exclusive_group()
    group_detect.add_argument('-f', '--from-encoding', dest='fromenc',
                              help='Specify original encoding explicitly. If not provided, will attempt to detect.'
    )
    group_detect.add_argument('--confidence', default=0.8, type=float,
                              help='Encoding detection confidence threshold with values between 0 and 1. \
                                    Files won\'t be converted if detection confidence is below this level.'
    )
    conv_p.add_argument('-t', '--to-encoding', dest='toenc', default='utf-8',
                        help='Specify target file encoding. See full list of supported encodings in Python\'s Codec module.'
    )

    # params for both
    parser.add_argument('path',
                        help='Path (or filename) to process. Only files with .txt|.TXT extension are considered.'
    )
    parser.add_argument('--log', default=os.path.splitext(parser.prog)[0] + '.log',
                        help='Log file.'
    )
    return parser.parse_args()


def print_args(arguments):
    print('\nRuntime:')
    print(json.dumps(vars(arguments), indent=2))
    print('\n')


def which_command(arguments):
    return 'C' if arguments.command in ['c', 'co', 'convert'] else 'D'


def display_encodings(txtencoder, filename):
    _detres = txtencoder.detectEncoding(filename)
    print('-- Detector:    ' + str(_detres))
    # also display alternative method via Unix <file> tool
    print('-- Unix <file>: ' + str(check_output(["file", "-b", filename], universal_newlines=True)))




if __name__ == '__main__':
    myargs = get_parsed_args()
    print_args(myargs)

    t_flist = FileIO().getFileList(myargs.path, ext='.txt', ignore_ext_case=True)
    t_flist.sort()
    print('Found {} files.'.format(len(t_flist)))

    txtenc = TxtEncoding()

    wf = open(myargs.log, mode='w')

    fc = 0
    for fname in t_flist:
        fc += 1
        if which_command(myargs) is 'D':
            ### Display mode ###
            print('\n[{}/{}] Encoding for "{}":'.format(fc, len(t_flist), fname))
            display_encodings(txtenc, fname)
        else:
            ### Convert mode ###
            print('\n[{}/{}] Converting "{}" to {}...'.format(fc, len(t_flist), fname, myargs.toenc))
            if myargs.fromenc:
                fromenc = myargs.fromenc
            else:
                ## encoding detection
                detres = txtenc.detectEncoding(fname)
                # files where encoding detection is not confident enough, will be skipped and logged
                if detres['confidence'] < myargs.confidence:
                    warntext = '[WARN] "{}": Skipping conversion; confidence too low = {}\n'.format(fname, detres['confidence'])
                    wf.write(warntext)
                    continue
                fromenc = detres['encoding']

            # read in the file (in memory)
            with open(fname, mode='r', encoding=fromenc) as f:
                ftext = f.read()

            with open(fname, mode='w', encoding=myargs.toenc) as f:
                f.write(ftext)

            # re-display the encoding detector's results on the converted file
            display_encodings(txtenc, fname)

    wf.close()

    if os.stat(myargs.log).st_size > 0:
        print('\n\n[!] The conversion hasn\'t been entirely successful. See <{}> for details.'.format(myargs.log))
