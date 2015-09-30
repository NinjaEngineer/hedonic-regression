__author__ = 'KKindle'

import csv
import requests
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

url = 'http://www.footballoutsiders.com/stats/teameff'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)

table = soup.find('table', attrs = {'class' : 'stats'})

list_of_rows = []
for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll('td'):
        text = cell.text
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)

outfile = open("./stats.csv", "w")
writer = csv.writer(outfile)
writer.writerows(list_of_rows)