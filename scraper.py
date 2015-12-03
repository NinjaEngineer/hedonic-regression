import requests
from bs4 import BeautifulSoup
import sys

def fetch_search_results(query=None, minAsk=None, MaxAsk=None, bedrooms=None):
    search_params = { key: val for key, val in locals().items() if val is not None}
    if not search_params:
        raise ValueError("No valid keywords")

    base = 'http://seattle.craigslist.org/search/apa'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()
    return resp.content, resp.encoding

def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed

if __name__ == '__main__':
