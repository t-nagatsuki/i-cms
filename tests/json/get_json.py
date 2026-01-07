#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib
import json
import requests
from bs4 import BeautifulSoup

base_url = "http://starcitizendb.com"
target_url = base_url + "/api/components/QuantumDrive"
lst_json = []


r = requests.get(target_url)
soup = BeautifulSoup(r.text, "lxml")

for a in soup.find_all("a"):
	read_obj = urllib.urlopen(base_url + a.get("href"))
	lst_json.append(json.loads(read_obj.read()))

print(lst_json)
