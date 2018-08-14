# HAProxy config generator for Stolon replicas

## Setup

* Create Python 3.6 virtualenv
* Clone repo into it
* Install requirements `pip install -r requirements.txt`
* Set needed variables in config.yml

## Usage

`python src/main.py config.yml`

Script will check stolon state every `timeout` secs and restart HAProxy with new config every time when state was changed.