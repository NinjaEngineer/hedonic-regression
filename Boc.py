__author__ = 'kkindle'

import requests
import csv
import pandas as pd
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

url = "http://www.footballoutsiders.com/stats/teameff"
r = requests.get(url)
soup = BeautifulSoup(r.text)

disasters = []
for row in soup.findAll('li'):
    disasters.append(row.text)
df = pd.DataFrame(disasters, columns =['raw'])

print disasters