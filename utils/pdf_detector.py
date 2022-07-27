import os
import shutil
import time
import PyPDF2
import re
from datetime import datetime
from utils.ext_manager import Extensions


class PhrasePDFDetector(Extensions):

    def __init__(self, path):
        super().__init__(path)

    '''
    Searching specified phrases in PDF files.
    '''
    @staticmethod
    def get_year(filepath):
        year = time.ctime(os.path.getmtime(filepath))
        year = datetime.strptime(year, "%a %b %d %H:%M:%S %Y")
        year = year.year
        return year

    @staticmethod
    def is_string_in_pdf(string, filepath):
        object = PyPDF2.PdfFileReader(filepath)
        number_of_pages = object.getNumPages()
        for i in range(number_of_pages):
            page = object.getPage(i)
            text = page.extractText()
            if re.search(string, text):
                return True
            else:
                pass

    def look_up_pdf(self, keywords):
        files = self.files
        for key in keywords:
            for f in files:
                if f.endswith('.pdf'):
                    if self.is_string_in_pdf(
                        key,
                        os.path.join(self.path, f)
                    ):
                        year = self.get_year(os.path.join(self.path, f))
                        destpath = os.path.join(self.path, key, str(year))
                        os.makedirs(destpath, exist_ok=True)
                        nfile = os.path.join(destpath, f)
                        shutil.move(os.path.join(self.path, f), nfile)
                    else:
                        print("Phrase not found in either pdf file.")
                else:
                    print("No pdf files found")
