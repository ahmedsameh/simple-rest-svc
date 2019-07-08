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
            //if the tests are passing I will just deliver the artifacts 
            //and as may app is .py file "I am not compiling it" I will just deliver the Docker file
            steps {
                echo 'I am Delivering only the Dockerfile to be visible at Jenkins artifacts'
            }
            post {
                success {
                    archiveArtifacts 'Dockerfile'
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