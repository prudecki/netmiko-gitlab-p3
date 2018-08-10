from netmiko import ConnectHandler

#import gitlab
import requests
import re
from jinja2 import Environment

# download ip adresses from zenoss
dsa = {
    'device_type': 'cisco_ios',
    'ip': '172.17.0.101',
    'username': 'test',
    'password': 'test',
}

connect = ConnectHandler(**dsa)

#with gitlab.Gitlab('http://172.17.0.2', 'x6sP6xf57gb5sxxiXutq') as git:
#    get = git.projects.get('root/netmiko')
#    file = gitlab.Gitlab
#    print(file)
#
#git_req = requests.get('http://172.17.0.3/api/v4/projects/1/repository/files/start/raw?ref=master', headers={'PRIVATE-TOKEN': 'x6sP6xf57gb5sxxiXutq'})
#print(git_req.text)
#
#out = git_req.text.splitlines()
#
## check if out is a list and send commands
#if isinstance(out, list):
#    connect.send_config_set(out)
#else:
#    raise AttributeError

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
pass


