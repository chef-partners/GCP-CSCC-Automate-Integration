import requests
import json
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(category=InsecureRequestWarning)

class AutomateClient:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
    
    def post(self, resource, body):
        req = requests.post(f"https://{self.url}/api/v0/{resource}", data=json.dumps(body), headers=self.headers, verify=False)
        return req.json()      

    def get(self, resource):
        req = requests.get(f"https://{self.url}/api/v0/{resource}", headers=self.headers, verify=False)
        return req.json()
