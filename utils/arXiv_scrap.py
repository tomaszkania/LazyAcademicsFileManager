from typing import List

from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
from ArxivQuery.AQuery import *

# SPECIFY YOUR SEARCH

AUTHORCONTAINS: str = "Wąsowicz"
TITLECONTAINS1: str = ""
TITLECONTAINS2: str = ""
MSCCLACONTAINS: str = ""
ANYWHERECONTA1: str = ""
ANYWHERECONTA2: str = ""

# SPECIFY DATE RANGE (IF NOT RELEVANT LEAVE EMPTY STRINGS): DATE FORMAT YYYY-MM-DD

DATEFROM = ""
DATETO = ""

##

dumpfolder = datetime.now().strftime('ArXiv_dump_%Y%m%d%H%M')
os.makedirs(dumpfolder, exist_ok=True)
placeholders = ["AUTHORCONTAINSPLACEHOLDER", "TITLECONTAINS1PLACEHOLDER", "TITLECONTAINS2PLACEHOLDER", "MSCCLACONTAINSPLACEHOLDER", "ANYWHERECONTA1PLACEHOLDER",
            'ANYWHERECONTA2PLACEHOLDER', 'DATEFROM', 'DATETO']
keywords = [AUTHORCONTAINS, TITLECONTAINS1, TITLECONTAINS2, MSCCLACONTAINS, ANYWHERECONTA1, ANYWHERECONTA2]
working_dictionary = zip(placeholders, keywords)
result_pages_no = int(LIMITSEARCH / 200)

if len(DATEFROM) > 3 and len(DATETO) > 3:
    query = query_dates
    placeholders = placeholders + ["DATEFROM", "DATETO"]
    keywords = keywords + [DATEFROM, DATETO]

queries: list[str] = []

q = query
print(q)
for placeholder, key in working_dictionary:
    q = q.replace(placeholder, key)
queries.append(q)

for index, query in enumerate(queries):
    query = query + "&start=" + str(index * 200)
    print(query)


for q in queries:
    print(q)
print(len(queries))
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
