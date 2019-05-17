import ast
import json
import logging
import os
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.urllib3.disable_warnings(category=InsecureRequestWarning)

class Properties:
    logger = logging.getLogger(__name__)

    def __init__(self, env = None):
      if (env == 'gcp'):
        self.__buildPropertiesFromGCPMetadata()
      else:
        self.__buildPropertiesFromFile()

    def __buildPropertiesFromFile(self):
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

    def __buildPropertiesFromGCPMetadata(self):
        path = f"{os.getcwd()}/"
        self.automateUrl = self.__getMetadataAttribute("automate-ip")
        self.scanProfiles = []
        metadata_profiles = self.__getMetadataAttribute("scan-profiles")
        if not metadata_profiles:
            self.scanProfiles = ast.literal_eval(metadata_profiles))
        self.automateApiToken = self.__getMetadataAttribute("automate-api-token")
        self.__outputCsccKey(self.__getMetadataAttribute("cscc-key"))
        self.csccKey = f"{path}/csccKey.json"
        self.serviceAccount = self.__getMetadataAttribute("service-account")
        self.organization = self.__getMetadataAttribute("organization-id")
        self.sourceId = self.__getMetadataAttribute("source-id")
        self.__log_properties()

    def __getMetadataAttribute(self, attributeName):
      headers = {"Metadata-Flavor": "Google", "content-type": "application/json"}
      req = requests.get(f"http://metadata/computeMetadata/v1/instance/attributes/{attributeName}", headers=headers)
      return req.text.rstrip()
    
    def __outputCsccKey(self, csccKey):
      with open('csccKey.json', 'w+') as f:
        f.write(csccKey)

    def __log_properties(self):
      self.logger.info(f"Automate Url: {self.automateUrl}")
      self.logger.info(f"Scan Profiles: {self.scanProfiles}")
      self.logger.info(f"Automate Api Token: {self.automateApiToken}")
      self.logger.info(f"Source ID: {self.sourceId}")


