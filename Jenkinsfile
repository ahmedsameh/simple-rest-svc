pipeline {
    agent none
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:2-alpine'
                }
            }
            steps {
                sh 'python -m py_compile app/msg_of_the_day.py'
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'python:3.6'
                }
            }
            steps {
                sh "pip install flask"
                sh 'python --verbose --junit-xml test-reports/results.xml ./'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}