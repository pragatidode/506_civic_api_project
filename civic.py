from urllib import response

import requests
import urllib.parse

def Election_info(address):
	api_key = 'AIzaSyDPfesEkFhBBwUA_MFHdgON1plhsecUP30'
	search_api_url ='https://www.googleapis.com/civicinfo/v2/elections?key=' + api_key
	response = requests.get(url=search_api_url)
	data = response.json()
	# in the data make sure you select the information
	# relative the address only, not all of them
	#for election in data['elections']:
		#print(election)
	return data


def validateAddress(address):
	api_key = 'AIzaSyDEksQzo5Tx4zRvPYf_xerwKoaXRcOR7hw'
	encodedaddress=urllib.parse.quote_plus(address)
	geocodeapi = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ encodedaddress + '&key=' + api_key
	response = requests.get(url=geocodeapi)
	data = response.json()
	return data