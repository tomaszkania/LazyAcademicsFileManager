import os
from utils.ext_manager import Extensions
from utils.dupl_remove import Duplicates
from utils.pdf_detector import PhrasePDFDetector
from pathlib import Path


def main(PATH):
    ext1 = Extensions(PATH)
    ext1.group_by_extension()
    print(ext1.get_extension(PATH))
    files = ext1.get_files(PATH)
    print(files)
    print(f"{len(files)=}")


def purge(PATH):
    ext2 = Duplicates(PATH)
    ext2.remove_duplicated_files()


def move_pdf(PATH):
    ext3 = PhrasePDFDetector(PATH)
    ext3.look_up_pdf(["Lancaster"])


if __name__ == '__main__':
    PATH = os.path.join(Path.home(), "Downloads")
    PATH_DUPLICATES = PATH + "/Documents"
    purge(PATH_DUPLICATES)
    main(PATH)
    move_pdf(PATH_DUPLICATES)
