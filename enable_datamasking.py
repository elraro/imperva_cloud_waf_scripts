import json
from urllib import request
from urllib import parse
from pprint import pprint
import argparse
import sys

# Enter your API and Site ID info here.
api_id = XXXXX
api_key = "XXXXXXXXXXXXXXXXXXXX"
account_id = XXXXXXX

# API Urls
base_url_v1 = "https://my.imperva.com/api/prov/v1"
base_url_v2 = "https://my.imperva.com/api/prov/v2"
list_sites_url_v1 = "/sites/list"
masking_settings_url_v2 = "/sites/{siteId}/settings/masking"

# Setting variables
site_list = []

params_site_list = {
	"account_id": account_id,
	"page_size": 100,
	"page_num": 0
}

masking_settings = {
	"hashing_enabled": "true",
	"hash_salt": "XXXXXXXXXX"
}

# Send site list request
try:
	params_site_list_data = parse.urlencode(params_site_list)
	params_site_list_data = params_site_list_data.encode("ascii")
	req = request.Request(base_url_v1 + list_sites_url_v1, params_site_list_data)
	req.add_header("x-API-Id", api_id)
	req.add_header("x-API-Key", api_key)
	with request.urlopen(req, timeout=10) as response:
		json_raw = json.loads(response.read().decode("utf8"))
		for site in json_raw["sites"]:
			site_list.append(site["site_id"])
	pprint(site_list)
except Exception as e:
	print('Error:', e)
	exit(0)

# Set datamasking settings for each site in site_list
try:
	for siteId in site_list:
		siteId = str(siteId)
		masking_url = f"/sites/{siteId}/settings/masking"
		req = request.Request(base_url_v2 + masking_url, masking_settings)
		req.add_header("x-API-Id", api_id)
		req.add_header("x-API-Key", api_key)
		req.add_header("Content-Type", "application/json")
		with request.urlopen(req, data=json.dumps(masking_settings).encode('utf-8'), timeout=10) as response:
			json_raw = json.loads(response.read().decode("utf8"))
			pprint(json_raw)
except Exception as e:
	print('Error:', e)
	exit(0)
