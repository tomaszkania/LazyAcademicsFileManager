import os
import shutil
import re
import PyPDF3
from typing import List



class ArxivIdentify(Extensions):
    """
    A class to identify and organize arXiv preprints in a given directory.
    Inherits from the `Extensions` class.
    """

    def __init__(self, path: str):
        """
        Initialize an ArxivIdentify instance.

        Args:
            path (str): The directory path containing the PDF files.
        """
        super().__init__(path)

    def get_arxiv_identifier(self) -> None:
        """
        Identify arXiv preprints in the directory, and move them to their respective
        category subdirectories.
        """
        files = self._get_files_in_directory()
        for file in files:
            if file.endswith('.pdf'):
                print(file)
                possible_preprint = PyPDF3.PdfFileReader(os.path.join(self.path, file))
                frontpage = possible_preprint.getPage(0).extractText()

                if re.search(r'arXiv:', frontpage):
                    category = self._extract_category(frontpage)
                    destpath = os.path.join(self.path, category)
                    os.makedirs(destpath, exist_ok=True)
                    nfile = os.path.join(destpath, file)
                    shutil.move(os.path.join(self.path, file), nfile)
                else:
                    print("Likely not an arXiv preprint.")

    def _get_files_in_directory(self) -> List[str]:
        """
        Retrieve the list of file names in the directory.

        Returns:
            List[str]: A list of file names in the directory.
        """
        return [entry.name for entry in os.scandir(self.path) if entry.is_file()]

    @staticmethod
    def _extract_category(frontpage: str) -> str:
        """
        Extract the arXiv category from the front page of the PDF.

        Args:
            frontpage (str): The text extracted from the front page of the PDF.

        Returns:
            str: The arXiv category.
        """
        position = frontpage.index('arXiv:')
        category_placeholder = frontpage[position + 18:position + 35]
        category_leftendpoint = category_placeholder.find("[")
        category_rightendpoint = category_placeholder.find("]")
        return category_placeholder[category_leftendpoint + 1:category_rightendpoint]


if __name__ == "__main__":
    # Example usage
    path = r"C:\Users\Tomek\Downloads\pdfs"
    arxiv_identifier = ArxivIdentify(path)
    arxiv_identifier.get_arxiv_identifier()
