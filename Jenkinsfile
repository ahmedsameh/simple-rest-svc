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
                docker {
                    image 'python:3.6'
                }
            }
            steps {
                sh 'mkdir env'
                sh 'python3 -m venv env'
                sh 'source ./env/bin/activate' 
                sh 'python3 -m pip install flask'
                sh 'python3 --verbose --junit-xml test-reports/results.xml ./'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}