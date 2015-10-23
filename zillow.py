__author__ = 'jstannard'

from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults, GetUpdatedPropertyDetails

address = '1760 Ardmore St NE'
zipcode = '32907'
# zillow_id = '43504943'


zillow_data = ZillowWrapper('X1-ZWz1a2ngha04jv_8s1xw')
deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
result = GetDeepSearchResults(deep_search_response)
#
# response = zillow_data.ge
# print(result.get_attr('home_info'))
# result = GetUpdatedPropertyDetails(response)

print(result.get_attr('home_size'))
print(result.get_attr('bedrooms'))
print(result.get_attr('home_type'))
print(result.get_attr('zestimate_amount'))
print(result.get_attr('zillow_id'))