#!/env/bin/py
import requests, logging
logger = logging.getLogger(__name__)

def http_exc(e):
	if isinstance(e, requests.Response):
		raise Exception(f"HTTP Error Message: {e.text}", f"HTTP Error: {e.status_code}")
	raise Exception(f"HTTP Error Message: {e.response.text}", f"HTTP Error: {e.response.status_code}")

def get_zones(api_url, api_key, headers: dict = None) -> requests.Response:
	h = { 'X-API-Key': api_key }
	if headers: 
		del headers['X-API-Key']
		h = h.update(headers)
	try:
		response = requests.get(
			url=f"{api_url}/api/v1/servers/localhost/zones", 
			headers=h
		)
	except requests.HTTPError as e:
		http_exc(e)
	if response.status_code >= 400:
		http_exc(response)
	return response