# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
#

__author__ = 'HD'

import os
import sys
from pathlib import Path

import chardet


def _get_path_list(file_dir, file_exts):
    file_paths = []
    for ext in file_exts:
        file_paths.extend(Path(file_dir).glob(ext))
    return file_paths


def _get_encoding_type(file_path):
    raw_data = open(file_path, 'rb').read()
    result = chardet.detect(raw_data)
    return result['encoding']


def _convert_encoding(file_path, source_encoding, dest_encoding):
    file_stream = open(file_path, 'rb')
    raw_data = file_stream.read()
    file_stream.close()

    source_text = raw_data.decode(source_encoding)
    dest_bytes = source_text.encode(dest_encoding, 'ignore')

    file_stream = open(file_path, 'wb')
    file_stream.write(dest_bytes)
    file_stream.close()


def main(argv):
    if len(argv) < 4:
        usage = """Usage: %s file_dir source_encoding dest_encoding file_filters
Example: %s c:\\ gb2312 utf-8 *.cpp *.h"""
        script_name = os.path.basename(__file__)
        print(usage % (script_name, script_name))
        return

    file_dir = argv[0]
    source_encoding = argv[1]
    dest_encoding = argv[2]
    file_exts = argv[3:]

    converted_files = []
    file_paths = _get_path_list(file_dir, file_exts)
    for path in file_paths:
        encoding_type = _get_encoding_type(path)
        print(encoding_type, path)
        if encoding_type.lower() == source_encoding.lower():
            _convert_encoding(path, source_encoding, dest_encoding)
            converted_files.append(path)
    print('---------- converted file list begin ----------')
    for path in converted_files:
        print(path)
    print('---------- converted file list end ----------')
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
