from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler 
from automate.automate_service import AutomateService
from cscc.cscc_service import CsccService
import logging
import sys

class JobListener(BackgroundScheduler):
  logger = logging.getLogger(__name__)

  def listen(self, automateService, csccService):
    reports = automateService.findReports()
    failedControls = automateService.getFailedControls(reports)
    findings = csccService.buildFindings(failedControls)
    for finding in findings:
      csccService.createFinding(finding)
    if len(findings) > 0:
       self.logger.info(f"Creating {len(findings)} findings")

    

      



