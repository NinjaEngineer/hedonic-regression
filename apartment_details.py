import requests, sys, time, sqlite3
from random import randint
from bs4 import BeautifulSoup

conn = sqlite3.connect("apartment_data.db")
c = conn.cursor()


def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, "lxml", from_encoding=encoding)
    return parsed

def extract_listings(parsed):
    # location_attrs = {'data-latitude': True, 'data-longitude': True}
    listings = parsed.find_all(class_='photoMapContainer man pan')
    return listings

def fetch_search_results(query=None, minAsk=None, maxAsk=None, bedrooms=None, location=None):
    search_params = {key: val for key, val in locals().items() if val is not None}
    if not search_params:
        raise ValueError("No valid keywords")
    base = 'http://www.trulia.com/' + location
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()
    time.sleep(randint(0, 4))
    return resp.content, resp.encoding


def read_search_results():
    return print("break"), print("possibly do this later")


def apt_details_links():
    return list(c.execute("SELECT DISTINCT link FROM aptSummary"))


def write_db(storage, fitness_center, elevator, spa, tennis_court, club_house, garbage_disposal, pool, dishwasher, \
             washing_mach, dryer, microwave, ac, sauna):
    Insert = [storage, fitness_center, elevator, spa, tennis_court, club_house, garbage_disposal, pool, dishwasher, \
              washing_mach, dryer, microwave, ac, sauna]
    c.execute("INSERT INTO aptSummary (storage, fitness_center, elevator, spa, tennis_court, club_house, "
                "garbage_disposal, pool, dishwasher, washing_mach, dryer, microwave, ac, sauna) VALUES "
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", Insert)

def write_details(details):
    d = details.find("div", class_="mvl")
    storage, fitness_center, elevator, spa, tennis_court, club_house, garbage_disposal, pool, dishwasher, washing_mach,\
    dryer, microwave, ac, sauna = False, False, False, False, False, False, False, False, False, False, False, \
                                  False, False, False
    if "Storage" in d:
        storage = True
    if "Fitness Center" in d:
        fitness_center = True
    if 'Elevator' in d:
        elevator = True
    if 'Spa' in d:
        spa = True
    if 'Tennis Court' in d:
        tennis_court = True
    if 'Club House' in d:
        club_house = True
    if 'Garbage Disposal' in d:
        garbage_disposal = True
    if 'Pool' in d:
        pool = True
    if 'Dishwasher' in d:
        dishwasher = True
    if 'Washing Machine' in d:
        washing_mach = True
    if 'Dryer' in d:
        dryer = True
    if 'Microwave' in d:
        microwave = True
    if 'Air Conditioning' in d:
        ac = True
    if 'Sauna' in d:
        sauna = True
    write_db()

if __name__ == '__main__':
    # apt_details_pages = apt_details_links()
    # for page in apt_details_pages:
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results(minAsk=500, maxAsk=1000, bedrooms=2, location="/rental-community/9000026190/Yacht-Club-at-Brickell-Apartments-1111-Brickell-Bay-Dr-Miami-FL-33131/")
        doc = parse_source(html, encoding)
        details = extract_listings(doc)
        write_details(details[0])
        # i = 0
            # while i < len(listings):
            #     write_listing(listings[i])
            #     print("Scraping " + metro + "\n extracting, translating, and exporting to a comma separated"
            #                                 " file and inserting into a sqlite table")
            #    i += 1
    conn.close()
