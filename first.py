from netmiko import ConnectHandler
from jinja2 import Template
import requests
import re

# download ip adresses from zenoss
dsa = {
    'device_type': 'cisco_ios',
    'ip': '172.17.0.101',
    'username': 'test',
    'password': 'test',
}

connect = ConnectHandler(**dsa)


git_req = requests.get('http://172.17.0.3/api/v4/projects/1/repository/files/start/raw?ref=master', headers={'PRIVATE-TOKEN': 'x6sP6xf57gb5sxxiXutq'})
print(git_req.text)
out = git_req.text.splitlines()

# check if out is a list and send commands
if isinstance(out, list):
    connect.send_config_set(out)
else:
    raise AttributeError

check_interface_status = connect.send_command('show interface status')
print(check_interface_status)

access = []
trunk = []

for line in check_interface_status.split('\n'):
    interfaces = re.match('^(?P<int_name>\w+\d+\/\d+).*\w+\s+(?P<int_vlan>trunk|\d+).*$', line)
    if interfaces is not None:
        interface = {}
        if interfaces.group('int_vlan') != 'trunk':
            interface['name'] = interfaces.group('int_name')
            interface['vlan'] = interfaces.group('int_vlan')
            access.append(interface)
        elif interfaces.group('int_vlan') == 'trunk':
            interface['name'] = interfaces.group('int_name')
            interface['vlan'] = interfaces.group('int_vlan')
            trunk.append(interface)

int_access_template = ''
int_trunk_template = ''

# configure access interfaces
if access is not None:
    get_int_access_template = requests.get('http://172.17.0.3/api/v4/projects/1/repository/files/access/raw?ref=master',
                                           headers={'PRIVATE-TOKEN': 'x6sP6xf57gb5sxxiXutq'})
    if get_int_access_template.status_code == 200:
        int_access_template = Template(get_int_access_template.text)
    else:
        requests.exceptions.RequestException()
    conf_access_interfaces = int_access_template.render(interfaces=access)
    apply_access_interface_conf = connect.send_config_set(conf_access_interfaces)
    print(apply_access_interface_conf)

# configure trunk interfaces
if trunk is not None:
    get_int_trunk_template = requests.get('http://172.17.0.3/api/v4/projects/1/repository/files/trunk/raw?ref=master',
                                          headers={'PRIVATE-TOKEN': 'x6sP6xf57gb5sxxiXutq'})
    if get_int_trunk_template.status_code == 200:
        int_trunk_template = Template(get_int_trunk_template.text)
    else:
        requests.exceptions.RequestException()
    conf_trunk_interfaces = int_trunk_template.render(interfaces=trunk)
    apply_trunk_interface_conf = connect.send_config_set(conf_trunk_interfaces)
    print(apply_trunk_interface_conf)

