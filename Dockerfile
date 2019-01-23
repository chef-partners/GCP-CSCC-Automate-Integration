FROM python:3.7.2-stretch
RUN echo "deb http://packages.cloud.google.com/apt cloud-sdk-stretch main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  apt-get update && apt-get install -y google-cloud-sdk
RUN git clone https://github.com/chef-partners/GCP-CSCC-Automate-Integration.git 
COPY /home/app.properties.json GCP-CSCC-Automate-Integration/reporter/app/
RUN pip install -r requirements.txt
ENTRYPOINT ["python" "GCP-CSCC-Automate-Integration/reporter/app/app.py"]