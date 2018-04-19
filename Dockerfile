# Docker continer to run sdor as cronjob in Kubernetes
FROM fredhutch/ls2_ubuntu:16.04_20180126
USER root
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
    python \
    python-swiftclient

COPY sdor.py /sdor.py
COPY run-sdor-list /run-sdor-list
