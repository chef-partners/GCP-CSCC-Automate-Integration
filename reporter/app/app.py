import sys
from automate.automate_client import AutomateClient
from automate.automate_service import AutomateService
from automate.job_listener import JobListener
from cscc.cscc_service import CsccService
from logging.config import dictConfig
from properties import Properties
import datetime
import time
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
  # Init automate and cscc service with app.properties
  properties = Properties()
  automate = AutomateService(properties)
  cscc = CsccService(properties, properties.sourceId)

  # Start Intial Scan.
  automate.startScan()

  # Start JobListener
  jobListener = JobListener()
  jobListener.start()
  jobListener.add_job(jobListener.listen, 'interval', seconds=60, args=[automate, cscc])

  while True:
   time.sleep(1)
 
if __name__ == "__main__":
  main()
