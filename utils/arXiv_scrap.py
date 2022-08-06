from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
from ArxivQuery.AQuery import *

# SPECIFY YOUR SEARCH

AUTHORCONTAINS: str = "Wąsowicz" # Add author's name
TITLECONTAINS1: str = ""         # Some phrase from the title
TITLECONTAINS2: str = ""         # Some phrase from the title, 2
MSCCLACONTAINS: str = ""         # MSC classification tag
ANYWHERECONTA1: str = ""         # Anything, anywhere: could be the are tag, e.g. [math.GN]
ANYWHERECONTA2: str = ""         # As above.

# SPECIFY DATE RANGE (IF NOT RELEVANT LEAVE EMPTY STRINGS): DATE FORMAT YYYY-MM-DD

DATEFROM: str = ""
DATETO: str = ""

# The files will be fetched to ./utils/ArXiv_dump_"timestamp"

# Variables:

dumpfolder = datetime.now().strftime('ArXiv_dump_%Y%m%d%H%M')

# Folder preparation
os.makedirs(dumpfolder, exist_ok=True)

# Search placeholders
placeholders = ["AUTHORCONTAINSPLACEHOLDER", "TITLECONTAINS1PLACEHOLDER", "TITLECONTAINS2PLACEHOLDER", "MSCCLACONTAINSPLACEHOLDER", "ANYWHERECONTA1PLACEHOLDER",
            'ANYWHERECONTA2PLACEHOLDER']
keywords = [AUTHORCONTAINS, TITLECONTAINS1, TITLECONTAINS2, MSCCLACONTAINS, ANYWHERECONTA1, ANYWHERECONTA2]

working_dictionary = zip(placeholders, keywords)
result_pages_no = int(LIMITSEARCH / 200)

# Checking whether time range is set
if len(DATEFROM) > 3 and len(DATETO) > 3:
    query = query_dates
    placeholders = placeholders + ["DATEFROM", "DATETO"]
    keywords = keywords + [DATEFROM, DATETO]

queries: list[str] = []

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

    print(links)

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
