#!/bin/sh
kubectl delete ingress msg-of-the-day-ingress
kubectl delete service msg-of-the-day-svc
kubectl delete deployment msg-of-the-day