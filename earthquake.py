import requests
import json
import xmltodict
 
URL = "https://www.seismicportal.eu/fdsnws/event/1/query?start=2023-2-20&end=2023-2-22&minlat=42.240172&maxlat=29.588440&minlon=28.533673&maxlon=49.348036"

r = requests.get(URL)
data = r.content
data_dict = xmltodict.parse(data)
json_data = json.dumps(data_dict)
g = json.loads(json_data)
json_data = json.dumps(g, indent=4)

with open("data.json", "w") as json_file:
	json_file.write(json_data)
