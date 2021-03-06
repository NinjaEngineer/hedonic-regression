__author__ = 'kkindle'

import lxml.html
from lxml.cssselect import CSSSelector

# get some html
import requests

r = requests.get('http://www.footballoutsiders.com/stats/teameff')

# build the DOM Tree
tree = lxml.html.fromstring(r.text)

# print the parsed DOM Tree
print lxml.html.tostring(tree)

# construct a CSS Selector
sel = CSSSelector('div.foo li a')

# Apply the selector to the DOM tree.
results = sel(tree)
print results

# print the HTML for the first result.
match = results[1]
print lxml.html.tostring(match)

# get the href attribute of the first result
print match.get('href')

# print the text of the first result.
print match.text

# get the text out of all the results
data = [result.text for result in results]