# A simple Rest API systemd service with full CI/CD/CD through packer, Ansible, Docker, Kubernetes, Jenkins, Prometheus & Grafana

A simple Rest API using python and Flask, the API is initialized using systemd service and provides the following information on `/info`:

```json
{"date":"", "time":"", "ip":"", "hash":""}
```

The API is used through a systemd service, various deployment options are available through Packer, Docker, Ansible and Google Cloud using GKE, the whole project is following the CI/CD/CD principals using Jenkins pipeline, also Monitoring is available through Prometheus & Grafana.

## Perquisites

Please insure that you have installed all the following components locally:

* Packer
* KVM/Qemu
* Ansible
* Docker
* Jenkins with Blue Ocean
* Kubectl
* GCloud SDK

You will need to create GCloud Project and service account key for it.

## Configuration & Building Project

### Build and Run the whole project

* Fork the project.
* Create a GCloud cluster through your convenient way, and edit `project.properties` to include the cluster name.
* Change the project variables at `project.properties` file to yours.
* Create a new jenkins Blue Ocean pipeline.
* Link the pipeline to your github account.
* Run the pipeline

The pipeline has the following stages:

1. init - Initializes environment variables from `project.properties`.

2. Build - Build the source code.

3. Test - Test the source code with tests available in `/tests` completing the CI "Continuos Integration" stage.

4. Deliver - Build Docker image with the latest code.

5. Test Delivery - Test Docker image, the current implemented tests is very simple, more complicated tests can be added.

6. Publish - Publish the image to google gcr Completing the CD "Continuos Delivery" stage.

7. Deploy - Deploy the whole project in K8S cluster.

## Configure Monitoring and Dashboards

* Note the Ingress service external IP address and port after the installation; you can use the follwoing bash commands.

```bash
gcloud container clusters get-credentials YOUR_CLUSTER_NAME
kubectl get ingress
```

* Change the IP address and port at the last line at `config/prometheus/prometheus.yml` to your ingress IP address and port.
* Run the monitoring environment using the following bash command

```bash
docker-compose -f docker-prometheus-grafana.yml up
```

* Access Grafana at <http://127.0.0.1:3000>

```none
Username: admin
Password: admin
```

* Sometimes GCLoud ingress takes a long time to activate.

## Image only Usage

### Build image using packer

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

* Prepare K8S deployment for Prometheus and Grafana to consolidate the project.
* Add more unit tests and integration tests.
