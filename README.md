![Google Cloud](logo_cloud_192.png)

## Overview

This guide helps install and configure the integration of Chef Automate with [Google's Cloud Security Command Center](https://cloud.google.com/security-command-center/)

### Chef Automate - Google CSCC Integration (Beta)

The integration between a Chef Automate server and Google CSCC requires the following:

* Chef Automate
* [Google Cloud Subscription](https://cloud.google.com/) with CSCC Enabled

The Chef Automate integration with Google CSCC has been developed in order to allow Compliance Scan results for the Google Cloud API to be shown in the Cloud Security Command Center Dashboard, along with other security and compliance findings for the Organisations Projects. The initial implementation uses the [CIS Certified Google Cloud Platform Foundation Benchmark from Chef](https://www.cisecurity.org/partner/chef/) in order to check the compliance of the GCP Organisation with respect to the controls from the Benchmark at both Level 1 and Level 2.


#### Pre-requisites

* [Google Cloud Subscription](https://cloud.google.com/)
* [Google CSCC (Beta) Feature Enabled](https://cloud.google.com/security-command-center/)
* [Chef automate server installation](https://docs.chef.io/chef_automate.html)

### Configuration

#### Google GCP Configuration

- Assumption that gcloud SDK is installed
- Create or update a Service Account that has Cloud Compute Instance create role for installing integration tools
- Create Service Account for CSCC Access, Retrieve Key and Add Admin role:
1. gcloud iam service-accounts create <SERVICE_ACCOUNT> --display-name "service account for CSCC Integration" --project <PROJECT_ID>
2. gcloud iam service-accounts keys create <KEY_FILE_NAME.json> --iam-account <SERVICE_ACCOUNT>@<PROJECT_ID>.iam.gserviceaccount.com
3. gcloud beta organizations add-iam-policy-binding <ORGANIZATION_ID> --member="serviceAccount:<SERVICE_ACCOUNT>@<PROJECT_ID>.iam.gserviceaccount.com" --role='roles/securitycenter.adminEditor'
- Enable the Google CSCC API for the Service Account Project going to https://console.developers.google.com/apis/api/securitycenter.googleapis.com/overview?project=YOUR_PROJECT_ID and clicking Enable

### Install Google CSCC Integration for Chef

#### Dependencies

* python3.7 must be installed
* A Licensed installation of Chef Automate2

#### Installation Steps

$ git clone https://github.com/chef-partners/GCP-CSCC-Automate-Integration.git

$ cd reporter  

$ python3.7 -m venv tsenv

$ . tsenv/bin/activate

$ pip3.7 install -r requirements.txt

Add your configuration to "reporter/app/app.properties.json", an example version is available in the reporter directory "sample_app.properties.json"

* automatePublicIp: Public IP of the Chef Automate Server
* scanProfiles: The app launches a recurring scan with this profile. The results are automatically sent to CSCC.
* automateApiToken: The API token from your Chef Automate Instance.
* organization: The Organization Id
* source: The source id of the Chef Automate CSCC source - recorded when you added the Integration in Google Marketplace
* cscc: The Path to your CSCC json key file created at Step 2 above.
* serviceAccount: The gcloud service account used to create the GCP Node Integration in Step 1 above.

#### Launch the App

Once configuration is complete the reporter app can be launch. See sample_app.properties.json for an example of complete configuration.

$ cd reporter

$ python3.7 app/app.py 

