FROM python:3.7.2-stretch
RUN echo "deb http://packages.cloud.google.com/apt cloud-sdk-stretch main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  apt-get update && apt-get install -y google-cloud-sdk
RUN git clone https://github.com/chef-partners/GCP-CSCC-Automate-Integration.git 
RUN pip install -r GCP-CSCC-Automate-Integration/reporter/requirements.txt
CMD pip-licenses --with-license-file >> licenses_full.txt && pip-licenses >> licenses_list.txt
ENTRYPOINT python GCP-CSCC-Automate-Integration/reporter/app/app.py gcp
