import google.auth
import json
import logging
import os
import uuid
from google.cloud import securitycenter_v1beta1
from google.protobuf import empty_pb2, struct_pb2, timestamp_pb2
from datetime import datetime, timedelta
from dateutil import parser

class CsccService:
    logger = logging.getLogger(__name__)

    def __init__(self, properties, securitySource = None):
        self.properties = properties
        print(os.getcwd())
        self.client = securitycenter_v1beta1.SecurityCenterClient().from_service_account_json(self.properties.csccKey)
        self.orgParent = f"organizations/{self.properties.organization}"
        if (not securitySource):
            self.initializeAutomateSource()
        else:
            self.securitySource = securitySource
            self.logger.info(f"Using Provided Security Source {self.securitySource}")

    def initializeAutomateSource(self):
        if (not self.AutomateSourceExists()):
            self.logger.info('Creating New Chef Automate Source')
            source = {'name': 'chef_automate', 'display_name':'Chef Automate',
            'description': f"Chef Automate Instance https://{self.properties.automateUrl}/event-feed"}
            self.securitySource = self.client.create_source(self.orgParent, source).name

    def createSource(self, parent, source):
        response = self.client.create_source(parent, source)
        return response

    def createFinding(self, finding):
        findingId = finding.get('name')
        response = self.client.create_finding(self.securitySource, findingId, finding)
        return response

    def getAllSources(self):
        sources = []
        for page in self.client.list_sources(self.orgParent).pages:
            for element in page:
               sources.append(element)
        return sources

    def getAllFindings(self):
        findings = []
        for page in self.client.list_findings(self.securitySource).pages:
            for element in page:
               findings.append(element)
        return findings
    
    def AutomateSourceExists(self):
        self.logger.info('Checking for existing Chef Automate Source')
        for source in self.getAllSources():
            if ('Chef Automate' in source.display_name):
                self.logger.info(f"Chef Automate Source Found. Using existing source {source.name}")
                self.securitySource = source.name
                return True 
        return False

    def buildFindings(self, failedControls):
        findings = []
        for control in failedControls:
            publicIp = 
            finding = {'name': str(uuid.uuid4()).replace('-', ''),
            'parent': self.securitySource,
            'resource_name': f"{self.orgParent}/projects/{control.get('node_name')}",
            'state':'ACTIVE',
            'category': control.get('control_title'),
            'external_uri': f"https://{self.properties.automateUrl}/compliance/reporting/nodes/{control.get('node_id')}",
            'source_properties': self.buildSourceProperties(control),
            'security_marks': {},
            'event_time': self.timestamp(datetime.now()),
            'create_time': self.timestamp(parser.parse(control.get('end_time')))}
            findings.append(finding)
        return findings

    def buildSourceProperties(self, control):
        sourceProperties = {'control_id': struct_pb2.Value(string_value=control.get('control_id')),
         'code_description': struct_pb2.Value(string_value=control.get('description')),
         'code_message': struct_pb2.Value(string_value=control.get('message')),
         'profile': struct_pb2.Value(string_value=control.get('profile')),
         'summary': struct_pb2.Value(string_value=control.get('profile_summary')),
         'status': struct_pb2.Value(string_value=control.get('status'))}
        return sourceProperties
   
    def timestamp(self, datetime):
        return timestamp_pb2.Timestamp(seconds=self.__unixTimeMillis(datetime))

    def __unixTimeMillis(self, dt):
        return int((dt.replace(tzinfo=None) - datetime.utcfromtimestamp(0)).total_seconds())
