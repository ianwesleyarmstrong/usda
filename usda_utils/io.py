from glob import glob
import logging
from os.path import join
from typing import List

logging.basicConfig(level=logging.DEBUG)


def gather_extensions(data_dir: str, extensions: str) -> List[str]:
    # support for compressor or uncompressed .fq files
    # https://stackoverflow.com/questions/4568580/python-glob-multiple-filetypes
    filenames = []
    if type(extensions) == str:
        extensions = (extensions,)
    for ext in extensions:
        data_dir_name = join(data_dir, ext)
        logging.debug(data_dir_name)
        filenames.extend(glob(data_dir_name))
    logging.debug(f'Found {len(filenames)} files with extension(s) {extensions}')
    return filenames
