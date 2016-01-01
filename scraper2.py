import requests
from bs4 import BeautifulSoup
import sys, os, csv

def fetch_search_results(query=None, minAsk=None, maxAsk=None, bedrooms=None):
    search_params = {key: val for key, val in locals().items() if val is not None}
    if not search_params:
        raise ValueError("No valid keywords")
    base = 'http://www.trulia.com/for_rent/Lakeland,FL/APARTMENT_COMMUNITY_type'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()
    return resp.content, resp.encoding


def read_search_results():
    return print("break")


def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, "lxml", from_encoding=encoding)
    return parsed


def extract_listings(parsed):
    # location_attrs = {'data-latitude': True, 'data-longitude': True}
    listings = parsed.find_all(class_='media mvn') # , attrs=location_attrs)
    return listings

def write_listings(listings):
    return print("placeholder")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results(minAsk=500, maxAsk=1000, bedrooms=2)
    doc = parse_source(html, encoding)
    listings = extract_listings(doc)
    #print(listings)
    with open(os.path.join(os.path.dirname(__file__) + 'listings.csv'), "w", newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow("Price, Place, Address, Bedrooms, Bathrooms, Pet Friendly, Location")


    #print(doc.prettify(encoding=encoding))