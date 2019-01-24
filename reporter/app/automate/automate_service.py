from apscheduler.schedulers.blocking import BlockingScheduler
from automate.automate_client import AutomateClient
from logging.config import dictConfig
import datetime
import json
import logging
import sys
import time

class AutomateService:
  logger = logging.getLogger(__name__)

  def __init__(self, properties):
    self.properties = properties
    self.apiClient = AutomateClient(properties.automateUrl, {"api-token": properties.automateApiToken, "content-type": "application/json"})
    self.lastSentReports = []

  def startScan(self):
    managerId = self.__getGcpNodeManager()  
    scanProfiles = self.properties.scanProfiles
    self.addScanProfiles(scanProfiles)
    startTime = self.__formatScanDateTime(datetime.datetime.utcnow() + datetime.timedelta(minutes = 1))
    body = {"type": "exec", "tags": [], "name": f"cscc-scan-{datetime.datetime.now()}", "profiles": scanProfiles,
    "node_selectors": [{"manager_id": managerId, "filters": []}], "recurrence": f"DTSTART={startTime};FREQ=HOURLY;INTERVAL=1"}
    self.logger.info(f"Starting Scan on Node Manager: {managerId} with Profiles: {scanProfiles}" )
    return self.apiClient.post("compliance/scanner/jobs", body)

  def createCloudManagementService(self, serviceAccount):
    self.logger.info("Creating new GCP Node Manager")
    body = {"name": f"CSCC-Integration-{datetime.datetime.now()}", "type": "gcp-api", "credential_data": [
    {"key": "GOOGLE_CREDENTIALS_JSON", "value": json.dumps(serviceAccount)}], "instance_credentials": []}
    return self.apiClient.post("nodemanagers", body)

  def findReports(self):
    reportIds = self.__filterReports()
    reportList = []
    for id in reportIds:
      report = self.apiClient.post(f"compliance/reporting/reports/id/{id}", None)
      reportList.append(report)
    if (len(reportList) > 0):
      self.logger.info(f" {len(reportList)} Reports Found")
      self.logger.info(f"Reports: {reportIds}")
    return reportList

  def addScanProfiles(self, profiles):
    for p in profiles:
      profile = p.split("admin/")[1].split("#")
      profileName = profile[0]
      profileVersion = profile[1]
      body = {"name":f"{profileName}","version":f"{profileVersion}"}
      self.apiClient.post("compliance/profiles?owner=admin", body)

  def getFailedControls(self, reports):
    failedControls = []
    for report in reports:
      for profile in report['profiles']:
        for control in profile['controls']:
          for result in control['results']:
             if (result['status'] == "failed"):
              failedControl = {'node_name': report['node_name'],
              'node_id' : report['node_id'],
              'end_time': report['end_time'],
              'profile': profile['name'],
              'profile_summary': profile['summary'],
              'control_id': control['id'], 
              'control_title': control['title'], 
              'description':result['code_desc'],
              'message': result['message'],
              'status': result['status']}
              failedControls.append(failedControl)
    return failedControls

  def getReports(self, reportIds):
    reports = []
    for id in reportIds:
      self.logger.info(f"fetching report for id: {id}")
      report = self.apiClient.get(f"compliance/reporting/reports/id/{id}")
      reports.append(report)
    return reports

  def __filterReports(self):
    reportList = []
    start_time = self.__formatDate(datetime.datetime.utcnow() - datetime.timedelta(minutes = 2))
    end_time = self.__formatDate(datetime.datetime.utcnow())
    body = {"filters":[
	          {"type":"start_time","values":[start_time]},
	          {"type":"end_time","values":[end_time]},
	          {"type":"environment","values":["gcp-api"]}],
          "page":0,"per_page":0,"sort":"latest_report.end_time","order":"DESC"}
    nodesList = self.apiClient.post("compliance/reporting/nodes/search", body)["nodes"]
    for node in nodesList:
      if (node["latest_report"]["status"] == "failed"):
        reportList.append(node["latest_report"]["id"])
    return self.__checkDuplicates(reportList)

  def __getGcpNodeManager(self):
    gcpNodeManager = ""
    body = '{"filter_map": [{"key": "manager_type","exclude": true,"values": [ "aws-ec2","aws-api", "azure-api"]}]}'
    try:
      response = self.apiClient.post("nodemanagers/search", json.loads(body))
      nodeManagers = response["managers"]
    except Exception as e: 
      self.logger.exception(e)
      self.logger.error(response)
    for manager in nodeManagers:
      if("CSCC-Integration" in manager["name"] and manager["type"] == "gcp-api" and manager["status"] == "reachable"):
        gcpNodeManager = manager["id"]
    if (not gcpNodeManager):
      try:
        response = self.createCloudManagementService(self.properties.serviceAccount)
        gcpNodeManager = response["ids"][0]["id"] 
      except Exception as e: 
        self.logger.exception(e)
        self.logger.error(response) 
    else:
      self.logger.info("Using existing GCP Node Integration: " + gcpNodeManager)
    return gcpNodeManager

  def __formatDate(self, date):
    formattedDate = date.strftime("%Y-%m-%dT%H:%M:%S%Z")
    return formattedDate + "Z"

  def __formatScanDateTime(self, date):
    formattedDate = date.strftime("%Y%m%dT%H%M%S%Z")
    return formattedDate + "Z"

  def __checkDuplicates(self, reportList):
    if self.lastSentReports:
      uniqueReportList = list(set(reportList) - set(self.lastSentReports))
      self.lastSentReports.clear()
      self.lastSentReports.extend(reportList)
      return uniqueReportList
    else:
      self.lastSentReports.extend(reportList)
      return reportList
    