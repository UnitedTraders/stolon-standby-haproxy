[![Known Vulnerabilities](https://snyk.io/test/github/UnitedTraders/stolon-standby-haproxy/badge.svg)](https://snyk.io/test/github/UnitedTraders/stolon-standby-haproxy)
# HAProxy config generator for Stolon replicas

## Setup

* Create Python 3.6+ virtualenv
* Clone repo into it
* Install requirements `pip install -r requirements.txt`
* Set needed variables in config.yml and environment variables for stolonctl

## Configuration

```yml
# port which haproxy binds to
postgres_haproxy_port: 35432
# path for generated config for haproxy
postgres_haproxy_config: '/etc/haproxy/stolon_standby.cfg'
# command for reloading haproxy when config changed
haproxy_reload_command: '/usr/bin/sudo systemctl reload haproxy'
# period between stolon status check in seconds
timeout: 60
# if set to true, stolon-haproxy will bind to master when no healthy slaves available
fallback_to_master: false
# settings below used for haproxy backend configuration, see haproxy documentation (https://www.haproxy.com/documentation/aloha/10-0/traffic-management/lb-layer7/health-checks/)
# timeout for haproxy tcp check
inter_timeout_ms: 1000
# how many checks should be failed before postgres instance will marked as DONW
fall_count: 3
# how many checks should be succeed before postgres instance will marked as UP
rise_count: 2
```

## Example systemd unit

```systemd
[Unit]
Description=stolon_haproxy is script for access to the stolon replicas
After=network.target
Requires=network.target

[Service]
ExecStart=/opt/stolon_haproxy/env/bin/python src/stolon_haproxy.py config.yml
User=ansible
Environment="STOLONCTL_CLUSTER_NAME=pg-stolon"
Environment="STOLONCTL_STORE_BACKEND=etcdv3"
Environment="STOLONCTL_STORE_ENDPOINTS=http://localhost:2379"
Environment="PATH=$PATH:/usr/stolon-0.10.0/bin"
WorkingDirectory=/opt/stolon_haproxy/sources
Restart=on-failure
RestartSec=100ms
```

## Usage

`python src/stolon_haproxy.py config.yml`

Script will check stolon state every `timeout` secs and restart HAProxy with new config every time when state was changed.

## Docker

All Docker-related configs stored in `docker` folder (except Dockerfile).

Build: `docker build -t registry/stolon-haproxy:latest .`

Run: `docker run --rm -e STOLONCTL_CLUSTER_NAME=pg-stolon -e STOLONCTL_STORE_BACKEND=etcdv3 -e STOLONCTL_STORE_ENDPOINTS=http://etcd.example.com:2379 registry/stolon-haproxy`

## Testing

```bash

[venv] $ cd src

[venv] $ python -m unittest -v stolon_haproxy_test.py

test_with_fallback (stolon_haproxy_test.TestStolonJson) ... ok
test_without_fallback (stolon_haproxy_test.TestStolonJson) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.002s
```

## TODO (PRs are welcome ;) )

* Apply Docker best practices (run from unprivileged user etc);
* Handle exceptions in main script;
* CI/CD, Docker Hub publishing;
* Tune default HAProxy config;
* Prometheus metrics (master fallback, last haproxy reload, reload counter).
