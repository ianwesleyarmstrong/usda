import glob
import logging
from os.path import join
from typing import List, Tuple, Union

logging.basicConfig(level=logging.DEBUG)


def gather_extensions(data_dir: str, extensions: Union[str, tuple(str)]) -> List[str]:
    # support for compressor or uncompressed .fq files
    # https://stackoverflow.com/questions/4568580/python-glob-multiple-filetypes
    filenames = []
    for ext in extensions:
        filenames.extend(glob(join(data_dir, ext)))
    logging.debug(f'Found {len(filenames)} files with extension(s) {extensions}')
    return filenames
