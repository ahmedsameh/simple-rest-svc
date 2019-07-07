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
                    image 'qnib/pytest'
                }
            }
            steps {
                sh "sudo pip install flask"
                sh 'py.test --verbose --junit-xml test-reports/results.xml ./'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}