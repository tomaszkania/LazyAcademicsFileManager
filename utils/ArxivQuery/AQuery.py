import requests
import re


query_dates = "https://arxiv.org/search/advanced?advanced=terms-0-operator=AND&terms-0-term=AUTHORCONTAINSPLACEHOLDER&terms-0-field"\
        "=author&terms-1-operator=AND&terms-1-term=TITLECONTAINS1PLACEHOLDER&terms-1-field=title&terms-2-operator=AND&terms-2"\
        "-term=ANYWHERECONTA1PLACEHOLDER&terms-2-field=all&terms-3-operator=AND&terms-3-term" \
        "=ANYWHERECONTA2PLACEHOLDER&terms-3-field=all&terms-4-operator=AND&terms-4-term=MSCCLACONTAINSPLACEHOLDER&terms-4-field" \
        "=msc_class&terms-5-operator=AND&terms-5-term=TITLECONTAINS2PLACEHOLDER&terms-5-field=title&classification" \
        "-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date" \
        "-from_date=DATEFROM&date-to_date=DATETO&date-date_type=submitted_date&abstracts=show&size=200&order" \
        "=-announced_date_first"

query = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term" \
              "=AUTHORCONTAINSPLACEHOLDER&terms-0-field=author&terms-1-operator=AND&terms-1-term" \
              "=TITLECONTAINS1PLACEHOLDER&terms-1-field=title&terms-2-operator=AND&terms-2-term" \
              "=ANYWHERECONTA1PLACEHOLDER&terms-2-field=all&terms-3-operator=AND&terms-3-term" \
              "=ANYWHERECONTA2PLACEHOLDER&terms-3-field=all&terms-4-operator=AND&terms-4-term" \
              "=MSCCLACONTAINSPLACEHOLDER&terms-4-field=msc_class&terms-5-operator=AND&terms-5-term" \
              "=TITLECONTAINS2PLACEHOLDER&terms-5-field=title&classification-physics_archives=all&classification" \
              "-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date" \
              "-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first"

LIMITSEARCH = 600


def get_html_document(url):
    response = requests.get(url)
    return response.text


def cut_arxiv_link(string):
    cut_string = string[22:]
    cut_string = re.sub('^\d+(\.\d+)*$', '', cut_string)  # accept numbers separated by dots
    return cut_string + ".pdf"
