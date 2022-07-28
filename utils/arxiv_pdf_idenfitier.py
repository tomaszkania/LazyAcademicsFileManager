import os
import shutil
import re
import PyPDF2

from utils.ext_manager import Extensions


class ArxivIdentify(Extensions):
    def __init__(self, path):
        super().__init__(path)

    def get_arxiv_identifier(self):
        files = []
        for entry in os.scandir(self.path):
            if entry.is_file():
                files.append(entry.name)
            else:
                continue
        for f in files:
            if f.endswith('.pdf'):
                print(f)
                possible_preprint = PyPDF2.PdfFileReader(os.path.join(self.path, f))
                frontpage = possible_preprint.getPage(0)
                frontpage = frontpage.extractText()
                print(type(frontpage))
                # identifiers = re.findall(r"(?i)arXiv:[\d{4}\.\d*]", frontpage)
                if re.search(r'arXiv:', frontpage):
                    position = frontpage.index('arXiv:')
                    # identifier = frontpage[position + 6:position + 18].replace(" ", "")  # rename the filename after
                    # invoking the purge method
                    category_placeholder = frontpage[position + 18:position + 35]  # we are avoiding deliberately
                    # complicated regexs
                    category_leftendpoint = category_placeholder.find("[")
                    category_rightendpoint = category_placeholder.find("]")
                    category = category_placeholder[category_leftendpoint + 1:category_rightendpoint]
                    destpath = os.path.join(self.path, category)
                    os.makedirs(destpath, exist_ok=True)
                    nfile = os.path.join(destpath, f)
                    shutil.move(os.path.join(self.path, f), nfile)
                else:
                    # identifier = identifiers[0]
                    print("Likely not an arXiv preprint.")