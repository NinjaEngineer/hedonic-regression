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

#Use this later
def find_stripped(soup): #, what):
    #found = soup.find(what)
    found = soup
    if found is not None:
        return found.text.strip()
    else:
        return " "

# I am aware this function does too much stuff
def write_listing(apt):
    specialAttr = find_stripped(apt.find("small", class_="typeCaps typeEmphasize mrm h7"))
    place = apt.find("div", class_="man typeTruncate").text.strip()
    address = apt.find(itemprop="streetAddress").text.strip() + apt.find(itemprop="addressLocality").text.strip() + \
        " " + apt.find(itemprop="postalCode").text.strip()
    #link = apt.find("a", "primaryLink pdpLink activeLink").text.strip()
    location = apt.find(itemprop="addressLocality").text.strip()

    aptTypes = apt.find_all("div", class_="col cols17")
    for aptType in aptTypes:
        bedrooms = aptType.find("div", class_="txtL col cols7").text.strip()
        bathrooms = aptType.find("div", class_="txtC col cols4").text.strip()
        sqft = aptType.find("div", class_="txtC col cols6").text.strip()
        price = aptType.find_all("div", class_="txtC col cols6")[1].text.strip()
        writer.writerow(price + ", " + sqft + ", " + place + ", " + address.replace(",", " ") + ", " +
                        bedrooms + ", " + bathrooms + ", " + specialAttr + ", " + location) # + ", " + link)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results(minAsk=500, maxAsk=1000, bedrooms=2)
    doc = parse_source(html, encoding)
    listings = extract_listings(doc)
    with open(os.path.join(os.path.dirname(__file__) + 'listings.csv'), "w", newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow("Price, Sqft, Place, Address, Bedrooms, Bathrooms, SpecialAttribute, Location, Link")
        #print(listings.find("small", class_="typeCaps typeEmphasize mrm h7"))
        i = 0
        while i < len(listings):
           write_listing(listings[i])
           i += 1


    #print(doc.prettify(encoding=encoding))