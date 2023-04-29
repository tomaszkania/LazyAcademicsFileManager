import os
import requests
import feedparser
import re
from typing import Dict, List

class ArxivScraper:
    """
    A class designed to search, list, and download arXiv preprints based on specified search parameters.

    The `ArxivScraper` class provides functionality to search for arXiv preprints by author, title,
    year range, and other specified criteria. It allows users to list the preprints matching the search
    parameters and download their PDFs.

    Attributes:
        base_url (str): The base URL for the arXiv API.
        search_url (str): The URL for the arXiv API search endpoint.
        rows (int): The maximum number of results to be returned per API request.

    Methods:
        build_query(author_contains: str = "", title_contains: str = "", year_from: int = None, year_to: int = None) -> str:
            Builds an arXiv API search query using the specified parameters.
        get_paper_list(query: str) -> List[Dict[str, str]]:
            Fetches a list of arXiv preprints matching the specified query.
        download_pdf(paper_id: str, save_dir: str) -> None:
            Downloads the PDF for a specified arXiv preprint and saves it to the provided directory.
        download_pdfs(paper_list: List[Dict[str, str]], save_dir: str) -> None:
            Downloads the PDFs for a list of arXiv preprints and saves them to the provided directory.

    Usage:
        To use this class, instantiate an `ArxivScraper` object. Then, use the `build_query` method to create
        a search query based on your desired parameters. Call the `get_paper_list` method with your query
        to fetch a list of arXiv preprints that match your criteria. Finally, use the `download_pdfs` method
        to download the PDFs of the listed preprints and save them to a specified directory.

        Example:
            scraper = ArxivScraper()
            query = scraper.build_query(author_contains="Kania", title_contains="Banach", year_from=2010, year_to=2021)
            paper_list = scraper.get_paper_list(query)
            save_dir = "path/to/your/directory"
            scraper.download_pdfs(paper_list, save_dir).
    """

    
    def __init__(self, max_results: int = 10):
        self.max_results = max_results
        self.base_url = "http://export.arxiv.org/api/query?"
        self.pdf_base_url = "https://arxiv.org/pdf/"

    @staticmethod
    def build_query(authorcontains: str = "", titlecontains: str = "", year_from: int = 0, year_to: int = 0) -> str:
        query_parts = []

        if authorcontains:
            query_parts.append(f"au:{authorcontains}")

        if titlecontains:
            query_parts.append(f"ti:{titlecontains}")

        if year_from and year_to:
            query_parts.append(f"submittedDate:[{year_from}0101 TO {year_to}1231]")
        elif year_from:
            query_parts.append(f"submittedDate:[{year_from}0101 TO *]")
        elif year_to:
            query_parts.append(f"submittedDate:[* TO {year_to}1231]")

        query = " AND ".join(query_parts)
        return query

    def _get_search_url(self, query: str) -> str:
        return f"{self.base_url}search_query={query}&start=0&max_results={self.max_results}"

    def get_paper_list(self, query: str) -> List[Dict[str, str]]:
        url = self._get_search_url(query)
        response = requests.get(url)
        response.raise_for_status()

        # Use feedparser to parse the XML response
        parsed_response = feedparser.parse(response.content)
        entries = parsed_response["entries"]

        paper_list = [
            {
                "id": entry["id"].split("/abs/")[-1],
                "title": entry["title"],
                "authors": ", ".join(author["name"] for author in entry["authors"]),
                "published": entry["published"],
            }
            for entry in entries
        ]
        return paper_list

    def download_pdfs(self, paper_list: List[Dict[str, str]], folder: str = "pdfs"):
        os.makedirs(folder, exist_ok=True)
        for paper in paper_list:
            pdf_url = f"{self.pdf_base_url}{paper['id']}.pdf"
            response = requests.get(pdf_url)
            response.raise_for_status()

            # Remove the version number (e.g., "v2") from the paper ID
            sanitized_id = re.sub(r'v\d+$', '', paper['id'])
            # Replace forward slash with underscore
            sanitized_id = sanitized_id.replace('/', '_')
            pdf_path = os.path.join(folder, f"{sanitized_id}.pdf")

            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(response.content)
        print(f"Downloaded {len(paper_list)} PDFs to the '{folder}' folder.")


# Example usage
scraper = ArxivScraper(max_results=5)

# Build query
query = scraper.build_query(authorcontains="Kania", titlecontains="Banach", year_from=2010, year_to=2022)

# Fetch paper list
paper_list = scraper.get_paper_list(query)

for paper in paper_list:
    print(f"{paper['title']} by {paper['authors']} - {paper['published']}")

# Download PDFs
scraper.download_pdfs(paper_list, "pdfs")
