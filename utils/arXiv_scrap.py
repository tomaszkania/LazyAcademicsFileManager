from bs4 import BeautifulSoup
import re
import os
import requests
from datetime import datetime
from ArxivQuery.AQuery import query, query_dates, LIMITSEARCH, cut_arxiv_link, get_html_document

# SPECIFY YOUR SEARCH

AUTHORCONTAINS: str = ""    # Add author's name - it is not mandatory; can be left as empty string
TITLECONTAINS1: str = "Banach"         # Some phrase from the title
TITLECONTAINS2: str = ""         # Some phrase from the title, 2
MSCCLACONTAINS: str = ""         # MSC classification tag
ANYWHERECONTA1: str = ""         # Anything, anywhere: could be the are tag, e.g. [math.GN]
ANYWHERECONTA2: str = ""         # As above.

# SPECIFY DATE RANGE (IF NOT RELEVANT LEAVE EMPTY STRINGS): DATE FORMAT YYYY-MM-DD

DATEFROM: str = "2010-10-10"
DATETO: str = "2011-10-10"

# Folder preparation
# The files will be fetched to ./utils/ArXiv_dump_"timestamp"

dumpfolder = datetime.now().strftime('ArXiv_dump_%Y%m%d%H%M')
os.makedirs(dumpfolder, exist_ok=True)

# Search placeholders
placeholders = ["AUTHORCONTAINSPLACEHOLDER", "TITLECONTAINS1PLACEHOLDER", "TITLECONTAINS2PLACEHOLDER", "MSCCLACONTAINSPLACEHOLDER", "ANYWHERECONTA1PLACEHOLDER",
            'ANYWHERECONTA2PLACEHOLDER']
keywords = [AUTHORCONTAINS, TITLECONTAINS1, TITLECONTAINS2, MSCCLACONTAINS, ANYWHERECONTA1, ANYWHERECONTA2]
result_pages_no = int(LIMITSEARCH / 200)

# Checking whether time range is set
if len(DATEFROM) > 3 and len(DATETO) > 3:
    query = query_dates
    placeholders = placeholders + ["DATEFROM", "DATETO"]
    keywords = keywords + [DATEFROM, DATETO]

working_dictionary = zip(placeholders, keywords)
queries = []
q = query

for placeholder, key in working_dictionary:
    q = q.replace(placeholder, key)
queries.append(q)

for index, query in enumerate(queries):
    query = query + "&start=" + str(index * 200)
    print(query)

for url_to_scrape in queries:
    # create document
    html_document = get_html_document(url_to_scrape)

    # create soap object
    soup = BeautifulSoup(html_document, 'html.parser')
    links = soup.find_all('a', attrs={'href': re.compile("^https://arxiv.org/pdf/")})
    number_of_links = len(links)
    print(f"Found: {number_of_links} preprints.")

    for link in links:
        url = link.get('href')
        print(url)
        name = cut_arxiv_link(url)
        print(name)
        local_file = os.path.join(dumpfolder, name)
        data = requests.get(url)
        with open(local_file, 'wb') as file:
            file.write(data.content)

##############
