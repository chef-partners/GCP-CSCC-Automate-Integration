import json
import os

class Properties:
    def __init__(self):
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
