# LazyAcademicsFileManager
This repository contains a collection of Python classes to help you organise and manage your PDF files, particularly those from the arXiv preprint server.

## Classes

### 1. ArxivScraper

`ArxivScraper` is a class that allows you to download arXiv preprints based on specified search criteria. You can search for papers by author, title keywords, or date range, and the class will download the corresponding PDF files to a specified folder.

### 2. ArxivIdentify

`ArxivIdentify` is a class that analyses PDF files in a given folder and identifies whether they are arXiv preprints. If a PDF is identified as an arXiv preprint, it will be moved to a subfolder named after its corresponding arXiv category.

### 3. Extensions

`Extensions` is a utility class that provides a set of methods to manage and organise files based on their extensions. It can group files in a folder into subfolders according to their file types, such as documents, pictures, executables, and archives.

### 4. Duplicates

`Duplicates` is a class that detects and removes duplicated files in a given folder. It compares files based on their content, and if two or more files are identical, it removes the duplicates, keeping only one instance of the file.

### 5. PhrasePDFDetector

`PhrasePDFDetector` is a class that searches for specified phrases in PDF files within a folder. If a PDF file contains any of the given phrases, the file will be moved to a subfolder named after the phrase and the file's modification year.


## Usage

1. Import the desired class from the corresponding file.
2. Create an instance of the class, passing the path to the folder containing your PDF files.
3. Call the appropriate methods to organise your PDF files based on your requirements.

For example:

```python
from arxiv_scraper import ArxivScraper
from arxiv_identify import ArxivIdentify
from duplicates import Duplicates
from phrase_pdf_detector import PhrasePDFDetector

# Download arXiv preprints
scraper = ArxivScraper()
scraper.download_papers(authorcontains="John Smith", titlecontains="Quantum")

# Identify arXiv preprints and organise them by category
identifier = ArxivIdentify("path/to/your/folder")
identifier.get_arxiv_identifier()

# Remove duplicated files
duplicates = Duplicates("path/to/your/folder")
duplicates.remove_duplicated_files()

# Search for phrases in PDF files and organise them accordingly
detector = PhrasePDFDetector("path/to/your/folder")
detector.look_up_pdf(["phrase1", "phrase2"])```


