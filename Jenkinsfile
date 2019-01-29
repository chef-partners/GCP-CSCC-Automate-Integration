def pod_label = "cscc-automate-${UUID.randomUUID().toString()}"
def app_version = "1.0.0"
pipeline {
  agent {
    kubernetes {
      label pod_label
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: cscc
    image: gcr.io/chefio-saas/cscc-automate:latest
    command: ['cat']
    tty: true
"""
    }
  }
    stages {
        stage('Build Information') {
            steps {
                container('cscc') {
                    sh 'pwd'
                    sh 'ls -al'
                    sh 'echo $PATH'
                }
            }
        }
        stage('Unit Tests') {
            steps {
            withCredentials([file(credentialsId: 'cscc-app-properties', variable: 'APP_PROPS')]) {
                withCredentials([file(credentialsId: 'CSCC_KEY', variable: 'CSCC_KEY')]) {
                container('cscc') {
                    dir('reporter/') {
                    sh 'cp $APP_PROPS app.properties.json'
                    sh 'cp $CSCC_KEY csccKey.json'
                    sh 'ls -la'
                    sh 'cat app.properties.json > app/app.properties.json'
                    sh 'cat csccKey.json > app/csccKey.json'
                    sh 'pytest -p no:warnings app/test_app.py'
                }
                }
                }
              }
            }
        }
    }

  options {
    buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '10')
  }
 }