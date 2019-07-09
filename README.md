# simple-rest-svc
Simple Rest Service using python and Flask, the service is used through a systemd service, deployments through Packer or Docker are available.

Installations
Prerequistes
Jenkins & Docker installed locally
Kubectl and Gcloud SDK


cat /var/lib/jenkins/Test-KE-1fcb98ac0434.json | docker login -u _json_key --password-stdin https://gcr.io


Create GCloud Cluster
gcloud container clusters create msg-of-the-day-cluster --num-nodes=2

Get Cluster Credentials
gcloud container clusters get-credentials msg-of-the-day-cluster