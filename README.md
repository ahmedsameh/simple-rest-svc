# A simple Rest API systemd service with full CI/CD/CD through packer, Ansible, Docker, Kubernetes, Jenkins, Prometheus & Grafana

Simple Rest API using python and Flask, the API is initialized using systemd service and it has the following information
a. Path: '/info'
b. Method: GET
c. Format: JSON

```json
{"date":"", "time":"", "ip":"", "hash":""}
```

The service is used through a systemd service, various deployment options are available through Packer, Docker, Ansible and Over the Google cloud using GKE, the whole project is following the CI/CD/CD principals using Jenkins pipeline, also Monitoring is available therough Prometheus & Grafana.

## Prerequistes

Please insure that you have installed all the following components locally:

* Packer
* KVM/Qemu
* Ansible
* Docker
* Jenkins with Blue Ocean
* Kubectl
* Gcloud SDK

You will need to create GCloud Project and service account key for it.

## Configuration & Building Project

### Build and Run the whole project

* Create a GCloud cluster through your convinent way, and edit `project.properies` to include the cluster name.
* Change the project variables at `project.properies` file to yours.
* Fork the project.
* Create a new jenkins Blue Ocean pipeline.
* Link the pipeline to your github account.
* Run the pipeline

The pipeline has the following stages:

1. init - initialize enviorment variables from `project.propperties`.

2. Build - Build the source code.

3. Test - Test the source code with tests avaliable in `/tests` completeing the CI "Continous Integration" stage.

4. Deliver - Build Docker image with the latest code.

5. Test Delivery - Test the docker image, the current implemented test is very simple, more compicated tests can be added.

6. Publish - Publish the image to google gcr Completing the CD "Continous Delivery" stage.

7. Deploy - Deploy the whole project in K8S cluster.

## Configure Monitoring and Dashboards

* Note the Ingress service external IP address after the installation you can use the follwoing bash commands.

```bash
gcloud container clusters get-credentials YOUR_CLUSTER_NAME
kubectl get ingress
```

* Change the IP address at the last line at `config/prometheus/prometheus.yml` to your ingress IP address and port if necessary.
* Run the monitoring environment using the following bash command

```bash
docker-compose -f docker-prometheus-grafana.yml up
```

* Access Grafana at <http://127.0.0.1:3000>

```none
Username: admin
Password: admin
```

## Image only Usage

### Build the image using packer

```bash
cd packer
packer build centos7.json
```

The output image will be at

```bash
paker/build
```

### Build and run Docker image for standalone usage

```bash
docker build --rm -f "Dockerfile" -t local\docker:latest .
docker run -ti --privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 5000:5000 local\docker:latest
```

The service will be up at <http://localhost:5000/info>

## Interesting future work

* Prepare K8S depyment for Prometheus and Grafana to consolidate the project.
* Add more unit tests and integration tests.
