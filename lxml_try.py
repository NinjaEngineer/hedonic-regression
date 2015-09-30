__author__ = 'kkindle'

import requests
import csv
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

url = 'http://www.footballoutsiders.com/stats/teameff'

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)

print soup