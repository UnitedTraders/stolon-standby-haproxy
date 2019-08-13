import json
import sys
import yaml
import os
from jinja2 import Template
from subprocess import check_output, run
import time


def read_config(config_file):
    input_file = open(config_file, 'rb')
    return yaml.load(input_file.read())
 
def check_env_variables():
    need_env = ['STOLONCTL_CLUSTER_NAME', 'STOLONCTL_STORE_BACKEND', 'STOLONCTL_STORE_ENDPOINTS']
    for ne in need_env:
        if ne not in os.environ:
            sys.stderr.write("Please set {} environment variable".format(ne))
            sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: %s <yaml config>" % sys.argv[0])
        sys.exit(-1)

    # read config
    config = read_config(sys.argv[1])
    check_env_variables()

    while True:

        stolon_json = json.loads(check_output(
            "stolonctl clusterdata", shell=True))
        haproxy_template = open('./stolon_haproxy.j2', 'r')

        standby_list = []

        # Adding support for newer version stolon clusterdata format
        if 'DBs' in stolon_json:
            key = 'DBs'
        else:
            key = 'dbs'

        # get standby's
        for db in stolon_json[key]:
            database = stolon_json[key][db]
            if 'healthy' in database['status'] and 'listenAddress' in database['status']:
                if database['status']['healthy'] and database['spec']['role'] == 'standby':
                    standby_list.append(
                        database['status']['listenAddress'] + ':' + database['status']['port'])
        # print(standby_list)

        template = Template(haproxy_template.read())
        new_render = template.render(servers=standby_list,
                                     frontend_port=config['postgres_haproxy_port'])

        haproxy_config = open(config['postgres_haproxy_config'], 'r')
        if haproxy_config.read() == new_render:
            print("Config not changed!")
        else:
            print("Config changed!")
            haproxy_config.close()
            haproxy_config = open(config['postgres_haproxy_config'], 'w')
            haproxy_config.write(new_render)
            run(config['haproxy_reload_command'], shell=True, check=True)

        haproxy_config.close()
        haproxy_template.close()

        time.sleep(config['timeout'])