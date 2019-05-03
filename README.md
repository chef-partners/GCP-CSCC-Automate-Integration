![Google Cloud](logo_cloud_192.png)

# Chef Automate Integration with Google Cloud SCC

This guide helps install and configure the integration of Chef Automate with [Google's Cloud Security Command Center](https://cloud.google.com/security-command-center/)

### Chef Automate - Google Cloud SCC Integration (Beta)

The integration between a Chef Automate server and Google Cloud SCC requires the following:

* Chef Automate
* [Google Cloud Subscription](https://cloud.google.com/) with Cloud SCC Enabled

The Chef Automate integration with Google Cloud SCC has been developed in order to allow Compliance Scan results for the Google Cloud API to be shown in the Cloud Security Command Center Dashboard, along with other security and compliance findings for the Organisations Projects. The initial implementation uses the [CIS Certified Google Cloud Platform Foundation Benchmark from Chef](https://www.cisecurity.org/partner/chef/) in order to check the compliance of the GCP Organisation with respect to the controls from the Benchmark at both Level 1 and Level 2.


#### Pre-requisites

* [Google Cloud Subscription](https://cloud.google.com/)
* [Google Cloud SCC Feature Enabled](https://cloud.google.com/security-command-center/)
* [Chef automate server installation](https://docs.chef.io/chef_automate.html)

### Configuration

#### Getting started on GCP Marketplace

1. On Google Cloud Marketplace select the Chef Automate CSCC integration https://console.cloud.google.com/marketplace/

2. Click Deploy and complete the required fields
- automate-ip: The public ip address of the Chef Automate instance
- source-id: The source id of the Chef Source found on the Cloud SCC Security
- organization-id: The organization id of the GCP organization
- automate-api-token: The api token from Chef Automate instance
- cscc-key: The GCP service account json key with cloud security centre access

#### Getting started on local machine

- Assumption that gcloud SDK is installed
- Create or update a Service Account that has Cloud Compute Instance create role for installing integration tools
- Create Service Account for Cloud SCC Access, Retrieve Key and Add Admin role:
1. gcloud iam service-accounts create <SERVICE_ACCOUNT> --display-name "service account for Cloud SCC Integration" --project <PROJECT_ID>
2. gcloud iam service-accounts keys create <KEY_FILE_NAME.json> --iam-account <SERVICE_ACCOUNT>@<PROJECT_ID>.iam.gserviceaccount.com
3. gcloud beta organizations add-iam-policy-binding <ORGANIZATION_ID> --member="serviceAccount:<SERVICE_ACCOUNT>@<PROJECT_ID>.iam.gserviceaccount.com" --role='roles/securitycenter.adminEditor' --role='roles/compute.admin'
4. Enable the Google Cloud SCC API for the Service Account Project going to https://console.developers.google.com/apis/api/securitycenter.googleapis.com/overview?project=YOUR_PROJECT_ID and clicking Enable

### Install Google Cloud SCC Integration for Chef

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
* scanProfiles: The app launches a recurring scan with this profile. The results are automatically sent to Cloud SCC.
* automateApiToken: The API token from your Chef Automate Instance.
* organization: The Organization Id
* source: The source id of the Chef Automate Cloud SCC source - recorded when you added the Integration in Google Marketplace
* cscc: The Path to your Cloud SCC json key file created at Step 2 above.
* serviceAccount: The gcloud service account used to create the GCP Node Integration in Step 1 above. Requires compute.admin role

#### Launch the App

Once configuration is complete the reporter app can be launched. See sample_app.properties.json for an example of complete configuration. To run the app using the properties file use the args 'file'.

$ cd reporter

$ python3.7 app/app.py file

