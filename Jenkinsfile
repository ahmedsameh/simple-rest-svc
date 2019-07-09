def getEnvVar(String paramName){
    return sh (script: "grep '${paramName}' ./project.properties|cut -d'=' -f2", returnStdout: true).trim();
}
pipeline {
    agent none
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('init') {
            agent any
            steps{
                script{
                    env.JENKINS_GCLOUD_CRED_ID = getEnvVar('JENKINS_GCLOUD_CRED_ID')
                    env.GCLOUD_PROJECT_ID = getEnvVar('GCLOUD_PROJECT_ID')
                    env.GCLOUD_K8S_CLUSTER_NAME = getEnvVar('GCLOUD_K8S_CLUSTER_NAME')
                    env.JENKINS_GCLOUD_CRED_LOCATION = getEnvVar('JENKINS_GCLOUD_CRED_LOCATION')
                }
            }      
        }
        stage('Build') {
            agent {
                docker {
                    image 'python:3.6'
                }
            }
            steps {
                sh 'python3 -m py_compile app/msg_of_the_day.py'
            }
        }
        stage('Test') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'tests'
                }
            }
            steps {
                sh 'nose2 --plugin nose2.plugins.junitxml -s tests -c tests/unittest.cfg'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deliver') { 
            agent any
            steps {
                //Building docker image for delivery
                sh 'docker build --rm -f "Dockerfile" -t gcr.io/${GCLOUD_PROJECT_ID}/c7-msg-of-the-day:latest .'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'Dockerfile', fingerprint: true
                }
            }
        }
        stage('Test Delivery') {
            agent any
            steps {
                //only testing service is up and delivery is succeding, more complicated testing can be added
                sh 'docker run -d -ti --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 5000:5000 gcr.io/${GCLOUD_PROJECT_ID}/c7-msg-of-the-day:latest'
                sleep 30
                sh 'curl http://127.0.0.1:5000/info'
                sh 'docker stop $(docker ps -q --filter ancestor=gcr.io/${GCLOUD_PROJECT_ID}/c7-msg-of-the-day:latest)'
            }
        }
        stage('Publish') {
            agent any
            steps {
                sh 'cat ${JENKINS_GCLOUD_CRED_LOCATION} | docker login -u _json_key --password-stdin https://gcr.io'
                sh 'docker push gcr.io/${GCLOUD_PROJECT_ID}/c7-msg-of-the-day:latest'
            }      
        }
        stage('Deploy'){
            agent any
            steps {
                sh """
                    #!/bin/sh -xe
                    gcloud auth activate-service-account ${JENKINS_GCLOUD_CRED_ID} --key-file=${JENKINS_GCLOUD_CRED_LOCATION}
                    gcloud config set compute/zone europe-west3-c
                    gcloud config set compute/region europe-west3
                    gcloud config set project ${GCLOUD_PROJECT_ID}
                    gcloud container clusters get-credentials ${GCLOUD_K8S_CLUSTER_NAME}
                    kubectl apply --force=true --all=true --record=true -f ./k8s/msg_of_the_day-deployment.yml
                    """
            }

        }
    }
}