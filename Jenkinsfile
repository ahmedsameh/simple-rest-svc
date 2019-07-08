pipeline {
    agent none
    options {
        skipStagesAfterUnstable()
    }
    stages {
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
                //testing docker file build
                sh 'docker build --rm -f "Dockerfile" -t c7-msg-of-the-day:B${BUILD_NUMBER} .'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'Dockerfile', fingerprint: true
                }
            }
        }
        stage('Test Delivery') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir '.'
                }
            }
            steps {
                //only testing service is up and delivery is succeding, more complicated testing can be added
                sh 'curl 127.0.0.1:5000'
            }
        }
    }
}