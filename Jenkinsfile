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
    }
}