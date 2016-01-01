from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from bs4 import BeautifulSoup
import requests
import pyexcel

url = 'http://www.zillow.com/homes/for_rent/FL/apartment_duplex_type/14_rid/featured_sort/32.630123,-73.487549,22.624152,-92.559814_rect/5_zm/2_p/'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "lxml")
list1 = soup.findAll('span', {'itemprop' : 'streetAddress'})
list2 = soup.findAll('span', {'itemprop' : 'postalCode'})
list10 = []
for item in list1:
    text = item.text
    list10.append(text)
list11 = []
for item in list2:
    text = item.text
    list11.append(text)
zillow_data = ZillowWrapper('X1-ZWz1a2ngha04jv_8s1xw')

list6 = []
list7 = []
list9 = []
for i in range (0,len(list10)):
    deep_search_response = zillow_data.get_deep_search_results(list10[i], list11[i])
    result = GetDeepSearchResults(deep_search_response)
    #print(result.get_attr('home_detail_link'))

    url2 = result.get_attr('home_detail_link')
    response = requests.get(url2)
    html = response.content

    soup2 = BeautifulSoup(html)
    list4 = soup2.findAll('ul', { 'class' : 'zsg-list_square zsg-lg-1-3 zsg-md-1-2 zsg-sm-1-1'})
    list8 = soup2.findAll('div', {'class':'zsg-lg-2-3 zsg-sm-1-1 hdp-header-description'})
    list5 = soup2.findAll('div', {'class':  'main-row  home-summary-row'})
    for item in list4:
        text = item.text
        list6.append(text)
    for item in list5:
        text = item.text
        list7.append(text)
    for item in list8:
        text = item.text
        list9.append(text)
list3 = []
for i in range(0,len(list9)):
    list3.append([list9[i], list6[i], list7[i]])

print(list4[0])
print(list8[0])
print(list5[0])

s1 = pyexcel.Sheet(list3)
s1.save_as('info1.csv')