__author__ = 'jstannard'

from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

address = '2238 Washington St. NE #2238C'
zipcode = '32905'

zillow_data = ZillowWrapper('X1-ZWz1a2ngha04jv_8s1xw')

deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
result = GetDeepSearchResults(deep_search_response)


print(result.get_attr('home_size'))
print(result.get_attr('bedrooms'))
print(result.get_attr('home_type'))
print(result.get_attr('zestimate_amount'))
