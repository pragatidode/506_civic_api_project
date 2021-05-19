from urllib import response

import requests


def Election_info(address):
	api_key = 'AIzaSyDPfesEkFhBBwUA_MFHdgON1plhsecUP30'




	search_api_url ='https://www.googleapis.com/civicinfo/v2/elections?key=AIzaSyDPfesEkFhBBwUA_MFHdgON1plhsecUP30'

	response = requests.get(url=search_api_url)
	data = response.json()


	# in the data make sure you select the information
	# relative the address only, not all of them
	#for election in data['elections']:
		#print(election)

	return ""

#print(Election_info(None))