import json
import sys
import yaml
from jinja2 import Template
from subprocess import check_output, run
import time


def read_config(config_file):
    input_file = open(config_file, 'rb')
    return yaml.load(input_file.read())


if len(sys.argv) != 2:
    print("Usage: %s <yaml config>" % sys.argv[0])
    sys.exit(-1)

if __name__ == '__main__':
    # read config
    config = read_config(sys.argv[1])

    while True:

        stolon_json = json.loads(check_output("stolonctl clusterdata", shell=True))
        haproxy_template = open('./stolon_haproxy.j2', 'r')

        standby_list = []

        # get standby's 
        for db in stolon_json['DBs']:
            if stolon_json['DBs'][db]['status']['healthy'] and stolon_json['DBs'][db]['spec']['role'] == 'standby':
                standby_list.append(stolon_json['DBs'][db]['status']['listenAddress'] + ':' + stolon_json['DBs'][db]['status']['port'])
        # print(standby_list)

        template = Template(haproxy_template.read())
        new_render = template.render(servers=standby_list,
                                frontend_port=config['postgres_haproxy_port'])

        haproxy_config = open(config['postgres_haproxy_config'], 'w+')
        if haproxy_config.read() == new_render:
            print("Config not changed!")
        else:
            print("Config changed!")
            haproxy_config.write(new_render)
            run(config['haproxy_reload_command'], shell=True, check=True)
            
        haproxy_config.close()
        haproxy_template.close()

        time.sleep(config['timeout'])
