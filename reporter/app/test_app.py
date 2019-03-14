import json
import pytest
import os
from automate.automate_service import AutomateService
from cscc.cscc_service import CsccService
from properties import Properties
from datetime import datetime, timedelta
from google.protobuf import empty_pb2, struct_pb2, timestamp_pb2

class TestCsccService:
    # Tests that findings built from an Automate Report equals the number of Failed Controls
    def testBuildFindings(self):
        #SETUP
        properties = Properties()
        testSecuritySource = 'organizations/827482578277/sources/9233151395087538604'
        cscc = CsccService(properties, testSecuritySource)
        automate = AutomateService(properties)
        # GIVEN a report with Failing Controls
        reports = []
        path = f"{os.getcwd()}/test_resources"
        with open(os.path.join(path, 'mock_report.json')) as r:
            report = json.load(r)
        reports.append(report)

        # WHEN failed controls are extracted
        failedControls = automate.getFailedControls(reports)

        # THEN cscc findings can be built
        findings = cscc.buildFindings(failedControls)
        assert len(findings) == 23

    # Tests that a finding is successfully created in Google Cloud Security Centre
    @pytest.mark.skip(reason="Creates a new finding on cscc. Don't run until deletion is enabled.")
    def testCreateFindings(self):
        #SETUP
        properties = Properties()
        testSecuritySource = 'organizations/827482578277/sources/9233151395087538604'
        cscc = CsccService(properties, testSecuritySource)

        # GIVEN a mock finding
        finding = {'name': 'TESTFINDING123', 'parent': 'organizations/827482578277/sources/9233151395087538604', 
        'resource_name': 'organizations/827482578277/projects/test-project', 'state': 'INACTIVE', 'category': 'TEST-CATEGORY', 
        'external_uri': 'https://35.197.241.246/compliance/reporting/nodes/d35f7363-4d0a-40a3-b52d-d92ff1050c33', 
        'source_properties': {'control_id': struct_pb2.Value(string_value="cis-gcp-benchmark-vms-4.6"),
        'control_title': struct_pb2.Value(string_value='Title'), 'code_description': struct_pb2.Value(string_value="Instance chef-automate should have disks encrypted with csek"),
        'code_message': struct_pb2.Value(string_value="expected #has_disks_encrypted_with_csek? to return true, got false"),
        'summary': struct_pb2.Value(string_value="CIS Google Cloud Platform Foundation Benchmark Level 2"),
        'status': struct_pb2.Value(string_value='Fail')}, 'security_marks': {}, 'event_time': cscc.timestamp(datetime.now()),
        'create_time': cscc.timestamp(datetime.now())}

        # WHEN create finding is called
        cscc.createFinding(finding)

        # THEN findings are sent to cscc
        findingList = cscc.getAllFindings()
        assert len(findingList) >=1 