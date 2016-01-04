import requests, sys, os, csv, time, sqlite3
from random import randint
from bs4 import BeautifulSoup

apt_location_pages = []
conn = sqlite3.connect("apartment_data.db")
c = conn.cursor()

def create_apt_list(locations):
    for location in locations:
        loc_link = 'http://www.trulia.com/for_rent/' + location + '/APARTMENT_COMMUNITY_type'
        html, encoding = fetch_search_results(minAsk=500, maxAsk=1000, bedrooms=2, location=loc_link)
        doc = parse_source(html, encoding)
        #if doc.find(class_='col cols16 mts txtC srpPagination_list').text.strip() != "1":
        try:
            print("Checking for multiple pages of listings in " + location)
            pages = int(doc.find(class_='col cols16 mts txtC srpPagination_list').text.strip()[-1])
            page = 1
            while page <= pages:
                apt_location_pages.append('http://www.trulia.com/for_rent/' + location +
                                          '/APARTMENT_COMMUNITY_type/' + str(page) + '_p')
                page += 1
        except AttributeError:
            print("Problem Here: " + location)


def fetch_search_results(query=None, minAsk=None, maxAsk=None, bedrooms=None, location=None):
    search_params = {key: val for key, val in locals().items() if val is not None}
    if not search_params:
        raise ValueError("No valid keywords")
    base = location
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()
    time.sleep(randint(0, 4))
    return resp.content, resp.encoding


def read_search_results():
    return print("break"), print("possibly do this later")


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
    place = find_stripped(apt.find("div", class_="man typeTruncate"))
    address = find_stripped(apt.find(itemprop="streetAddress")) + find_stripped(apt.find(itemprop="addressLocality")) +\
        " " + find_stripped(apt.find(itemprop="postalCode"))
    xAddress = find_stripped(apt.find(itemprop="streetAddress")).replace(",","")
    xlocale = find_stripped(apt.find(itemprop="addressLocality"))
    xZip = find_stripped(apt.find(itemprop="postalCode"))
    #link = apt.find("a", "primaryLink pdpLink activeLink").text.strip()
    location = find_stripped(apt.find(itemprop="addressLocality"))
    aptTypes = apt.find_all("div", class_="col cols17")
    for aptType in aptTypes:
        bedrooms = find_stripped(aptType.find("div", class_="txtL col cols7"))
        if bedrooms == "Studio":
            xbedrooms = "0"
        else:
            xbedrooms = bedrooms[0]
        bathrooms = find_stripped(aptType.find("div", class_="txtC col cols4"))
        xbathrooms = bathrooms[0]
        sqft = find_stripped(aptType.find("div", class_="txtC col cols6"))
        xsqft = sqft.replace("+", "")[:-4]
        price = aptType.find_all("div", class_="txtC col cols6")[1].text.strip()
        xprice = price.replace("+", "")[1:-3]
        writer.writerow(price + "," + sqft + "," + place + "," + address.replace(",", " ") + "," +
                        bedrooms + "," + bathrooms + "," + specialAttr + "," + location) # + ", " + link)
        xInsert = [xprice, xsqft, place, xAddress, xZip, xlocale, xbedrooms, xbathrooms, specialAttr, location]
        c.execute("INSERT INTO aptSummary (price, sqft, place, address, zip, locale, bedrooms, bathrooms, specAttr, "
                  "location) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", xInsert)
        # c.execute("INSERT INTO aptSummary (price, sqft, place, address, zip, locale, bedrooms, bathrooms, specAttr, "
        #           "location) VALUES (" + xprice + ", " + xsqft + ", " + place + ", " + xAddress + ", " + xZip +
        #           ", " + xlocale + ", " + xbedrooms + ", " + xbathrooms + ", " + specialAttr + ", " + location + ");")
        conn.commit()


if __name__ == '__main__':
    locations = ['Miami,FL', 'Fort_Lauderdale,FL', 'West_Palm_Beach,FL', 'Tampa,FL',
                 'Saint_Petersburg,FL', 'Clearwater,FL', 'Orlando,FL', 'Kissimmee,FL', 'Sanford,FL', 'Jacksonville,FL',
                 'North_Port,FL', 'Bradenton,FL', 'Sarasota,FL', 'Cape_Coral,FL', 'Fort_Myers,FL', 'Lakeland,FL',
                 'Winter_Haven,FL', 'Palm_Bay,FL', 'Melbourne,FL', 'Titusville,FL', 'Tallahassee,FL', 'Ocala,FL',
                 'Daytona_Beach,FL', 'Pensacola,FL', 'Gainesville,FL', 'Port_Saint_Lucie,FL']
    create_apt_list(locations)
    with open(os.path.join(os.path.dirname(__file__), 'listings.csv'), "w", newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow("Price,Sqft,Place,Address,Bedrooms,Bathrooms,SpecialAttribute,Location") # ,Link")
        for metro in apt_location_pages:
            if len(sys.argv) > 1 and sys.argv[1] == 'test':
                html, encoding = read_search_results()
            else:
                html, encoding = fetch_search_results(minAsk=500, maxAsk=1000, bedrooms=2, location=metro)
                doc = parse_source(html, encoding)
                listings = extract_listings(doc)
                i = 0
                while i < len(listings):
                    write_listing(listings[i])
                    print("Scraping " + metro + "\n extracting, translating, and exporting to a comma separated"
                                                " file and inserting into a sqlite table")
                    i += 1
    conn.close()