import datetime
import daemon
import time
import logging
import os
import sys
from automate.automate_client import AutomateClient
from automate.automate_service import AutomateService
from automate.job_listener import JobListener
from cscc.cscc_service import CsccService
from logging.config import dictConfig
from properties import Properties

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
dir = os.getcwd()
with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stderr, working_directory=dir):
  def main(propertyEnv):
    # Init automate and cscc service with app.properties
    properties = Properties(propertyEnv[0])
    automate = AutomateService(properties)
    cscc = CsccService(properties, properties.sourceId)

    # Start Intial Scan.
    if properties.scanProfiles and properties.scanProfiles is not None:
      automate.startScan()

    # Start JobListener
    jobListener = JobListener()
    jobListener.start()
    jobListener.add_job(jobListener.listen, 'interval', seconds=120, args=[automate, cscc], max_instances=2)

    while True:
      time.sleep(1)
if __name__ == "__main__":
  main(sys.argv[1:])