import json
import os
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(category=InsecureRequestWarning)

class Properties:
    def __init__(self, env = None):
      if (env == 'gcp'):
        self.buildPropertiesFromGCPMetadata()
      else:
        self.buildPropertiesFromFile()

    def buildPropertiesFromFile(self):
      path = f"{os.getcwd()}/app"
      with open(os.path.join(path,'app.properties.json')) as p:
        propertiesFile = json.load(p)
        self.automateUrl = propertiesFile["properties"]["automatePublicIp"]
        self.scanProfiles = propertiesFile["properties"]["scanProfiles"]
        self.automateApiToken = propertiesFile["properties"]["automateApiToken"]
        self.csccKey = propertiesFile["properties"]["cscc"]
        self.serviceAccount = propertiesFile["properties"]["serviceAccount"]
        self.organization = propertiesFile["properties"]["organization"]
        self.sourceId = propertiesFile["properties"]["source"]

    def buildPropertiesFromGCPMetadata(self):
        path = f"{os.getcwd()}/app"
        self.automateUrl = self.getMetadataAttribute("automate-ip")
        self.scanProfiles = self.getMetadataAttribute("scan-profiles")
        self.automateApiToken = self.getMetadataAttribute("automate-api-token")
        self.outputCsccKey(self.getMetadataAttribute("cscc-key"))
        self.csccKey = f"{path}/csccKey.json"
        self.serviceAccount = self.getMetadataAttribute("service-account")
        self.organization = self.getMetadataAttribute("organization-id")
        self.sourceId = self.getMetadataAttribute("source-id")

    def getMetadataAttribute(self, attributeName):
      headers = {"Metadata-Flavor": "Google", "content-type": "application/json"}
      req = requests.get(f"http://metadata/computeMetadata/v1/instance/attributes/{attributeName}", headers=headers)
      return req.text

    def outputCsccKey(self, csccKey):
      with open('csccKey.json') as f:
        f.write(csccKey)

