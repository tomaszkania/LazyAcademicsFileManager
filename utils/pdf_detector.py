import os
import shutil
import time
import PyPDF3
import re
from datetime import datetime
from typing import List
from utils.ext_manager import Extensions


class PhrasePDFDetector(Extensions):
    """
    A class to find and move PDF files containing specified phrases.

    The `PhrasePDFDetector` class inherits from the `Extensions` class and provides functionality
    to search for specified phrases in PDF files within a given directory and move the files to
    new directories based on the phrase and the file's year.

    Methods:
        get_year(filepath: str) -> int:
            Gets the year of the last modification time of the file.
        is_string_in_pdf(string: str, filepath: str) -> bool:
            Checks if the given string is present in the specified PDF file.
        display_pdfs_with_phrases(keywords: List[str]) -> None:
            Displays the PDF files containing any of the specified phrases.
        move_pdfs_with_phrases(keywords: List[str]) -> None:
            Moves the PDF files containing any of the specified phrases to new directories.

    Usage:
        To use this class, instantiate a `PhrasePDFDetector` object with a path to the directory you want to
        search for PDF files containing specified phrases. Call the `display_pdfs_with_phrases` method to
        display the PDF files containing any of the specified phrases or use the `move_pdfs_with_phrases`
        method to move them to new directories based on the phrase and the file's year.

        Example:
            pdf_detector = PhrasePDFDetector("path/to/your/directory")
            phrases = ["phrase1", "phrase2"]
            pdf_detector.display_pdfs_with_phrases(phrases)
            pdf_detector.move_pdfs_with_phrases(phrases)
    """

    def __init__(self, path: str):
        super().__init__(path)

    @staticmethod
    def get_year(filepath: str) -> int:
        year = time.ctime(os.path.getmtime(filepath))
        year = datetime.strptime(year, "%a %b %d %H:%M:%S %Y")
        year = year.year
        return year

    @staticmethod
    def is_string_in_pdf(string: str, filepath: str) -> bool:
        pdf_object = PyPDF3.PdfFileReader(filepath)
        number_of_pages = pdf_object.getNumPages()
        for i in range(number_of_pages):
            page = pdf_object.getPage(i)
            text = page.extractText()
            if re.search(string, text):
                return True
        return False

    def display_pdfs_with_phrases(self, keywords: List[str]) -> None:
        files = self.files
        for key in keywords:
            for f in files:
                if f.endswith('.pdf'):
                    if self.is_string_in_pdf(key, os.path.join(self.path, f)):
                        print(f"Phrase '{key}' found in PDF file: {f}")
                else:
                    print("No PDF files found")

    def move_pdfs_with_phrases(self, keywords: List[str]) -> None:
        files = self.files
        for key in keywords:
            for f in files:
                if f.endswith('.pdf'):
                    if self.is_string_in_pdf(key, os.path.join(self.path, f)):
                        year = self.get_year(os.path.join(self.path, f))
                        destpath = os.path.join(self.path, key, str(year))
                        os.makedirs(destpath, exist_ok=True)
                        nfile = os.path.join(destpath, f)
                        shutil.move(os.path.join(self.path, f), nfile)
                    else:
                        print(f"Phrase '{key}' not found in PDF file: {f}")
                else:
                    print("No PDF files found")
