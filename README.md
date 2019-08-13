# HAProxy config generator for Stolon replicas

## Setup

* Create Python 3.6+ virtualenv
* Clone repo into it
* Install requirements `pip install -r requirements.txt`
* Set needed variables in config.yml and environment variables for stolonctl

## Example systemd unit

```systemd
[Unit]
Description=stolon_haproxy is script for access to the stolon replicas
After=network.target
Requires=network.target

[Service]
ExecStart=/opt/stolon_haproxy/env/bin/python src/main.py config.yml
User=ansible
Environment="STKEEPER_UID=pgtest3"
Environment="STOLONCTL_CLUSTER_NAME=pg-stolon"
Environment="STOLONCTL_STORE_BACKEND=etcdv3"
Environment="STOLONCTL_STORE_ENDPOINTS=http://localhost:2379"
Environment="PATH=$PATH:/usr/stolon-0.10.0/bin"
WorkingDirectory=/opt/stolon_haproxy/sources
Restart=on-failure
RestartSec=100ms
```

## Usage

`python src/main.py config.yml`

Script will check stolon state every `timeout` secs and restart HAProxy with new config every time when state was changed.

## Docker

All Docker-related configs stored in `docker` folder (except Dockerfile).

Build: `docker build -t registry/stolon-haproxy:latest .`

Run: `docker run --rm -e STKEEPER_UID=pgkeepertest -e STOLONCTL_CLUSTER_NAME=pg-stolon -e STOLONCTL_STORE_BACKEND=etcdv3 -e STOLONCTL_STORE_ENDPOINTS=http://etcd.example.com:2379 registry/stolon-haproxy`
